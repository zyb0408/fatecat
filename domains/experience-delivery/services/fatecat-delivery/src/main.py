import asyncio
import json
import logging
import os
import secrets
import sys
import time
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime
from threading import Lock
from typing import Any
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response

from _paths import FATE_CORE_SRC_DIR, get_env_file
from branding import attach_branding, get_branding_payload, get_disclaimer_payload
from utils.timezone import now_cn

if str(FATE_CORE_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(FATE_CORE_SRC_DIR))

try:
    load_dotenv(get_env_file(), override=False)
except FileNotFoundError:
    pass

SERVICE_HOST = os.getenv("FATE_SERVICE_HOST", "127.0.0.1")
SERVICE_PORT = int(os.getenv("FATE_SERVICE_PORT", "8001"))
API_TOKEN = os.getenv("FATE_API_TOKEN", "").strip()


def _env_int(name: str, default: int, *, minimum: int = 0) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return max(value, minimum)


MAX_REQUEST_BYTES = _env_int("FATE_MAX_REQUEST_BYTES", 1_048_576, minimum=1024)
REQUEST_TIMEOUT_SECONDS = _env_int("FATE_REQUEST_TIMEOUT_SECONDS", 30, minimum=1)
RATE_LIMIT_PER_MINUTE = _env_int("FATE_RATE_LIMIT_PER_MINUTE", 120, minimum=0)
TRUST_PROXY_HEADERS = os.getenv("FATE_TRUST_PROXY_HEADERS", "").strip().lower() in {"1", "true", "yes"}
ENABLE_HSTS = os.getenv("FATE_ENABLE_HSTS", "").strip().lower() in {"1", "true", "yes"}

import db_v2 as db  # noqa: E402
from bazi_calculator import BaziCalculator  # noqa: E402
from fate_core.capabilities import CapabilityExecutor, CapabilityInput, list_capabilities  # noqa: E402
from fate_core.usecases import PureAnalysisInput, calculate_pure_analysis  # noqa: E402
from liuyao_factors import generate_factor  # noqa: E402
from models import (  # noqa: E402
    BaziData,
    BaziRequest,
    BaziResponse,
    BrandingInfo,
    LiuyaoFactorData,
    LiuyaoFactorRequest,
    LiuyaoFactorResponse,
    Meta,
    TimeInfo,
)
from prediction_systems import prediction_systems_payload  # noqa: E402
from report_generator import (  # noqa: E402
    build_report_hide,
    generate_full_report,
    normalize_report_system,
    public_birth_place,
)
from web_ui import render_web_report_page  # noqa: E402

