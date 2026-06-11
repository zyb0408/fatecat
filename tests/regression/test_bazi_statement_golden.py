from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest

from fate_core.usecases import PureAnalysisInput, calculate_pure_analysis

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "domains" / "fate-analysis" / "data-products" / "bazi" / "golden" / "statement_cases.json"


def _load_fixture() -> dict:
    with FIXTURE.open("r", encoding="utf-8") as fh:
        return json.load(fh)


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
            use_true_solar_time=True,
        )
    )


def _pillar_names(result: dict) -> dict[str, str]:
    return {name: result["fourPillars"][name]["fullName"] for name in ["year", "month", "day", "hour"]}


@pytest.mark.parametrize("case", _load_fixture()["cases"], ids=lambda case: case["id"])
def test_bazi_statement_cases_lock_core_judgement_boundaries(case: dict):
    result = _run_case(case)
    expected = case["expected"]

    assert _pillar_names(result) == expected["fourPillars"]
    assert result["dayMaster"]["stem"] == expected["dayMaster"]["stem"]
    assert result["dayMaster"]["strength"] == expected["dayMaster"]["strength"]
    assert result["geju"]["main"] == expected["gejuMain"]

    yong_shen = result["yongShen"]
    assert yong_shen.get("note", "") == expected["yongShen"]["note"]
    assert yong_shen.get("basisSource", "") == expected["yongShen"]["basisSource"]
    assert yong_shen.get("tiaohouRaw", "") == expected["yongShen"]["tiaohouRaw"]

    assert result["ganzhiRelations"]["tianGan"] == expected["ganzhiRelations"]["tianGan"]
    assert len(result["branchRelations"]["conflicts"]) == expected["ganzhiRelations"]["branchConflictCount"]
    assert result["jiaoYun"]["startDate"] == expected["fortuneStart"]["startDate"]
    assert result["jiaoYun"]["jiaoJieQi"] == expected["fortuneStart"]["anchorTerm"]

    emitted_rule_ids = {
        rule_id for item in result["analysisEvidence"]["items"].values() for rule_id in item.get("ruleIds", [])
    }
    for rule_id in expected["accuracyRuleIds"]:
        assert rule_id in emitted_rule_ids
