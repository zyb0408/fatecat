from __future__ import annotations

from pathlib import Path


def _find_enterprise_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "pyproject.toml").exists() and (candidate / "domains").is_dir():
            return candidate
    raise RuntimeError("无法定位仓库根目录")


FATE_REPO_ROOT = _find_enterprise_repo_root()
FATE_CONTRACT_ROOT = FATE_REPO_ROOT / "contracts" / "fate"
FATE_CONFIG_ROOT = FATE_REPO_ROOT / "infra" / "environments" / "local"
FATE_DATA_ROOT = FATE_REPO_ROOT / "domains" / "fate-analysis" / "data-products"
FATE_DATABASE_ROOT = FATE_REPO_ROOT / "infra" / "databases"
FATE_VENDOR_ROOT = FATE_REPO_ROOT / "tools" / "reference-repos"
FATE_RUNTIME_ROOT = FATE_REPO_ROOT / "infra" / "runtime" / "local-state"
FATE_ASSET_ROOT = FATE_CONTRACT_ROOT
FATE_ASSETS_DIR = FATE_CONTRACT_ROOT
FATE_CAPABILITY_DIR = FATE_CONTRACT_ROOT / "capabilities"
FATE_PROFILE_DIR = FATE_CONTRACT_ROOT / "profiles"
TELEGRAM_SERVICE_ROOT = FATE_REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery"
TELEGRAM_SRC_DIR = TELEGRAM_SERVICE_ROOT / "src"
TELEGRAM_START_SCRIPT = TELEGRAM_SERVICE_ROOT / "start.py"
LUNAR_PYTHON_DIR = FATE_VENDOR_ROOT / "github" / "lunar-python-master"
