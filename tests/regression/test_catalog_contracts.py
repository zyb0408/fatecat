from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG_COMPONENTS = ROOT / "catalog" / "components"
COMPATIBILITY_LEDGER = ROOT / "governance" / "migration" / "compatibility-ledger.md"


def test_component_catalog_has_no_active_compatibility_box_pointers() -> None:
    forbidden_markers = [
        "compatibility_source_root:",
        "temporary-compatibility-box",
        "scripts/project/modules",
    ]

    offenders: list[str] = []
    for path in sorted(CATALOG_COMPONENTS.glob("*.yaml")):
        source = path.read_text(encoding="utf-8")
        if any(marker in source for marker in forbidden_markers):
            offenders.append(path.name)

    assert offenders == []


def test_component_catalog_points_to_canonical_service_roots() -> None:
    expected_roots = {
        "fate-core.yaml": "source_root: domains/fate-analysis/services/fate-core/src",
        "fatecat-delivery.yaml": "source_root: domains/experience-delivery/services/fatecat-delivery/src",
    }

    for filename, expected_source_root in expected_roots.items():
        source = (CATALOG_COMPONENTS / filename).read_text(encoding="utf-8")
        assert "lifecycle: canonical-active" in source
        assert expected_source_root in source
        assert "migration_status: compatibility-box-retired" in source


def test_retained_active_compatibility_entries_have_owner_and_removal_condition() -> None:
    ledger = COMPATIBILITY_LEDGER.read_text(encoding="utf-8")

    required_entries = [
        "domains/experience-delivery/services/fatecat-delivery/src/bazi_calculator.py",
        "domains/fate-analysis/services/fate-core/src/fate_core/adapters/legacy_bazi.py",
        "FATE_API_TOKEN",
    ]
    required_headings = ["owner", "真实契约", "保留原因", "移除条件"]

    for entry in required_entries:
        assert entry in ledger
    for heading in required_headings:
        assert heading in ledger
    assert "compatibility_source_root" in ledger
    assert "temporary-compatibility-box" in ledger
