from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from fate_core.capabilities import CapabilityExecutor, CapabilityInput
from fate_core.usecases import PureAnalysisInput, calculate_pure_analysis
from main import app

ROOT = Path(__file__).resolve().parents[2]
FATE_DIR = ROOT / "contracts" / "fate"
DATA_DIR = ROOT / "domains" / "fate-analysis" / "data-products"
BAZI_RULE_DEPTH_FIXTURE = DATA_DIR / "bazi" / "golden" / "rule_depth_cases.json"
ZIWEI_RULE_DEPTH_FIXTURE = DATA_DIR / "ziwei" / "golden" / "rule_depth_cases.json"


def _rule_depth_registry() -> dict:
    return json.loads((FATE_DIR / "rule_depth_registry.json").read_text(encoding="utf-8"))


def _classics_rule_ids() -> set[str]:
    data = json.loads((FATE_DIR / "classics_rule_index.json").read_text(encoding="utf-8"))
    return {rule["id"] for rule in data["rules"]}


def _rule_depth_rules() -> dict[str, dict]:
    return {rule["id"]: rule for rule in _rule_depth_registry()["rules"]}


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


def _run_bazi_case(case: dict) -> dict:
    payload = case["input"]
    return calculate_pure_analysis(
        PureAnalysisInput(
            birth_dt=datetime.strptime(payload["birthDateTime"], "%Y-%m-%d %H:%M:%S"),
            gender=payload["gender"],
            longitude=float(payload["longitude"]),
            latitude=float(payload["latitude"]),
            birth_place=payload.get("birthPlace", ""),
            name="测试样本",
            use_true_solar_time=True,
        )
    )


def _pillar_names(result: dict) -> dict[str, str]:
    return {name: result["fourPillars"][name]["fullName"] for name in ["year", "month", "day", "hour"]}


def test_rule_depth_registry_is_traceable_and_bounded():
    registry = _rule_depth_registry()
    classics = _classics_rule_ids()
    rules = registry["rules"]

    assert registry["copyrightBoundary"] == "summary_only_no_commercial_copy"
    assert {rule["system"] for rule in rules} == {"bazi", "ziwei"}
    assert len([rule for rule in rules if rule["system"] == "bazi"]) >= 22
    assert len([rule for rule in rules if rule["system"] == "ziwei"]) >= 22

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
    assert len(depth["appliedRules"]) >= 22
    assert {item["ruleId"] for item in depth["appliedRules"]} >= {
        "bazi.depth.strength.month_root_transparency",
        "bazi.depth.pattern.establishment",
        "bazi.depth.pattern.regular_vs_special",
        "bazi.depth.pattern.special_pattern_checklist",
        "bazi.depth.pattern.finance_official_seal_food_matrix",
        "bazi.depth.yongshen.strategy_matrix",
        "bazi.depth.yongshen.tiaohou_priority",
        "bazi.depth.yongshen.climate_detail_matrix",
        "bazi.depth.tengod.structure_profile",
        "bazi.depth.tengod.overlap_profile",
        "bazi.depth.tengod.role_family_matrix",
        "bazi.depth.climate.seasonal_adjustment",
        "bazi.depth.relation.combine_transform_guard",
        "bazi.depth.relation.punishment_harm_break_matrix",
        "bazi.depth.fortune.trigger_chain",
        "bazi.depth.fortune.decade_year_month_order",
        "bazi.depth.fortune.month_trigger",
        "bazi.depth.statement.combination_boundary",
        "bazi.depth.statement.narrative_markdown",
        "bazi.depth.auxiliary.boundary_guard",
    }
    assert depth["conflictMatrix"]
    assert depth["conflictResolution"]["primaryRuleIds"]
    assert depth["conflictResolution"]["conflicts"]
    assert all(item["explanation"] for item in depth["conflictResolution"]["conflicts"])
    assert all(item["type"] and item["discounts"] is not None for item in depth["conflictResolution"]["conflicts"])
    assert all(item["counterEvidence"] is not None for item in depth["conflictResolution"]["conflicts"])
    assert depth["weightProfile"]["totalWeight"] > 0
    assert depth["weightProfile"]["weightedConfidence"] > 0
    assert depth["combinationStatements"]
    assert all(item["ruleIds"] and item["riskBoundary"] for item in depth["combinationStatements"])
    assert depth["narrativeSummary"]["format"] == "markdown"
    assert "依据：" in depth["narrativeSummary"]["markdown"]
    assert set(depth["sourceRuleIds"]) <= _classics_rule_ids()

    evidence = result["analysisEvidence"]["items"]["baziRuleDepth"]
    assert evidence["conclusion"]["appliedRuleCount"] == len(depth["appliedRules"])
    assert "baziRuleDepth.appliedRules" in evidence["basis"]
    assert set(evidence["ruleIds"]) <= _classics_rule_ids()


