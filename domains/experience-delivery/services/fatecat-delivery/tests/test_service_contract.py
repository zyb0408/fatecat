from __future__ import annotations

import importlib.util
from pathlib import Path

SERVICE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SERVICE_ROOT.parents[3]
SRC_DIR = SERVICE_ROOT / "src"
DELIVERY_ORCHESTRATION_MODULES = [
    "main.py",
    "web_ui.py",
    "bot.py",
    "report_generator.py",
    "output_formatter.py",
]


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


def test_delivery_orchestration_modules_do_not_read_domain_rule_sources() -> None:
    forbidden_markers = [
        "rule_depth_registry.json",
        "classics_rule_index.json",
        "tools/reference-repos/github/bazi-1-master",
        "datas.jinbuhuan",
        "datas.tiaohous",
    ]

    for module_name in DELIVERY_ORCHESTRATION_MODULES:
        source = (SRC_DIR / module_name).read_text(encoding="utf-8")
        for marker in forbidden_markers:
            assert marker not in source, f"{module_name} must not read domain rule source {marker}"


def test_delivery_bazi_calculator_is_only_a_fate_core_wrapper() -> None:
    source = (SRC_DIR / "bazi_calculator.py").read_text(encoding="utf-8")

    assert "from fate_core.kernel.bazi_calculator import" in source
    assert "class BaziCalculator" not in source
    assert "from datas import" not in source
    assert "datas.jinbuhuan" not in source
    assert "datas.tiaohous" not in source


def test_delivery_has_no_domain_algorithm_source_files() -> None:
    domain_algorithm_markers = ["datas.jinbuhuan", "datas.tiaohous", "bazi-1 原生映射"]
    offenders = []

    for path in SRC_DIR.glob("*.py"):
        source = path.read_text(encoding="utf-8")
        if any(marker in source for marker in domain_algorithm_markers):
            offenders.append(path.name)

    assert offenders == []
