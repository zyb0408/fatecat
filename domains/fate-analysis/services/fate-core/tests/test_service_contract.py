from __future__ import annotations

import sys
from pathlib import Path

SERVICE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SERVICE_ROOT.parents[3]
SRC_DIR = SERVICE_ROOT / "src"
FATE_CORE_DIR = SRC_DIR / "fate_core"


def test_fate_core_source_root_is_canonical() -> None:
    contract = (SERVICE_ROOT / "service.yaml").read_text(encoding="utf-8")

    assert "source_root: domains/fate-analysis/services/fate-core/src" in contract
    assert "legacy_source_root:" not in contract
    assert "legacy_runtime_root:" not in contract
    assert (SRC_DIR / "fate_core" / "__init__.py").is_file()


def test_fate_core_package_loads_from_service_root() -> None:
    sys.modules.pop("fate_core", None)
    if str(SRC_DIR) in sys.path:
        sys.path.remove(str(SRC_DIR))
    sys.path.insert(0, str(SRC_DIR))

    import fate_core

    package_path = Path(fate_core.__file__).resolve()
    assert package_path.is_relative_to(SRC_DIR)
    assert (REPO_ROOT / "pyproject.toml").is_file()


def test_fate_core_kernel_owns_legacy_bazi_algorithm() -> None:
    kernel_source = (FATE_CORE_DIR / "kernel" / "bazi_calculator.py").read_text(encoding="utf-8")
    adapter_source = (FATE_CORE_DIR / "adapters" / "legacy_bazi.py").read_text(encoding="utf-8")

    assert "class BaziCalculator" in kernel_source
    assert "from datas import" in kernel_source
    assert "from fate_core.support.timezone import ensure_cn, fmt_cn, now_cn" in kernel_source
    assert "from fate_core.kernel.bazi_calculator import" in adapter_source
    assert "from bazi_calculator import" not in adapter_source
    assert "TELEGRAM_SRC_DIR" not in adapter_source