def test_bazi_core_evidence_items_have_trace_and_risk_boundary():
    result = _bazi_result()
    evidence_items = result["analysisEvidence"]["items"]
    required_items = {
        "dayMaster",
        "wuxingPreference",
        "pattern",
        "ganzhiRelations",
        "timePipeline",
        "solarTermBoundary",
        "patternUseGodTrace",
        "baziBenchmark",
        "baziRuleDepth",
    }

    assert required_items <= set(evidence_items)
    for item_id in required_items:
        item = evidence_items[item_id]
        assert item["ruleIds"], item_id
        assert item["sources"], item_id
        assert item["riskBoundary"], item_id


def test_bazi_gap_closure_benchmark_fields_are_structured():
    result = _bazi_result()
    benchmark = result["baziBenchmark"]

    combine = benchmark["combineTransformMatrix"]
    assert combine["schemaVersion"] == 1
    assert combine["conditionCatalog"] == [
        "paired_stems_present",
        "month_command_supports_transform_element",
        "transform_element_transparent",
        "transform_element_rooted",
        "no_direct_blocker",
    ]
    assert combine["riskBoundary"]
    for candidate in combine["candidates"]:
        assert candidate["conditions"]
        assert all("met" in condition and "evidence" in condition for condition in candidate["conditions"])
        assert candidate["status"] in {"formed_candidate", "guarded_candidate", "weak_candidate"}

    special = benchmark["patternRegistry"]["specialPatternCandidates"]
    assert {candidate["name"] for candidate in special["candidates"]} >= {
        "从格",
        "化气",
        "专旺",
        "假从",
        "从杀",
        "从财",
    }
    assert all(candidate["conditions"] and candidate["boundary"] for candidate in special["candidates"])
    assert all(candidate["status"] in {"candidate", "guarded", "not_supported"} for candidate in special["candidates"])

    decision = benchmark["yongShenDecision"]
    assert decision["primaryStrategy"]
    assert len(decision["scoredStrategies"]) == 4
    assert [item["score"] for item in decision["scoredStrategies"]] == sorted(
        [item["score"] for item in decision["scoredStrategies"]],
        reverse=True,
    )
    assert all(item["evidenceFields"] for item in decision["scoredStrategies"])

    topics = benchmark["topicProfiles"]
    assert {item["topic"] for item in topics} >= {"事业", "财运", "婚姻", "健康", "学业", "迁移"}
    assert all(item["status"] == "evidence_seed" for item in topics)
    assert all(0 <= item["score"] <= 100 and item["riskBoundary"] for item in topics)
    forbidden_profile_fields = {"statement", "prediction", "judgement", "conclusion", "advice"}
    forbidden_profile_terms = {"必然", "一定", "保证", "灾祸", "疾病", "投资建议", "医疗建议"}
    for item in topics:
        assert not (forbidden_profile_fields & set(item))
        rendered = json.dumps(item, ensure_ascii=False)
        assert not any(term in rendered for term in forbidden_profile_terms)


def test_bazi_pattern_matrix_declares_conditions_counterevidence_and_boundaries():
    rules = _rule_depth_rules()
    matrix = rules["bazi.depth.pattern.regular_vs_special"]["patternMatrix"]
    classics = _classics_rule_ids()

    assert {item["name"] for item in matrix} >= {"正格", "变格", "从格", "假从", "专旺", "化气"}
    for item in matrix:
        assert item["sourceRuleId"] in classics
        assert item["appliesWhen"]
        assert item["breaksWhen"]
        assert item["riskBoundary"]

    assert rules["bazi.depth.pattern.follow_transform_guard"]["patternMatrixRef"]
    assert rules["bazi.depth.pattern.special_pattern_checklist"]["patternMatrixRef"]


def test_bazi_combine_transform_matrix_declares_states_and_counter_conditions():
    matrix = _rule_depth_rules()["bazi.depth.relation.combine_transform_guard"]["transformStateMatrix"]

    assert {item["state"] for item in matrix} >= {
        "structural_relation",
        "transform_candidate",
        "transform_success",
        "transform_broken",
        "contested_transform",
    }
    assert {item["label"] for item in matrix} >= {"成化成立", "破化/阻隔", "争合"}
    for item in matrix:
        assert item["evidenceFields"]
        assert item["appliesWhen"]
        assert item["counterConditions"]
        assert item["riskBoundary"]