logger = logging.getLogger(__name__)
_metrics_lock = Lock()
_request_counts: dict[tuple[str, str, int], int] = defaultdict(int)
_request_latency_seconds: dict[tuple[str, str, int], float] = defaultdict(float)
_request_latency_buckets: dict[tuple[str, str, int, str], int] = defaultdict(int)
_request_error_counts: dict[tuple[str, str, int, str], int] = defaultdict(int)
_inflight_requests = 0
_rate_limit_lock = Lock()
_rate_limit_windows: dict[str, deque[float]] = defaultdict(deque)
_RATE_LIMIT_EXEMPT_PATHS = {"/health", "/live", "/ready", "/metrics"}
_REQUEST_LATENCY_BUCKETS = (0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
_BODY_LIMIT_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def _records_enabled() -> bool:
    return os.getenv("FATE_RECORDS_ENABLED", "1").strip().lower() not in {"0", "false", "no", "off"}


if _records_enabled():
    db.ensure_db()


@dataclass(frozen=True)
class ApiPrincipal:
    role: str
    user_id: str | None = None

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"


class RequestBodyTooLarge(Exception):
    """请求体超过公网服务允许的最大字节数。"""


def _cors_allow_origins() -> list[str]:
    raw = os.getenv("FATE_CORS_ALLOW_ORIGINS", "").strip()
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def _extract_auth_token(x_api_key: str | None, authorization: str | None) -> str:
    if x_api_key:
        return x_api_key.strip()
    if authorization:
        scheme, _, value = authorization.strip().partition(" ")
        if scheme.lower() == "bearer" and value:
            return value.strip()
    return ""


def _admin_tokens() -> list[str]:
    tokens = [API_TOKEN, os.getenv("FATE_API_ADMIN_TOKEN", "").strip()]
    return [token for token in dict.fromkeys(tokens) if token]


def _user_tokens() -> dict[str, str]:
    raw = os.getenv("FATE_API_USER_TOKENS", "").strip()
    if not raw:
        return {}

    mapping: dict[str, str] = {}
    for item in raw.split(","):
        user_id, sep, token = item.strip().partition(":")
        if sep and user_id.strip() and token.strip():
            mapping[user_id.strip()] = token.strip()
    return mapping


def _require_record_access(x_api_key: str | None, authorization: str | None) -> ApiPrincipal:
    if not _records_enabled():
        raise HTTPException(status_code=403, detail="记录接口未启用")
    admin_tokens = _admin_tokens()
    user_tokens = _user_tokens()
    if not admin_tokens and not user_tokens:
        raise HTTPException(status_code=403, detail="记录接口未启用")
    supplied = _extract_auth_token(x_api_key, authorization)
    if not supplied:
        raise HTTPException(status_code=403, detail="未授权")
    for token in admin_tokens:
        if secrets.compare_digest(supplied, token):
            return ApiPrincipal(role="admin")
    for user_id, token in user_tokens.items():
        if secrets.compare_digest(supplied, token):
            return ApiPrincipal(role="user", user_id=user_id)
    raise HTTPException(status_code=403, detail="未授权")


def _require_owner_or_admin(principal: ApiPrincipal, user_id: str) -> None:
    if principal.is_admin:
        return
    if principal.user_id == user_id:
        return
    raise HTTPException(status_code=403, detail="无权访问该记录")


app = FastAPI(title="八字排盘服务", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=_cors_allow_origins(), allow_methods=["*"], allow_headers=["*"])


def _client_key(request: Request) -> str:
    if TRUST_PROXY_HEADERS:
        forwarded_for = request.headers.get("x-forwarded-for", "")
        if forwarded_for:
            return forwarded_for.split(",", 1)[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


def _route_label(request: Request) -> str:
    route = request.scope.get("route")
    path = getattr(route, "path", None)
    if isinstance(path, str):
        return path
    return request.url.path


def _json_error(status_code: int, error: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=attach_branding({"success": False, "error": error, "statusCode": status_code}),
    )


def _check_rate_limit(request: Request) -> tuple[bool, int]:
    if RATE_LIMIT_PER_MINUTE <= 0 or request.url.path in _RATE_LIMIT_EXEMPT_PATHS:
        return True, 0

    now = time.monotonic()
    key = _client_key(request)
    with _rate_limit_lock:
        window = _rate_limit_windows[key]
        cutoff = now - 60
        while window and window[0] <= cutoff:
            window.popleft()
        if len(window) >= RATE_LIMIT_PER_MINUTE:
            retry_after = max(1, int(60 - (now - window[0])))
            return False, retry_after
        window.append(now)
    return True, 0


def _record_request_metric(
    method: str,
    route: str,
    status_code: int,
    elapsed_seconds: float,
    *,
    error_class: str | None = None,
) -> None:
    key = (method, route, status_code)
    with _metrics_lock:
        _request_counts[key] += 1
        _request_latency_seconds[key] += elapsed_seconds
        for bucket in _REQUEST_LATENCY_BUCKETS:
            if elapsed_seconds <= bucket:
                _request_latency_buckets[(method, route, status_code, _format_bucket(bucket))] += 1
        _request_latency_buckets[(method, route, status_code, "+Inf")] += 1
        if error_class:
            _request_error_counts[(method, route, status_code, error_class)] += 1


def _classify_error(status_code: int) -> str | None:
    if status_code < 400:
        return None
    if status_code == 400:
        return "bad_request"
    if status_code in {401, 403}:
        return "auth"
    if status_code == 404:
        return "not_found"
    if status_code == 413:
        return "body_too_large"
    if status_code == 422:
        return "validation"
    if status_code == 429:
        return "rate_limited"
    if status_code == 504:
        return "timeout"
    if status_code >= 500:
        return "server_error"
    return "client_error"


def _format_bucket(bucket: float) -> str:
    return f"{bucket:g}"


def _escape_metric_label(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


async def _buffer_limited_body(request: Request) -> None:
    if request.method not in _BODY_LIMIT_METHODS:
        return

    received = 0
    chunks: list[bytes] = []
    async for chunk in request.stream():
        received += len(chunk)
        if received > MAX_REQUEST_BYTES:
            raise RequestBodyTooLarge
        if chunk:
            chunks.append(chunk)

    body = b"".join(chunks)
    request._body = body
    consumed = False

    async def replay_body():
        nonlocal consumed
        if consumed:
            return {"type": "http.request", "body": b"", "more_body": False}
        consumed = True
        return {"type": "http.request", "body": body, "more_body": False}

    request._receive = replay_body


def _apply_public_response_headers(response: Response, request_id: str) -> Response:
    response.headers["X-Request-ID"] = request_id
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
        "script-src 'self' 'unsafe-inline'; frame-ancestors 'none'",
    )
    if ENABLE_HSTS:
        response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
    return response


def _finalize_early_response(
    request: Request,
    response: Response,
    request_id: str,
    status_code: int,
    started: float,
    error_class: str,
) -> Response:
    elapsed = time.perf_counter() - started
    route = _route_label(request)
    _record_request_metric(request.method, route, status_code, elapsed, error_class=error_class)
    _log_request(request, request_id, route, status_code, elapsed, error_class=error_class)
    return _apply_public_response_headers(response, request_id)


def _log_request(
    request: Request,
    request_id: str,
    route: str,
    status_code: int,
    elapsed_seconds: float,
    *,
    error_class: str | None,
) -> None:
    payload = {
        "event": "http_request",
        "requestId": request_id,
        "method": request.method,
        "route": route,
        "status": status_code,
        "elapsedMs": round(elapsed_seconds * 1000, 3),
        "client": _client_key(request),
    }
    if error_class:
        payload["errorClass"] = error_class
    message = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if status_code >= 500:
        logger.error(message)
    elif status_code >= 400:
        logger.warning(message)
    else:
        logger.info(message)


@app.middleware("http")
async def production_guardrails(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or uuid.uuid4().hex
    started = time.perf_counter()
    content_length = request.headers.get("content-length")
    if content_length:
        try:
            if int(content_length) > MAX_REQUEST_BYTES:
                response = _json_error(413, "请求体过大")
                return _finalize_early_response(request, response, request_id, 413, started, "body_too_large")
        except ValueError:
            response = _json_error(400, "Content-Length 无效")
            return _finalize_early_response(request, response, request_id, 400, started, "bad_request")

    allowed, retry_after = _check_rate_limit(request)
    if not allowed:
        response = _json_error(429, "请求过于频繁")
        response.headers["Retry-After"] = str(retry_after)
        return _finalize_early_response(request, response, request_id, 429, started, "rate_limited")

    try:
        await _buffer_limited_body(request)
    except RequestBodyTooLarge:
        response = _json_error(413, "请求体过大")
        return _finalize_early_response(request, response, request_id, 413, started, "body_too_large")

    global _inflight_requests
    with _metrics_lock:
        _inflight_requests += 1

    status_code = 500
    error_class: str | None = None
    try:
        response = await asyncio.wait_for(call_next(request), timeout=REQUEST_TIMEOUT_SECONDS)
        status_code = response.status_code
        error_class = _classify_error(status_code)
    except TimeoutError:
        response = _json_error(504, "请求处理超时")
        status_code = 504
        error_class = "timeout"
    finally:
        elapsed = time.perf_counter() - started
        route = _route_label(request)
        _record_request_metric(request.method, route, status_code, elapsed, error_class=error_class)
        _log_request(request, request_id, route, status_code, elapsed, error_class=error_class)
        with _metrics_lock:
            _inflight_requests -= 1

    return _apply_public_response_headers(response, request_id)


def _branding_model() -> BrandingInfo:
    return BrandingInfo(**get_branding_payload())


def _disclaimer_model() -> str:
    return get_disclaimer_payload()


@app.exception_handler(HTTPException)
async def branded_http_exception_handler(_request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=attach_branding(
            {
                "success": False,
                "error": str(exc.detail),
                "statusCode": exc.status_code,
            }
        ),
    )


@app.exception_handler(RequestValidationError)
async def branded_validation_exception_handler(_request, exc: RequestValidationError):
    logger.info("API 请求参数校验失败: %s", exc.errors())
    return JSONResponse(
        status_code=422,
        content=attach_branding(
            {
                "success": False,
                "error": "请求参数无效",
                "statusCode": 422,
            }
        ),
    )


@app.exception_handler(Exception)
async def branded_exception_handler(_request, exc: Exception):
    logger.exception("未处理 API 异常")
    return JSONResponse(
        status_code=500,
        content=attach_branding(
            {
                "success": False,
                "error": "服务器内部错误",
                "statusCode": 500,
            }
        ),
    )


@app.get("/health")
def health():
    return attach_branding({"status": "ok"})


@app.get("/live")
def live():
    return attach_branding({"status": "live"})


@app.get("/ready")
def ready():
    checks = {"database": "disabled" if not _records_enabled() else "ok", "capabilities": "ok"}
    try:
        if _records_enabled():
            db.ensure_db()
        list_capabilities()
    except Exception as exc:
        logger.exception("readiness 检查失败")
        return JSONResponse(
            status_code=503,
            content=attach_branding({"status": "not_ready", "checks": checks, "error": str(exc)}),
        )
    return attach_branding({"status": "ready", "checks": checks})


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    lines = [
        "# HELP fatecat_requests_total Total HTTP requests.",
        "# TYPE fatecat_requests_total counter",
    ]
    with _metrics_lock:
        counts = dict(_request_counts)
        latencies = dict(_request_latency_seconds)
        latency_buckets = dict(_request_latency_buckets)
        error_counts = dict(_request_error_counts)
        inflight = _inflight_requests

    for (method, route, status_code), count in sorted(counts.items()):
        labels = f'method="{_escape_metric_label(method)}",route="{_escape_metric_label(route)}",status="{status_code}"'
        lines.append(f"fatecat_requests_total{{{labels}}} {count}")

    lines.extend(
        [
            "# HELP fatecat_request_latency_seconds HTTP request latency histogram.",
            "# TYPE fatecat_request_latency_seconds histogram",
        ]
    )
    for (method, route, status_code, bucket), count in sorted(latency_buckets.items()):
        labels = (
            f'method="{_escape_metric_label(method)}",route="{_escape_metric_label(route)}",'
            f'status="{status_code}",le="{bucket}"'
        )
        lines.append(f"fatecat_request_latency_seconds_bucket{{{labels}}} {count}")
    for (method, route, status_code), count in sorted(counts.items()):
        labels = f'method="{_escape_metric_label(method)}",route="{_escape_metric_label(route)}",status="{status_code}"'
        lines.append(f"fatecat_request_latency_seconds_count{{{labels}}} {count}")
    for (method, route, status_code), total in sorted(latencies.items()):
        labels = f'method="{_escape_metric_label(method)}",route="{_escape_metric_label(route)}",status="{status_code}"'
        lines.append(f"fatecat_request_latency_seconds_sum{{{labels}}} {total:.6f}")

    lines.extend(
        [
            "# HELP fatecat_request_errors_total Total HTTP error responses by class.",
            "# TYPE fatecat_request_errors_total counter",
        ]
    )
    for (method, route, status_code, error_class), count in sorted(error_counts.items()):
        labels = (
            f'method="{_escape_metric_label(method)}",route="{_escape_metric_label(route)}",'
            f'status="{status_code}",error_class="{_escape_metric_label(error_class)}"'
        )
        lines.append(f"fatecat_request_errors_total{{{labels}}} {count}")

    lines.extend(
        [
            "# HELP fatecat_inflight_requests Current in-flight HTTP requests.",
            "# TYPE fatecat_inflight_requests gauge",
            f"fatecat_inflight_requests {inflight}",
        ]
    )
    return PlainTextResponse("\n".join(lines) + "\n", media_type="text/plain; version=0.0.4")


@app.get("/web", response_class=HTMLResponse)
def web_report(
    birthDate: str | None = None,
    birthTime: str | None = None,
    birthPlace: str | None = None,
    gender: str | None = None,
    name: str | None = None,
    reportSystem: str | None = None,
):
    """原生 HTML Web 版标准 Markdown 报告。"""
    return render_web_report_page(
        birth_date=birthDate,
        birth_time=birthTime,
        birth_place=birthPlace,
        gender=gender,
        name=name,
        report_system=reportSystem,
    )


@app.get("/api/v1/report/systems")
def list_report_systems():
    """列出当前可用和未来规划的独立输出体系。"""
    return attach_branding({"success": True, "data": {"systems": prediction_systems_payload()}})


@app.get("/api/v1/capabilities")
def list_prediction_capabilities():
    """列出统一预测 capability 注册表。"""
    capabilities = [
        {
            "capabilityId": item.capability_id,
            "name": item.name,
            "tradition": item.tradition,
            "status": item.status,
            "defaultVisibility": item.default_visibility,
            "reportProfile": item.report_profile,
            "riskLevel": item.risk_level,
        }
        for item in list_capabilities()
    ]
    return attach_branding({"success": True, "data": {"capabilities": capabilities}})


@app.post("/api/v1/capabilities/{capability_id}")
def execute_prediction_capability(capability_id: str, payload: dict[str, Any]):
    """执行已生产化的独立 capability。"""
    try:
        result = CapabilityExecutor().execute(CapabilityInput(capability_id=capability_id, payload=payload))
        return attach_branding(
            {
                "success": True,
                "capabilityId": result.capability_id,
                "status": result.status,
                "reportProfile": result.report_profile,
                "data": result.data,
                "evidence": result.evidence,
                "risk": result.risk,
                "meta": {"calculatedAt": now_cn().isoformat()},
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


def _parse_bazi_request(req: BaziRequest) -> tuple[datetime, float, float]:
    birth_dt = datetime.strptime(f"{req.birthDate} {req.birthTime}", "%Y-%m-%d %H:%M:%S")
    if not req.birthPlace:
        raise HTTPException(status_code=400, detail="birthPlace 必填（经纬度用于真太阳时/风水/占星）")
    return birth_dt, req.birthPlace.longitude, req.birthPlace.latitude


def _build_bazi_data(result: dict, *, birth_dt: datetime, true_solar_time: datetime | None, timezone: str) -> BaziData:
    major_fortune = dict(result.get("majorFortune", {}))
    major_fortune["pillars"] = [
        {
            **pillar,
            "year": pillar.get("year", pillar.get("startYear")),
        }
        for pillar in major_fortune.get("pillars", [])
        if isinstance(pillar, dict)
    ]

    tz = ZoneInfo(timezone)
    return BaziData(
        timeInfo=TimeInfo(
            inputTime=birth_dt.replace(tzinfo=tz).isoformat(),
            trueSolarTime=true_solar_time.replace(tzinfo=tz).isoformat() if true_solar_time else None,
            lunarDate=f"{result['fourPillars']['year']['fullName']}年",
            solarTerm="",
        ),
        fourPillars=result["fourPillars"],
        hiddenStems=result.get("hiddenStems", {}),
        tenGods=result.get("tenGods", {}),
        fiveElements=result.get("fiveElements", {}),
        dayMaster=result.get("dayMaster", {}),
        majorFortune=major_fortune,
        annualFortune=result.get("annualFortune", []),
        voidBranches=result.get("voidInfo", {}),
    )


def _calculate_bazi_raw(req: BaziRequest, *, report_system: str = "bazi") -> tuple[dict, BaziCalculator, datetime]:
    birth_dt, longitude, latitude = _parse_bazi_request(req)
    report_hide = build_report_hide(report_system)
    display_birth_place = public_birth_place(req.birthPlace.name)
    calculator = BaziCalculator(
        birth_dt,
        req.gender,
        longitude,
        latitude=latitude,
        name=req.name,
        birth_place=display_birth_place,
        use_true_solar_time=req.options.useTrueSolarTime,
    )
    result = calculator.calculate(hide=report_hide)
    return result, calculator, birth_dt


def _calculate_ziwei_capability(req: BaziRequest) -> dict[str, Any]:
    """使用统一 capability 执行紫微，不再从八字扩展链拼装 Markdown 数据。"""
    birth_dt, longitude, latitude = _parse_bazi_request(req)
    result = CapabilityExecutor().execute(
        CapabilityInput(
            capability_id="ziwei",
            payload={
                "birthDateTime": birth_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "gender": req.gender,
                "longitude": longitude,
                "latitude": latitude,
                "birthPlace": req.birthPlace.name,
                "name": req.name,
                "useTrueSolarTime": req.options.useTrueSolarTime,
            },
        )
    )
    return result.data


@app.post("/api/v1/bazi/simple")
def calculate_bazi_simple(req: BaziRequest):
    """简化八字计算 - 直接返回原始结果"""
    try:
        result, _calculator, _birth_dt = _calculate_bazi_raw(req, report_system="bazi")

        return attach_branding({"success": True, "data": result})
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("简化八字计算失败")
        raise HTTPException(status_code=500, detail="服务器内部错误") from e


@app.post("/api/v1/bazi/pure-analysis")
def calculate_bazi_pure_analysis(req: BaziRequest):
    """纯命理分析 - 仅返回配置约束下的核心字段。"""
    try:
        birth_dt, longitude, latitude = _parse_bazi_request(req)
        payload = PureAnalysisInput(
            birth_dt=birth_dt,
            gender=req.gender,
            longitude=longitude,
            latitude=latitude,
            name=req.name,
            birth_place=req.birthPlace.name,
            use_true_solar_time=req.options.useTrueSolarTime,
        )
        result = calculate_pure_analysis(payload)
        return attach_branding(
            {
                "success": True,
                "data": result,
                "meta": {
                    "calculatedAt": now_cn().isoformat(),
                    "profile": "pure_analysis",
                },
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("纯分析计算失败")
        raise HTTPException(status_code=500, detail="服务器内部错误") from e


@app.post("/api/v1/bazi/calculate", response_model=BaziResponse)
def calculate_bazi(
    req: BaziRequest,
    user_id: str | None = None,
    x_fatecat_api_key: str | None = Header(default=None, alias="X-FateCat-API-Key"),
    authorization: str | None = Header(default=None),
):
    """计算八字排盘"""
    try:
        if user_id:
            principal = _require_record_access(x_fatecat_api_key, authorization)
            _require_owner_or_admin(principal, user_id)
        result, calculator, birth_dt = _calculate_bazi_raw(req, report_system="bazi")

        ts_dt = calculator.true_solar_time if req.options.useTrueSolarTime else birth_dt
        data = _build_bazi_data(
            result,
            birth_dt=birth_dt,
            true_solar_time=ts_dt if req.options.useTrueSolarTime else None,
            timezone=req.birthPlace.timezone,
        )

        # 保存到数据库
        record_id = None
        if user_id:
            record_id = db.save_record(
                user_id=user_id,
                biz_type="bazi",
                name=req.name,
                gender=req.gender,
                calendar_type=req.options.calendarType,
                birth_date=req.birthDate,
                birth_time=req.birthTime,
                birth_place=req.birthPlace.name,
                longitude=req.birthPlace.longitude,
                latitude=req.birthPlace.latitude,
                dst=0,
                true_solar=1 if req.options.useTrueSolarTime else 0,
                early_zi=1 if req.options.midnightMode == "early" else 0,
                biz_data={"input": req.model_dump(), "result": result},
            )

        return BaziResponse(
            disclaimer=_disclaimer_model(),
            success=True,
            data=data,
            meta=Meta(calculatedAt=now_cn().isoformat(), recordId=record_id),
            branding=_branding_model(),
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("八字 API 计算失败")
        return BaziResponse(
            disclaimer=_disclaimer_model(),
            success=False,
            error="八字计算失败",
            meta=Meta(calculatedAt=now_cn().isoformat()),
            branding=_branding_model(),
        )


@app.post("/api/v1/report/markdown")
def generate_markdown_report(req: BaziRequest):
    """生成指定体系的 Markdown 报告。"""
    try:
        report_system = normalize_report_system(req.options.reportSystem)
        if report_system == "ziwei":
            result = _calculate_ziwei_capability(req)
        else:
            result, _calculator, _birth_dt = _calculate_bazi_raw(req, report_system=report_system)
        report_hide = build_report_hide(report_system)
        markdown = generate_full_report(result, hide=report_hide, report_system=report_system)
        return attach_branding(
            {
                "success": True,
                "data": {
                    "reportSystem": report_system,
                    "markdown": markdown,
                },
                "meta": {"calculatedAt": now_cn().isoformat()},
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Markdown 报告生成失败")
        raise HTTPException(status_code=500, detail="服务器内部错误") from e


@app.post("/api/v1/liuyao/factor", response_model=LiuyaoFactorResponse)
def calculate_liuyao_factor(req: LiuyaoFactorRequest):
    """六爻量化因子 - 统一输出结构"""
    try:
        factor = generate_factor(
            item=req.item,
            timestamp=req.timestamp,
            method=req.method,
            seed=req.seed,
            cnts=req.cnts,
            cycle_hint=req.cycleHint,
        )
        data = LiuyaoFactorData(**factor.to_dict())
        return LiuyaoFactorResponse(
            disclaimer=_disclaimer_model(),
            success=True,
            data=data,
            meta=Meta(calculatedAt=now_cn().isoformat(), algorithm="liuyao-divicast", version="1.0.0"),
            branding=_branding_model(),
        )
    except Exception:
        logger.exception("六爻因子计算失败")
        return LiuyaoFactorResponse(
            disclaimer=_disclaimer_model(),
            success=False,
            error="六爻因子计算失败",
            meta=Meta(calculatedAt=now_cn().isoformat(), algorithm="liuyao-divicast", version="1.0.0"),
            branding=_branding_model(),
        )


@app.get("/api/v1/records/{record_id}")
def get_record(
    record_id: int,
    x_fatecat_api_key: str | None = Header(default=None, alias="X-FateCat-API-Key"),
    authorization: str | None = Header(default=None),
):
    """获取记录"""
    principal = _require_record_access(x_fatecat_api_key, authorization)
    record = db.get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    _require_owner_or_admin(principal, str(record["userId"]))
    return attach_branding({"success": True, "data": record})


@app.get("/api/v1/user/{user_id}/records")
def get_user_records(
    user_id: str,
    biz_type: str = None,
    limit: int = Query(default=10, ge=1, le=100),
    x_fatecat_api_key: str | None = Header(default=None, alias="X-FateCat-API-Key"),
    authorization: str | None = Header(default=None),
):
    """获取用户记录"""
    principal = _require_record_access(x_fatecat_api_key, authorization)
    _require_owner_or_admin(principal, user_id)
    records = db.get_user_records(user_id, biz_type, limit)
    return attach_branding({"success": True, "data": records, "total": len(records)})


@app.delete("/api/v1/records/{record_id}")
def delete_record(
    record_id: int,
    x_fatecat_api_key: str | None = Header(default=None, alias="X-FateCat-API-Key"),
    authorization: str | None = Header(default=None),
):
    """删除记录"""
    principal = _require_record_access(x_fatecat_api_key, authorization)
    record = db.get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    _require_owner_or_admin(principal, str(record["userId"]))
    if db.delete_record(record_id):
        return attach_branding({"success": True})
    raise HTTPException(status_code=404, detail="Not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=SERVICE_HOST, port=SERVICE_PORT)
