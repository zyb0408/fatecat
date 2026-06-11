"""FateCat 企业根回归测试配置。"""

import sys
from pathlib import Path

import pytest

# 兼容历史裸模块导入，路径真相源已切换到 canonical service roots。
REPO_ROOT = Path(__file__).resolve().parents[2]
TELEGRAM_SERVICE_ROOT = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery"
TELEGRAM_SRC = TELEGRAM_SERVICE_ROOT / "src"
FATE_CORE_SRC = REPO_ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"

if str(TELEGRAM_SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(TELEGRAM_SERVICE_ROOT))
if str(TELEGRAM_SRC) not in sys.path:
    sys.path.insert(0, str(TELEGRAM_SRC))

if str(FATE_CORE_SRC) not in sys.path:
    sys.path.insert(0, str(FATE_CORE_SRC))


@pytest.fixture
def sample_birth_data():
    """Sample birth data for bazi calculation tests."""
    return {
        "year": 1990,
        "month": 6,
        "day": 15,
        "hour": 12,
        "gender": "male",
    }


@pytest.fixture
def sample_name():
    """Sample name for xingming analysis tests."""
    return {
        "surname": "测",
        "given_name": "试",
    }