def test_bazi_yongshen_strategy_scoring_matrix_has_conflict_policy():
    matrix = _rule_depth_rules()["bazi.depth.yongshen.strategy_matrix"]["strategyScoringMatrix"]

    assert [item["strategy"] for item in matrix] == ["调候", "扶抑", "通关", "病药"]
    for item in matrix:
        assert item["appliesWhen"]
        assert item["doesNotApplyWhen"]
        assert item["scoreBasis"]
        assert item["conflictPolicy"]


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
    assert len(depth["appliedRules"]) >= 22
    assert {item["ruleId"] for item in depth["appliedRules"]} >= {
        "ziwei.depth.star.brightness_weight",
        "ziwei.depth.star.fourteen_major_coverage",
        "ziwei.depth.star.support_malefic_balance",
        "ziwei.depth.palace.triad_focus",
        "ziwei.depth.palace.life_body_triad_bridge",
        "ziwei.depth.mutagen.scope_chain",
        "ziwei.depth.mutagen.flying_layer_guard",
        "ziwei.depth.pattern.condition_matrix",
        "ziwei.depth.pattern.sha_po_lang",
        "ziwei.depth.pattern.ji_yue_tong_liang",
        "ziwei.depth.combination.major_star_context",
        "ziwei.depth.star.encyclopedia_condition",
        "ziwei.depth.mutagen.opposition_guard",
        "ziwei.depth.mutagen.lu_quan_ke_ji_balance",
        "ziwei.depth.combination.palace_mutagen_bridge",
        "ziwei.depth.palace.topic_risk_boundary",
        "ziwei.depth.fortune.linkage_chain",
        "ziwei.depth.fortune.year_month_day_hour_order",
        "ziwei.depth.statement.combination_boundary",
        "ziwei.depth.statement.narrative_markdown",
    }
    assert depth["conflictResolution"]["primaryRuleIds"]
    assert depth["conflictResolution"]["conflicts"]
    assert all(item["explanation"] for item in depth["conflictResolution"]["conflicts"])
    assert all(item["type"] and item["discounts"] is not None for item in depth["conflictResolution"]["conflicts"])
    assert all(item["counterEvidence"] is not None for item in depth["conflictResolution"]["conflicts"])
    assert depth["weightProfile"]["totalWeight"] > 0
    assert depth["weightProfile"]["weightedConfidence"] > 0
    assert depth["combinationStatements"]
    assert all(item["ruleIds"] and item["riskBoundary"] for item in depth["combinationStatements"])
    assert depth["narrativeSummary"]["format"] == "markdown"
    assert "依据：" in depth["narrativeSummary"]["markdown"]
    assert result.evidence["coverage"]["hasRuleDepth"] is True
    assert set(result.evidence["items"]["ruleDepth"]["ruleIds"]) <= _classics_rule_ids()


@pytest.mark.parametrize(
    "case",
    json.loads(BAZI_RULE_DEPTH_FIXTURE.read_text(encoding="utf-8"))["cases"],
    ids=lambda case: case["id"],
)
def test_bazi_rule_depth_golden_cases(case: dict):
    result = _run_bazi_case(case)
    expected = case["expected"]
    depth = result["baziRuleDepth"]
    emitted = {item["ruleId"] for item in depth["appliedRules"]}

    assert _pillar_names(result) == expected["fourPillars"]
    assert result["dayMaster"]["strength"] == expected["dayMasterStrength"]
    assert result["geju"]["main"] == expected["gejuMain"]
    assert len(depth["appliedRules"]) >= expected["appliedRuleCountMin"]
    assert depth["conflictResolution"]["primaryRuleIds"] == expected["primaryRuleIds"]
    assert depth["weightProfile"]["weightedConfidence"] >= expected["weightedConfidenceMin"]
    assert {item["topic"] for item in depth["combinationStatements"]} >= set(expected["combinationTopics"])
    for rule_id in expected["requiredRuleIds"]:
        assert rule_id in emitted


@pytest.mark.parametrize(
    "case",
    json.loads(ZIWEI_RULE_DEPTH_FIXTURE.read_text(encoding="utf-8"))["cases"],
    ids=lambda case: case["id"],
)
def test_ziwei_rule_depth_golden_cases(case: dict):
    result = CapabilityExecutor().execute(CapabilityInput(capability_id="ziwei", payload=case["input"])).data
    expected = case["expected"]
    depth = result["ziweiRuleDepth"]
    guards = result["ziweiGoldenGuards"]
    emitted = {item["ruleId"] for item in depth["appliedRules"]}

    assert guards["lifePalace"] == expected["lifePalace"]
    assert guards["bodyPalace"] == expected["bodyPalace"]
    assert len(depth["appliedRules"]) >= expected["appliedRuleCountMin"]
    assert depth["conflictResolution"]["primaryRuleIds"] == expected["primaryRuleIds"]
    assert depth["weightProfile"]["weightedConfidence"] >= expected["weightedConfidenceMin"]
    assert {item["topic"] for item in depth["combinationStatements"]} >= set(expected["combinationTopics"])
    for rule_id in expected["requiredRuleIds"]:
        assert rule_id in emitted


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
    assert "综合八字规则摘要" in bazi_web.text
    assert "特殊格局边界" in bazi_web.text
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
    assert "紫微斗数规则摘要" in ziwei_web.text
    assert "命身宫-三方四正" in ziwei_web.text
    assert "规则深度 / 冲突策略" in ziwei_web.text
    assert "ziwei.depth.mutagen.scope_chain" in ziwei_web.text
    assert "上海" not in ziwei_web.text
