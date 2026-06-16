from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import sxtwl
from lunar_python import Solar

ROOT = Path(__file__).resolve().parents[2]
BAZI_BOUNDARY_FIXTURE = (
    ROOT / "domains" / "fate-analysis" / "data-products" / "bazi" / "golden" / "calendar_boundary_cases.json"
)
BAZI_MISMATCH_REPORT = (
    ROOT / "domains" / "fate-analysis" / "data-products" / "bazi" / "golden" / "calendar_oracle_mismatch_report.json"
)
REFERENCE_MANIFEST = ROOT / "tools" / "reference-repos" / "vendor_sources.json"
PRODUCTION_SRC_ROOTS = [
    ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src",
    ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src",
]

GAN = "甲乙丙丁戊己庚辛壬癸"
ZHI = "子丑寅卯辰巳午未申酉戌亥"


def _load_bazi_boundary_fixture() -> dict:
    with BAZI_BOUNDARY_FIXTURE.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _load_bazi_mismatch_report() -> dict:
    with BAZI_MISMATCH_REPORT.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _load_reference_manifest() -> dict:
    with REFERENCE_MANIFEST.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _gz(value) -> str:
    return f"{GAN[value.tg]}{ZHI[value.dz]}"


def _sxtwl_pillars(dt: datetime) -> dict[str, str]:
    day = sxtwl.fromSolar(dt.year, dt.month, dt.day)
    return {
        "year": _gz(day.getYearGZ()),
        "month": _gz(day.getMonthGZ()),
        "day": _gz(day.getDayGZ()),
        "hour": _gz(day.getHourGZ(dt.hour)),
    }


def _lunar_python_pillars(dt: datetime) -> dict[str, str]:
    eight_char = Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second).getLunar().getEightChar()
    return {
        "year": eight_char.getYear(),
        "month": eight_char.getMonth(),
        "day": eight_char.getDay(),
        "hour": eight_char.getTime(),
    }


def test_sxtwl_oracle_matches_lunar_python_on_stable_four_pillar_samples():
    fixture = _load_bazi_boundary_fixture()
    stable_case_ids = {"beijing_early_zi_2000", "hong_kong_utc_input"}
    checked = 0

    for case in fixture["cases"]:
        if case["id"] not in stable_case_ids:
            continue
        expected = case["expected"]
        oracle_dt = datetime.fromisoformat(expected["trueSolarTime"])

        assert _sxtwl_pillars(oracle_dt) == expected["fourPillars"], case["id"]
        assert _lunar_python_pillars(oracle_dt) == expected["fourPillars"], case["id"]
        checked += 1

    assert checked == len(stable_case_ids)


def test_oracle_libraries_stay_out_of_production_source_paths():
    forbidden_markers = [
        "import sxtwl",
        "from sxtwl",
        "bazica",
        "bazi-calculator-by-alvamind",
    ]

    for root in PRODUCTION_SRC_ROOTS:
        for path in root.rglob("*.py"):
            source = path.read_text(encoding="utf-8")
            for marker in forbidden_markers:
                assert marker not in source, f"{marker} leaked into {path.relative_to(ROOT)}"


def test_reference_manifest_keeps_oracles_out_of_production_role():
    manifest = _load_reference_manifest()
    entries = {entry["id"]: entry for entry in manifest["required"] + manifest["optionalFutureFeatures"]}

    assert entries["lunar-python"]["usageRole"] == "production_dependency"
    assert entries["lunar-python"]["productionUseAllowed"] is True
    assert entries["sxwnl"]["usageRole"] == "oracle_only"
    assert entries["sxwnl"]["productionUseAllowed"] is False
    assert entries["bazica"]["usageRole"] == "oracle_only"
    assert entries["bazica"]["productionUseAllowed"] is False
    assert entries["bazi-calculator-by-alvamind"]["usageRole"] == "reference_only"
    assert entries["bazi-calculator-by-alvamind"]["productionUseAllowed"] is False


def test_calendar_oracle_mismatch_report_covers_runtime_full_boundary_cases():
    fixture = _load_bazi_boundary_fixture()
    report = _load_bazi_mismatch_report()

    runtime_cases = {
        case["id"]: case for case in fixture["cases"] if case.get("validationMode", "runtime_full") == "runtime_full"
    }
    schema_catalog_count = len(fixture["cases"]) - len(runtime_cases)
    report_cases = {case["id"]: case for case in report["cases"]}

    assert report["schemaVersion"] == 1
    assert report["reportType"] == "calendar_oracle_mismatch"
    assert report["generatedFrom"] == "calendar_boundary_cases.json"
    assert report["summary"]["runtimeFullCaseCount"] == len(runtime_cases)
    assert report["summary"]["schemaCatalogExcludedCount"] == schema_catalog_count
    assert report["summary"]["unexplainedMismatchCount"] == 0
    assert set(report_cases) == set(runtime_cases)

    for case_id, source_case in runtime_cases.items():
        report_case = report_cases[case_id]
        assert report_case["validationMode"] == "runtime_full"
        assert report_case["provider"]
        assert report_case["oracle"]
        assert report_case["input"] == source_case["input"]
        assert report_case["expected"] == source_case["expected"]
        assert report_case["actual"] == source_case["expected"]
        assert report_case["mismatchStatus"] in {"none", "explained"}
        assert report_case["decision"] in {"accepted_regression", "explained_difference"}
        assert report_case["failureExplanation"] == source_case["failureExplanation"]
