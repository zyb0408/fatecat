from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from fastapi.testclient import TestClient
from fate_core.capabilities import CapabilityExecutor, CapabilityInput
from fate_core.usecases import PureAnalysisInput, calculate_pure_analysis
from main import app

ROOT = Path(__file__).resolve().parents[1]
FATE_DIR = ROOT / "assets" / "fate"


def _rule_depth_registry() -> dict:
    return json.loads((FATE_DIR / "rule_depth_registry.json").read_text(encoding="utf-8"))


def _classics_rule_ids() -> set[str]:
    data = json.loads((FATE_DIR / "classics_rule_index.json").read_text(encoding="utf-8"))
    return {rule["id"] for rule in data["rules"]}


def _bazi_result() -> dict:
    return calculate_pure_analysis(
        PureAnalysisInput(
            birth_dt=datetime(1990, 1, 1, 8, 0, 0),
            gender="male",
            longitude=116.4074,
            latitude=39.9042,
            birth_place="北京",
            name="测试样本",
            use_true_solar_time=True,
        )
    )


def test_rule_depth_registry_is_traceable_and_bounded():
    registry = _rule_depth_registry()
    classics = _classics_rule_ids()
    rules = registry["rules"]

    assert registry["copyrightBoundary"] == "summary_only_no_commercial_copy"
    assert {rule["system"] for rule in rules} == {"bazi", "ziwei"}
    assert len([rule for rule in rules if rule["system"] == "bazi"]) >= 6
    assert len([rule for rule in rules if rule["system"] == "ziwei"]) >= 6

    for rule in rules:
        assert rule["id"] in classics
        assert rule["evidenceFields"]
        assert rule["conditions"]
        assert rule["conflictPolicy"]
        assert rule["riskBoundary"]
        assert set(rule["sourceRuleIds"]) <= classics


def test_bazi_rule_depth_outputs_rule_applications_and_evidence():
    result = _bazi_result()
    depth = result["baziRuleDepth"]

    assert depth["system"] == "bazi"
    assert depth["registryVersion"]
    assert len(depth["appliedRules"]) >= 6
    assert {item["ruleId"] for item in depth["appliedRules"]} >= {
        "bazi.depth.strength.month_root_transparency",
        "bazi.depth.pattern.establishment",
        "bazi.depth.yongshen.strategy_matrix",
        "bazi.depth.fortune.trigger_chain",
        "bazi.depth.auxiliary.boundary_guard",
    }
    assert depth["conflictMatrix"]
    assert set(depth["sourceRuleIds"]) <= _classics_rule_ids()

    evidence = result["analysisEvidence"]["items"]["baziRuleDepth"]
    assert evidence["conclusion"]["appliedRuleCount"] == len(depth["appliedRules"])
    assert "baziRuleDepth.appliedRules" in evidence["basis"]
    assert set(evidence["ruleIds"]) <= _classics_rule_ids()


def test_ziwei_rule_depth_outputs_rule_applications_and_evidence():
    result = CapabilityExecutor().execute(
        CapabilityInput(
            capability_id="ziwei",
            payload={
                "birthDateTime": "1990-01-01 08:00:00",
                "gender": "男",
                "longitude": 116.4074,
                "latitude": 39.9042,
                "birthPlace": "北京",
                "name": "测试样本",
            },
        )
    )
    data = result.data
    depth = data["ziweiRuleDepth"]

    assert depth["system"] == "ziwei"
    assert depth["registryVersion"]
    assert len(depth["appliedRules"]) >= 6
    assert {item["ruleId"] for item in depth["appliedRules"]} >= {
        "ziwei.depth.star.brightness_weight",
        "ziwei.depth.palace.triad_focus",
        "ziwei.depth.mutagen.scope_chain",
        "ziwei.depth.pattern.condition_matrix",
        "ziwei.depth.fortune.linkage_chain",
    }
    assert result.evidence["coverage"]["hasRuleDepth"] is True
    assert set(result.evidence["items"]["ruleDepth"]["ruleIds"]) <= _classics_rule_ids()


def test_rule_depth_is_available_from_api_and_web_without_frontend_recalculation():
    client = TestClient(app)
    bazi_api = client.post(
        "/api/v1/capabilities/bazi",
        json={
            "birthDateTime": "1990-01-01 08:00:00",
            "gender": "男",
            "longitude": 116.4074,
            "latitude": 39.9042,
            "birthPlace": "北京",
            "name": "测试样本",
        },
    )
    assert bazi_api.status_code == 200
    assert bazi_api.json()["data"]["baziRuleDepth"]["appliedRules"]

    ziwei_api = client.post(
        "/api/v1/capabilities/ziwei",
        json={
            "birthDateTime": "1990-01-01 08:00:00",
            "gender": "男",
            "longitude": 116.4074,
            "latitude": 39.9042,
            "birthPlace": "北京",
            "name": "测试样本",
        },
    )
    assert ziwei_api.status_code == 200
    assert ziwei_api.json()["data"]["ziweiRuleDepth"]["appliedRules"]

    bazi_web = client.get(
        "/web",
        params={
            "birthDate": "1990-01-01",
            "birthTime": "08:00",
            "birthPlace": "北京",
            "gender": "male",
            "name": "测试样本",
        },
    )
    assert bazi_web.status_code == 200
    assert "规则深度 / 冲突策略" in bazi_web.text
    assert "bazi.depth.yongshen.strategy_matrix" in bazi_web.text

    ziwei_web = client.get(
        "/web",
        params={
            "birthDate": "1990-01-01",
            "birthTime": "08:00",
            "birthPlace": "上海",
            "gender": "male",
            "name": "测试样本",
            "reportSystem": "ziwei",
        },
    )
    assert ziwei_web.status_code == 200
    assert "规则深度 / 冲突策略" in ziwei_web.text
    assert "ziwei.depth.mutagen.scope_chain" in ziwei_web.text
    assert "上海" not in ziwei_web.text
