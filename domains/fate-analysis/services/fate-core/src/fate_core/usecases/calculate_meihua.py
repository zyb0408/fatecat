from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from fate_core.usecases.calculate_pure_analysis import parse_datetime

TRIGRAMS: tuple[str, ...] = ("坤", "艮", "坎", "巽", "震", "离", "兑", "乾")
TRIGRAM_ELEMENTS: dict[str, str] = {
    "乾": "金",
    "兑": "金",
    "离": "火",
    "震": "木",
    "巽": "木",
    "坎": "水",
    "艮": "土",
    "坤": "土",
}
HEXAGRAM_NAMES: dict[tuple[str, str], str] = {
    ("乾", "乾"): "乾为天",
    ("乾", "巽"): "天风姤",
    ("乾", "艮"): "天山遁",
    ("乾", "坤"): "天地否",
    ("巽", "坤"): "风地观",
    ("艮", "坤"): "山地剥",
    ("离", "坤"): "火地晋",
    ("离", "乾"): "火天大有",
    ("兑", "兑"): "兑为泽",
    ("兑", "坎"): "泽水困",
    ("兑", "坤"): "泽地萃",
    ("兑", "艮"): "泽山咸",
    ("坎", "艮"): "水山蹇",
    ("坤", "艮"): "地山谦",
    ("震", "艮"): "雷山小过",
    ("震", "兑"): "雷泽归妹",
    ("离", "离"): "离为火",
    ("离", "艮"): "火山旅",
    ("离", "巽"): "火风鼎",
    ("离", "坎"): "火水未济",
    ("艮", "坎"): "山水蒙",
    ("巽", "坎"): "风水涣",
    ("乾", "坎"): "天水讼",
    ("乾", "离"): "天火同人",
    ("震", "震"): "震为雷",
    ("震", "坤"): "雷地豫",
    ("震", "坎"): "雷水解",
    ("震", "巽"): "雷风恒",
    ("坤", "巽"): "地风升",
    ("坎", "巽"): "水风井",
    ("兑", "巽"): "泽风大过",
    ("兑", "震"): "泽雷随",
    ("巽", "巽"): "巽为风",
    ("巽", "乾"): "风天小畜",
    ("巽", "离"): "风火家人",
    ("巽", "震"): "风雷益",
    ("乾", "震"): "天雷无妄",
    ("离", "震"): "火雷噬嗑",
    ("艮", "震"): "山雷颐",
    ("艮", "巽"): "山风蛊",
    ("坎", "坎"): "坎为水",
    ("坎", "兑"): "水泽节",
    ("坎", "震"): "水雷屯",
    ("坎", "离"): "水火既济",
    ("兑", "离"): "泽火革",
    ("震", "离"): "雷火丰",
    ("坤", "离"): "地火明夷",
    ("坤", "坎"): "地水师",
    ("艮", "艮"): "艮为山",
    ("艮", "离"): "山火贲",
    ("艮", "乾"): "山天大畜",
    ("艮", "兑"): "山泽损",
    ("离", "兑"): "火泽睽",
    ("乾", "兑"): "天泽履",
    ("巽", "兑"): "风泽中孚",
    ("巽", "艮"): "风山渐",
    ("坤", "坤"): "坤为地",
    ("坤", "震"): "地雷复",
    ("坤", "兑"): "地泽临",
    ("坤", "乾"): "地天泰",
    ("震", "乾"): "雷天大壮",
    ("兑", "乾"): "泽天夬",
    ("坎", "乾"): "水天需",
    ("坎", "坤"): "水地比",
}


@dataclass(frozen=True)
class MeihuaInput:
    """梅花易数 capability 输入。"""

    question: str
    cast_method: str
    cast_value: str = ""
    cast_time: datetime | None = None
    place: str = ""


def _first_non_empty(*values: Any) -> Any:
    for value in values:
        if value not in (None, ""):
            return value
    return None


def build_meihua_input_from_payload(raw_payload: dict[str, Any]) -> MeihuaInput:
    """从统一 payload 构造梅花易数输入。"""
    question = str(raw_payload.get("question") or "").strip()
    if not question:
        raise ValueError("缺少必填字段: question")
    cast_method = str(_first_non_empty(raw_payload.get("castMethod"), raw_payload.get("method"), "time")).strip()
    cast_time_raw = _first_non_empty(raw_payload.get("castTime"), raw_payload.get("datetime"))
    return MeihuaInput(
        question=question,
        cast_method=cast_method,
        cast_value=str(raw_payload.get("castValue") or raw_payload.get("numbers") or "").strip(),
        cast_time=parse_datetime(str(cast_time_raw)) if cast_time_raw else None,
        place=str(raw_payload.get("place") or "").strip(),
    )


