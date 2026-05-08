from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from fate_core.adapters import LegacyBaziInput
from fate_core.kernel import project_by_profile
from fate_core.providers import (
    build_base_chart_section,
    build_classical_section,
    build_fortune_section,
    build_pure_analysis_runtime,
)


@dataclass(frozen=True)
class PureAnalysisInput:
    """纯命理分析用例输入。"""

    birth_dt: datetime
    gender: str
    longitude: float
    latitude: float
    name: str | None = None
    birth_place: str = ""
    use_true_solar_time: bool = True


def _first_non_empty(*values: Any) -> Any:
    for value in values:
        if value not in (None, ""):
            return value
    return None


def _parse_bool(value: Any, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "y", "on", "是"}:
        return True
    if normalized in {"0", "false", "no", "n", "off", "否"}:
        return False
    raise ValueError(f"无法解析布尔值: {value}")


def parse_datetime(value: str) -> datetime:
    """解析出生时间，兼容 CLI/API 常见输入格式。"""
    normalized = value.strip()
    if not normalized:
        raise ValueError("birthDateTime 不能为空")
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
        return parsed.replace(tzinfo=None) if parsed.tzinfo else parsed
    except ValueError:
        pass
    for time_format in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M:%S", "%Y/%m/%d %H:%M"):
        try:
            return datetime.strptime(normalized, time_format)
        except ValueError:
            continue
    raise ValueError(f"无法解析出生时间: {value}")


def normalize_gender(gender: str) -> str:
    """把人类输入统一成底层计算器使用的性别枚举。"""
    normalized = str(gender).strip().lower()
    if normalized in {"male", "m", "man", "boy", "男", "男性", "乾", "乾造"}:
        return "male"
    if normalized in {"female", "f", "woman", "girl", "女", "女性", "坤", "坤造"}:
        return "female"
    raise ValueError(f"无法识别性别: {gender}")


def normalize_pure_analysis_payload(raw_payload: dict[str, Any]) -> dict[str, Any]:
    """把 CLI/API/Capability 输入统一成纯分析用例字段。"""
    birth_place_value = raw_payload.get("birthPlace")
    birth_place_object: dict[str, Any] = birth_place_value if isinstance(birth_place_value, dict) else {}
    raw_options = raw_payload.get("options")
    options: dict[str, Any] = raw_options if isinstance(raw_options, dict) else {}

    birth_datetime = _first_non_empty(
        raw_payload.get("birthDateTime"),
        raw_payload.get("birth_datetime"),
        raw_payload.get("birth_dt"),
        raw_payload.get("datetime"),
    )
    if not birth_datetime and raw_payload.get("birthDate") and raw_payload.get("birthTime"):
        birth_datetime = f"{raw_payload['birthDate']} {raw_payload['birthTime']}"

    longitude = _first_non_empty(
        raw_payload.get("longitude"),
        raw_payload.get("lng"),
        birth_place_object.get("longitude"),
        birth_place_object.get("lng"),
    )
    latitude = _first_non_empty(
        raw_payload.get("latitude"),
        raw_payload.get("lat"),
        birth_place_object.get("latitude"),
        birth_place_object.get("lat"),
    )
    birth_place_name = _first_non_empty(
        raw_payload.get("birth_place"),
        raw_payload.get("birthPlaceName"),
        birth_place_value if isinstance(birth_place_value, str) else None,
        birth_place_object.get("name"),
    )
    use_true_solar_time = _first_non_empty(
        raw_payload.get("useTrueSolarTime"),
        raw_payload.get("use_true_solar_time"),
        options.get("useTrueSolarTime"),
    )

    normalized = {
        "birthDateTime": birth_datetime,
        "gender": _first_non_empty(raw_payload.get("gender"), raw_payload.get("sex")),
        "longitude": longitude,
        "latitude": latitude,
        "name": raw_payload.get("name"),
        "birthPlace": birth_place_name or "",
        "useTrueSolarTime": _parse_bool(use_true_solar_time, default=True),
    }
    missing = [
        field for field in ("birthDateTime", "gender", "longitude", "latitude") if normalized[field] in (None, "")
    ]
    if missing:
        raise ValueError(f"缺少必填字段: {', '.join(missing)}")
    normalized["longitude"] = float(normalized["longitude"])
    normalized["latitude"] = float(normalized["latitude"])
    normalized["gender"] = normalize_gender(str(normalized["gender"]))
    return normalized


def build_pure_analysis_input_from_payload(raw_payload: dict[str, Any]) -> PureAnalysisInput:
    """从统一 payload 构造纯分析输入。"""
    normalized = normalize_pure_analysis_payload(raw_payload)
    return PureAnalysisInput(
        birth_dt=parse_datetime(str(normalized["birthDateTime"])),
        gender=str(normalized["gender"]),
        longitude=normalized["longitude"],
        latitude=normalized["latitude"],
        name=normalized["name"],
        birth_place=str(normalized["birthPlace"]),
        use_true_solar_time=normalized["useTrueSolarTime"],
    )


def calculate_pure_analysis(payload: PureAnalysisInput) -> dict[str, Any]:
    """计算纯命理分析字段集合。"""
    runtime = build_pure_analysis_runtime(
        LegacyBaziInput(
            birth_dt=payload.birth_dt,
            gender=normalize_gender(payload.gender),
            longitude=payload.longitude,
            latitude=payload.latitude,
            name=payload.name,
            birth_place=payload.birth_place,
            use_true_solar_time=payload.use_true_solar_time,
        )
    )
    raw = {}
    raw.update(build_base_chart_section(runtime))
    raw.update(build_fortune_section(runtime))
    raw.update(build_classical_section(runtime))
    raw["analysisEvidence"] = runtime.calculator._calc_analysis_evidence(
        four_pillars=runtime.four_pillars,
        hidden_stems=runtime.hidden_stems,
        day_master=raw.get("dayMaster", {}),
        wuxing_scores=raw.get("wuxingScores", {}),
        geju=raw.get("geju", {}),
        yongshen=raw.get("yongShen", {}),
        ganzhi_relations=raw.get("ganzhiRelations", {}),
        branch_relations=raw.get("branchRelations", {}),
        spirits=raw.get("spiritsFull", {}),
        bone_weight=raw.get("boneWeight", {}),
    )
    projected = project_by_profile(raw, "pure_analysis")
    translated = runtime.calculator._translate_to_chinese(projected)
    safe_result = runtime.calculator._json_safe(translated)
    if not isinstance(safe_result, dict):
        raise RuntimeError("纯分析结果必须是 JSON 对象")
    return dict(safe_result)
