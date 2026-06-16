from __future__ import annotations

import sys
from typing import Any

from fate_core.support.paths import LUNAR_PYTHON_DIR

try:
    from lunar_python import Solar  # type: ignore[import-untyped]
except ModuleNotFoundError:
    if str(LUNAR_PYTHON_DIR) not in sys.path:
        sys.path.insert(0, str(LUNAR_PYTHON_DIR))
    from lunar_python import Solar  # type: ignore[import-untyped]  # noqa: E402

__all__ = ["Solar", "build_lunar_day", "build_lunar_datetime"]


def build_lunar_day(year: int, month: int, day: int) -> Any:
    """用 lunar-python 构造指定公历日的农历/黄历对象。"""
    return Solar.fromYmd(year, month, day).getLunar()


def build_lunar_datetime(year: int, month: int, day: int, hour: int) -> Any:
    """用 lunar-python 构造指定公历日时的农历/黄历对象。"""
    return Solar.fromYmdHms(year, month, day, hour, 0, 0).getLunar()