def _mod8(value: int) -> int:
    return value % 8 if value % 8 else 8


def _mod6(value: int) -> int:
    return value % 6 if value % 6 else 6


def _trigram(number: int) -> str:
    return TRIGRAMS[number - 1]


def _hexagram(upper: str, lower: str) -> dict[str, str]:
    return {
        "upper": upper,
        "lower": lower,
        "name": HEXAGRAM_NAMES.get((upper, lower), f"{upper}{lower}"),
    }


def _change_hexagram(upper_number: int, lower_number: int, moving_line: int) -> dict[str, str]:
    if moving_line <= 3:
        lower_number = _mod8(lower_number + moving_line)
    else:
        upper_number = _mod8(upper_number + moving_line)
    return _hexagram(_trigram(upper_number), _trigram(lower_number))


def _mutual_hexagram(upper_number: int, lower_number: int) -> dict[str, str]:
    return _hexagram(_trigram(_mod8(upper_number + lower_number)), _trigram(_mod8(upper_number * lower_number)))


def _cast_numbers(payload: MeihuaInput) -> tuple[int, int, int, dict[str, Any]]:
    numbers = [int(item) for item in payload.cast_value.replace("，", ",").split(",") if item.strip()]
    if len(numbers) < 2:
        raise ValueError("number 起卦需要 castValue 提供至少两个数字，例如 3,8")
    total = sum(numbers)
    upper = _mod8(numbers[0])
    lower = _mod8(numbers[1])
    moving = _mod6(total)
    return upper, lower, moving, {"numbers": numbers, "total": total}


def _cast_time(payload: MeihuaInput) -> tuple[int, int, int, dict[str, Any]]:
    cast_time = payload.cast_time or datetime.now()
    seed = cast_time.year + cast_time.month + cast_time.day
    upper = _mod8(seed)
    lower = _mod8(seed + cast_time.hour)
    moving = _mod6(seed + cast_time.hour)
    return upper, lower, moving, {"castTime": cast_time.strftime("%Y-%m-%d %H:%M:%S"), "seed": seed}


def calculate_meihua(payload: MeihuaInput) -> dict[str, Any]:
    """计算梅花易数独立 capability。"""
    method = payload.cast_method.lower()
    if method in {"number", "numbers", "数字", "数字起卦"}:
        upper_number, lower_number, moving_line, cast_basis = _cast_numbers(payload)
        method_label = "数字起卦"
        method_rule = "meihua.number_cast"
    elif method in {"time", "datetime", "时间", "时间起卦"}:
        upper_number, lower_number, moving_line, cast_basis = _cast_time(payload)
        method_label = "时间起卦"
        method_rule = "meihua.time_cast"
    else:
        raise ValueError(f"不支持的梅花起卦方式: {payload.cast_method}")

    upper = _trigram(upper_number)
    lower = _trigram(lower_number)
    original = _hexagram(upper, lower)
    mutual = _mutual_hexagram(upper_number, lower_number)
    changed = _change_hexagram(upper_number, lower_number, moving_line)
    body = "下卦" if moving_line <= 3 else "上卦"
    use = "上卦" if moving_line <= 3 else "下卦"

    evidence = {
        "schemaVersion": 1,
        "capabilityId": "meihua",
        "source": "fate_core.usecases.calculate_meihua",
        "items": {
            "cast": {
                "source": "梅花易数起卦规则",
                "ruleIds": [method_rule],
                "basis": cast_basis,
                "risk": "entertainment",
            },
            "bodyUse": {
                "source": "体用规则",
                "ruleIds": ["meihua.body_use"],
                "basis": {"movingLine": moving_line, "body": body, "use": use},
                "risk": "entertainment",
            },
            "transform": {
                "source": "本卦/互卦/变卦转换",
                "ruleIds": ["meihua.hexagram_transform"],
                "basis": {"upper": upper, "lower": lower, "movingLine": moving_line},
                "risk": "entertainment",
            },
        },
    }
    return {
        "capabilityId": "meihua",
        "question": payload.question,
        "castMethod": method_label,
        "castBasis": cast_basis,
        "hexagrams": {
            "original": original,
            "mutual": mutual,
            "changed": changed,
            "movingLine": moving_line,
        },
        "bodyUse": {
            "body": body,
            "use": use,
            "upperElement": TRIGRAM_ELEMENTS.get(upper, ""),
            "lowerElement": TRIGRAM_ELEMENTS.get(lower, ""),
        },
        "judgementBoundary": "梅花易数 capability 当前只输出盘面、体用和证据，不输出确定性断语。",
        "analysisEvidence": evidence,
    }
