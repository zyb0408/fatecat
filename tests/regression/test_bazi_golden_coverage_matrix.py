from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

import pytest

from fate_core.usecases import PureAnalysisInput, calculate_pure_analysis

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "domains" / "fate-analysis" / "data-products" / "bazi" / "golden" / "coverage_matrix_cases.json"


def _load_fixture() -> dict:
    with FIXTURE.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _pillar_names(result: dict) -> dict[str, str]:
    return {name: result["fourPillars"][name]["fullName"] for name in ["year", "month", "day", "hour"]}


def _run_case(case: dict) -> dict:
    payload = case["input"]
    return calculate_pure_analysis(
        PureAnalysisInput(
            birth_dt=datetime.strptime(payload["birthDateTime"], "%Y-%m-%d %H:%M:%S"),
            gender=payload["gender"],
            longitude=float(payload["longitude"]),
            latitude=float(payload["latitude"]),
            birth_place=payload.get("birthPlace", ""),
            name="测试样本",
            use_true_solar_time=bool(payload["useTrueSolarTime"]),
        )
    )


def _representative_cases(fixture: dict) -> list[dict]:
    """按 requiredTags 选择默认门禁代表集，避免退回少量手写抽样。"""
    cases = fixture["cases"]
    selected: dict[str, dict] = {}
    for tag in sorted(fixture["coverageRequirements"]["requiredTags"]):
        match = next((case for case in cases if tag in case["coverageTags"]), None)
        assert match is not None, tag
        selected[match["id"]] = match
    return list(selected.values())


def _shard_config_from_env() -> tuple[int, int]:
    total = int(os.getenv("FATECAT_GOLDEN_SHARD_TOTAL", "1"))
    index = int(os.getenv("FATECAT_GOLDEN_SHARD_INDEX", "0"))
    assert total >= 1, "FATECAT_GOLDEN_SHARD_TOTAL 必须 >= 1"
    assert 0 <= index < total, "FATECAT_GOLDEN_SHARD_INDEX 必须满足 0 <= index < total"
    return total, index


def _select_shard_cases(cases: list[dict], total: int, index: int) -> list[dict]:
    return [case for position, case in enumerate(cases) if position % total == index]


def test_bazi_golden_coverage_matrix_has_300_plus_traceable_cases():
    fixture = _load_fixture()
    cases = fixture["cases"]
    observed_tags = {tag for case in cases for tag in case["coverageTags"]}
    required_tags = set(fixture["coverageRequirements"]["requiredTags"])

    assert fixture["schemaVersion"] == 1
    assert fixture["source"] == "synthetic_anonymous_fixture"
    assert fixture["caseCount"] == len(cases)
    assert len(cases) >= fixture["coverageRequirements"]["minCaseCount"] >= 300
    assert required_tags <= observed_tags
    assert fixture["sourcePolicy"]["productionUse"] == "test_only_not_runtime_oracle"
    assert "专业格局断法" in fixture["sourcePolicy"]["riskBoundary"]

    ids = [case["id"] for case in cases]
    assert len(ids) == len(set(ids))

    for case in cases:
        assert case["source"]["type"] == "synthetic_anonymous_fixture"
        assert case["source"]["license"]
        assert case["source"]["privacy"] == "no_real_person_no_non_beijing_place"
        assert case["input"]["birthPlace"] == "北京"
        assert case["input"]["useTrueSolarTime"] is False
        assert case["coverageTags"]
        assert {"fourPillars", "dayStem", "fortuneStart", "assertionSet"} <= set(case["expected"])
        assert set(case["expected"]["fourPillars"]) == {"year", "month", "day", "hour"}
        assert all(case["expected"]["fourPillars"].values())
        assert case["expected"]["dayStem"]
        assert case["expected"]["fortuneStart"]["startDate"]
        assert case["failureExplanation"]["fourPillars"]
        assert case["failureExplanation"]["fortuneStart"]


def test_bazi_golden_coverage_matrix_shards_cover_all_cases_without_overlap():
    cases = _load_fixture()["cases"]
    shards = [_select_shard_cases(cases, total=4, index=index) for index in range(4)]
    shard_ids = [{case["id"] for case in shard} for shard in shards]

    assert all(shard for shard in shards)
    assert set().union(*shard_ids) == {case["id"] for case in cases}
    assert sum(len(ids) for ids in shard_ids) == len(cases)


@pytest.mark.parametrize("case", _representative_cases(_load_fixture()), ids=lambda case: case["id"])
def test_bazi_golden_coverage_matrix_representative_cases_match_current_core(case: dict):
    result = _run_case(case)
    expected = case["expected"]

    assert _pillar_names(result) == expected["fourPillars"]
    assert result["dayMaster"]["stem"] == expected["dayStem"]
    assert result["jiaoYun"]["startDate"] == expected["fortuneStart"]["startDate"]
    assert result["baziRuleDepth"]["appliedRules"]


@pytest.mark.slow
@pytest.mark.skipif(
    os.getenv("FATECAT_RUN_FULL_GOLDEN_MATRIX") != "1",
    reason="全量 300 case 属于 release/deep gate；默认本地回归跑 requiredTags 代表集。",
)
def test_bazi_golden_coverage_matrix_all_cases_match_current_core():
    cases = _load_fixture()["cases"]
    shard_total, shard_index = _shard_config_from_env()
    selected_cases = _select_shard_cases(cases, shard_total, shard_index)
    assert selected_cases, f"golden shard empty: index={shard_index}, total={shard_total}"

    for case in selected_cases:
        result = _run_case(case)
        expected = case["expected"]

        assert _pillar_names(result) == expected["fourPillars"], case["id"]
        assert result["dayMaster"]["stem"] == expected["dayStem"], case["id"]
        assert result["jiaoYun"]["startDate"] == expected["fortuneStart"]["startDate"], case["id"]
        assert result["baziRuleDepth"]["appliedRules"], case["id"]
