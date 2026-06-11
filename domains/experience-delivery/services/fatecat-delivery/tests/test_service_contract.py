from __future__ import annotations

import importlib.util
from pathlib import Path

SERVICE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SERVICE_ROOT.parents[3]
SRC_DIR = SERVICE_ROOT / "src"


def test_delivery_source_root_is_canonical() -> None:
    contract = (SERVICE_ROOT / "service.yaml").read_text(encoding="utf-8")

    assert "source_root: domains/experience-delivery/services/fatecat-delivery/src" in contract
    assert "legacy_source_root:" not in contract
    assert "legacy_runtime_root:" not in contract
    assert (SRC_DIR / "_paths.py").is_file()
    assert (SERVICE_ROOT / "start.py").is_file()


def test_delivery_paths_module_uses_enterprise_repo_root() -> None:
    spec = importlib.util.spec_from_file_location("fatecat_delivery_paths", SRC_DIR / "_paths.py")
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.REPO_ROOT == REPO_ROOT
    assert module.FATE_CORE_SRC_DIR.is_relative_to(REPO_ROOT)
