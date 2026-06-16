"""命卦计算。"""

from __future__ import annotations

from typing import Any

GUA_NAMES = ["坎", "坤", "震", "巽", "中", "乾", "兑", "艮", "离"]
GUA_DIRECTION = {"坎": "北", "坤": "西南", "震": "东", "巽": "东南", "乾": "西北", "兑": "西", "艮": "东北", "离": "南"}


def calc_ming_gua(year: int, gender: str) -> dict[str, Any]:
    """按出生年和性别计算命卦。"""
    digit_sum = sum(int(digit) for digit in str(year))
    while digit_sum >= 10:
        digit_sum = sum(int(digit) for digit in str(digit_sum))

    if gender == "male":
        gua_num = 11 - digit_sum if year < 2000 else 9 - digit_sum
        if gua_num <= 0:
            gua_num += 9
    else:
        gua_num = 4 + digit_sum if year < 2000 else 6 + digit_sum
        if gua_num > 9:
            gua_num -= 9

    if gua_num == 5:
        gua_num = 2 if gender == "male" else 8

    gua_name = GUA_NAMES[gua_num - 1] if 1 <= gua_num <= 9 else "坤"
    is_west_group = gua_name in ["乾", "兑", "艮", "坤"]
    return {
        "guaNum": gua_num,
        "guaName": gua_name,
        "direction": GUA_DIRECTION.get(gua_name, ""),
        "group": "西四命" if is_west_group else "东四命",
    }


__all__ = ["GUA_DIRECTION", "GUA_NAMES", "calc_ming_gua"]
