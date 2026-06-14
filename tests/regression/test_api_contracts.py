from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
TELEGRAM_SRC = ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
FATE_CORE_SRC = ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"

if str(TELEGRAM_SRC) not in sys.path:
    sys.path.insert(0, str(TELEGRAM_SRC))
if str(FATE_CORE_SRC) not in sys.path:
    sys.path.insert(0, str(FATE_CORE_SRC))

import main  # noqa: E402
from main import app  # noqa: E402


def _payload() -> dict:
    return {
        "name": "测试样本",
        "gender": "male",
        "birthDate": "1990-01-01",
        "birthTime": "08:00:00",
        "birthPlace": {
            "name": "北京市",
            "longitude": 116.4074,
            "latitude": 39.9042,
            "timezone": "Asia/Shanghai",
        },
        "options": {
            "useTrueSolarTime": True,
            "daylightSaving": "auto",
            "midnightMode": "early",
            "calendarType": "solar",
        },
    }


def test_pure_analysis_api_returns_success():
    response = TestClient(app).post("/api/v1/bazi/pure-analysis", json=_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["input"]["gender"] == "男"
    assert body["data"]["meta"]["genderCn"] == "乾造(男)"
    assert "jianChu" not in body["data"]


def test_health_adds_public_service_security_headers():
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert "frame-ancestors 'none'" in response.headers["content-security-policy"]
    assert response.headers["x-request-id"]


def test_ready_and_metrics_endpoints_are_available():
    client = TestClient(app)
    ready_response = client.get("/ready")

    assert ready_response.status_code == 200
    assert ready_response.json()["status"] == "ready"

    metrics_response = client.get("/metrics")
    assert metrics_response.status_code == 200
    assert metrics_response.headers["content-type"].startswith("text/plain")
    assert "fatecat_requests_total" in metrics_response.text
    assert "fatecat_inflight_requests" in metrics_response.text


def test_request_body_limit_rejects_oversized_payload(monkeypatch):
    monkeypatch.setattr(main, "MAX_REQUEST_BYTES", 32)

    response = TestClient(app).post("/api/v1/bazi/pure-analysis", json=_payload())

    assert response.status_code == 413
    assert response.json()["error"] == "请求体过大"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["x-request-id"]


def test_rate_limit_rejects_excess_requests(monkeypatch):
    monkeypatch.setattr(main, "RATE_LIMIT_PER_MINUTE", 1)
    main._rate_limit_windows.clear()

    client = TestClient(app)
    first_response = client.get("/api/v1/report/systems")
    second_response = client.get("/api/v1/report/systems")

    main._rate_limit_windows.clear()
    assert first_response.status_code == 200
    assert second_response.status_code == 429
    assert second_response.json()["error"] == "请求过于频繁"
    assert second_response.headers["retry-after"]
    assert second_response.headers["x-content-type-options"] == "nosniff"
    assert second_response.headers["x-frame-options"] == "DENY"
    assert second_response.headers["x-request-id"]


def test_simple_api_does_not_return_retired_jianchu_field():
    response = TestClient(app).post("/api/v1/bazi/simple", json=_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "jianChu" not in body["data"]


def test_calculate_api_returns_success_with_record_id(monkeypatch):
    saved = {}

    def fake_save_record(**kwargs):
        saved.update(kwargs)
        return 42

    monkeypatch.setattr("main.db.save_record", fake_save_record)
    monkeypatch.setattr(main, "API_TOKEN", "test-token")

    response = TestClient(app).post(
        "/api/v1/bazi/calculate?user_id=u1",
        json=_payload(),
        headers={"X-FateCat-API-Key": "test-token"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["meta"]["recordId"] == 42
    assert saved["gender"] == "male"
    assert saved["birth_place"] == "北京市"


def test_user_token_can_write_only_own_record(monkeypatch):
    saved = {}

    def fake_save_record(**kwargs):
        saved.update(kwargs)
        return 43

    monkeypatch.setattr("main.db.save_record", fake_save_record)
    monkeypatch.setattr(main, "API_TOKEN", "")
    monkeypatch.setenv("FATE_API_USER_TOKENS", "u1:user-token")

    own_response = TestClient(app).post(
        "/api/v1/bazi/calculate?user_id=u1",
        json=_payload(),
        headers={"X-FateCat-API-Key": "user-token"},
    )
    other_response = TestClient(app).post(
        "/api/v1/bazi/calculate?user_id=u2",
        json=_payload(),
        headers={"X-FateCat-API-Key": "user-token"},
    )

    assert own_response.status_code == 200
    assert own_response.json()["meta"]["recordId"] == 43
    assert saved["user_id"] == "u1"
    assert other_response.status_code == 403
    assert other_response.json()["error"] == "无权访问该记录"


def test_calculate_api_rejects_record_write_without_token(monkeypatch):
    monkeypatch.setattr(main, "API_TOKEN", "test-token")

    response = TestClient(app).post("/api/v1/bazi/calculate?user_id=u1", json=_payload())

    assert response.status_code == 403
    body = response.json()
    assert body["success"] is False
    assert body["error"] == "未授权"


def test_record_read_requires_api_token(monkeypatch):
    monkeypatch.setattr(main, "API_TOKEN", "test-token")

    response = TestClient(app).get("/api/v1/records/1")

    assert response.status_code == 403
    assert response.json()["error"] == "未授权"


def test_record_interfaces_can_be_disabled(monkeypatch):
    monkeypatch.setenv("FATE_RECORDS_ENABLED", "false")
    monkeypatch.setattr(main, "API_TOKEN", "admin-token")

    response = TestClient(app).get("/api/v1/records/1", headers={"X-FateCat-API-Key": "admin-token"})

    assert response.status_code == 403
    assert response.json()["error"] == "记录接口未启用"


def test_user_token_cannot_read_other_user_record(monkeypatch):
    monkeypatch.setattr(main, "API_TOKEN", "")
    monkeypatch.setenv("FATE_API_USER_TOKENS", "u1:user-token")
    monkeypatch.setattr(
        "main.db.get_record",
        lambda _record_id: {
            "id": 1,
            "userId": "u2",
            "bizType": "bazi",
            "input": {},
            "bizData": {},
            "createdAt": "2026-05-06T00:00:00+08:00",
        },
    )

    response = TestClient(app).get("/api/v1/records/1", headers={"X-FateCat-API-Key": "user-token"})

    assert response.status_code == 403
    assert response.json()["error"] == "无权访问该记录"


def test_admin_token_can_read_any_record(monkeypatch):
    monkeypatch.setattr(main, "API_TOKEN", "admin-token")
    monkeypatch.setattr(
        "main.db.get_record",
        lambda _record_id: {
            "id": 1,
            "userId": "u2",
            "bizType": "bazi",
            "input": {},
            "bizData": {},
            "createdAt": "2026-05-06T00:00:00+08:00",
        },
    )

    response = TestClient(app).get("/api/v1/records/1", headers={"Authorization": "Bearer admin-token"})

    assert response.status_code == 200
    assert response.json()["data"]["userId"] == "u2"


def test_user_records_limit_is_bounded(monkeypatch):
    monkeypatch.setattr(main, "API_TOKEN", "admin-token")

    response = TestClient(app).get(
        "/api/v1/user/u1/records?limit=-1",
        headers={"X-FateCat-API-Key": "admin-token"},
    )

    assert response.status_code == 422
    assert response.json()["error"] == "请求参数无效"


def test_markdown_report_api_selects_ziwei_without_bazi_blocks():
    payload = _payload()
    payload["options"]["reportSystem"] = "ziwei"

    response = TestClient(app).post("/api/v1/report/markdown", json=payload)

    assert response.status_code == 200
    body = response.json()
    markdown = body["data"]["markdown"]
    assert body["data"]["reportSystem"] == "ziwei"
    assert "# 紫微斗数报告：测试样本" in markdown
    assert "## 紫微斗数" in markdown
    assert "### 入盘依据" in markdown
    assert "### 命宫与身宫" in markdown
    assert "## 紫微结构解读（依据版）" in markdown
    assert "### 主星组合" in markdown
    assert "### 三方四正" in markdown
    assert "### 四化落宫" in markdown
    assert "### 大限/流年联动" in markdown
    assert "## 紫微基础" not in markdown
    assert "## 八字排盘详情" not in markdown


def test_markdown_report_api_rejects_retired_jianchu_system():
    payload = _payload()
    payload["options"]["reportSystem"] = "jianchu"

    response = TestClient(app).post("/api/v1/report/markdown", json=payload)

    assert response.status_code == 422


def test_markdown_report_api_rejects_retired_bone_system():
    payload = _payload()
    payload["options"]["reportSystem"] = "bone"

    response = TestClient(app).post("/api/v1/report/markdown", json=payload)

    assert response.status_code == 422


def test_report_systems_api_lists_enabled_and_planned_systems():
    response = TestClient(app).get("/api/v1/report/systems")

    assert response.status_code == 200
    body = response.json()
    systems = {item["id"]: item for item in body["data"]["systems"]}
    assert systems["bazi"]["enabled"] is True
    assert systems["ziwei"]["enabled"] is True
    assert systems["huangli"]["enabled"] is False
    assert systems["meihua"]["status"] == "production"
    assert systems["meihua"]["enabled"] is False
    assert systems["liuyao"]["status"] == "planned"
    assert systems["fengshui"]["group"] == "未来功能"


def test_capabilities_api_lists_almanac_as_standalone_production():
    response = TestClient(app).get("/api/v1/capabilities")

    assert response.status_code == 200
    body = response.json()
    capabilities = {item["capabilityId"]: item for item in body["data"]["capabilities"]}
    assert capabilities["bazi"]["defaultVisibility"] == "default"
    assert capabilities["almanac"]["status"] == "production"
    assert capabilities["almanac"]["defaultVisibility"] == "standalone"
    assert capabilities["ziwei"]["status"] == "production"
    assert capabilities["ziwei"]["defaultVisibility"] == "standalone"
    assert capabilities["meihua"]["status"] == "production"
    assert capabilities["meihua"]["defaultVisibility"] == "standalone"


def test_capability_api_executes_almanac_without_enabling_markdown_system():
    response = TestClient(app).post(
        "/api/v1/capabilities/almanac",
        json={
            "dateRange": {"start": "2026-05-08", "end": "2026-05-08"},
            "eventType": "出行",
            "place": "北京",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["capabilityId"] == "almanac"
    assert body["reportProfile"] == "almanac"
    assert body["data"]["dateRange"]["days"] == 1
    assert body["data"]["days"][0]["timeSlots"]
    assert len(body["data"]["days"][0]["timeSlots"]) == 12
    assert body["data"]["days"][0]["scoreBreakdown"]
    assert body["evidence"]["source"] == "lunar-python"


def test_capability_api_executes_meihua_without_enabling_markdown_system():
    response = TestClient(app).post(
        "/api/v1/capabilities/meihua",
        json={
            "question": "测试问题能否推进",
            "castMethod": "number",
            "castValue": "3,8,6",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["capabilityId"] == "meihua"
    assert body["reportProfile"] == "meihua"
    assert body["data"]["hexagrams"]["movingLine"] == 5
    assert body["evidence"]["items"]["cast"]["ruleIds"] == ["meihua.number_cast"]


def test_markdown_report_hides_non_beijing_birth_place():
    payload = _payload()
    payload["birthPlace"] = {
        "name": "上海市",
        "longitude": 121.4737,
        "latitude": 31.2304,
        "timezone": "Asia/Shanghai",
    }

    response = TestClient(app).post("/api/v1/report/markdown", json=payload)

    assert response.status_code == 200
    markdown = response.json()["data"]["markdown"]
    assert "上海" not in markdown
    assert "已填写（非北京地区已隐藏）" in markdown
