from __future__ import annotations

import contextlib
import io
from typing import Any

from fate_core.adapters import LegacyBaziInput, calculate_legacy_bazi
from fate_core.usecases.calculate_pure_analysis import (
    PureAnalysisInput,
    build_pure_analysis_input_from_payload,
    normalize_gender,
)

ZIWEI_HIDE: dict[str, bool] = {
    "extensions": False,
    "huangli": True,
    "zeri": True,
    "divination": True,
    "fengshui": True,
    "astro": True,
    "calendar": True,
    "number_divination": True,
    "yijing": True,
    "name_marriage": True,
    "system": True,
    "health": True,
}


def build_ziwei_input_from_payload(raw_payload: dict[str, Any]) -> PureAnalysisInput:
    """从统一 payload 构造紫微斗数输入。"""
    return build_pure_analysis_input_from_payload(raw_payload)


def _public_place(place: str) -> str:
    return place if "北京" in place else "已填写（非北京地区已隐藏）"


def _select_ziwei_payload(raw: dict[str, Any], payload: PureAnalysisInput) -> dict[str, Any]:
    input_payload = dict(raw.get("input", {})) if isinstance(raw.get("input"), dict) else {}
    if input_payload.get("birthPlace"):
        input_payload["birthPlace"] = _public_place(str(input_payload["birthPlace"]))

    return {
        "capabilityId": "ziwei",
        "input": input_payload,
        "birthInfo": raw.get("birthInfo", {}),
        "ziweiChart": raw.get("ziweiChart", {}),
        "palaceAnalysis": raw.get("palaceAnalysis", {}),
        "starInfluence": raw.get("starInfluence", {}),
        "starPositions": raw.get("starPositions", []),
        "ziweiHoroscope": raw.get("ziweiHoroscope", {}),
        "ziweiBasic": raw.get("ziweiBasic", {}),
        "meta": {
            "birthPlaceDisplay": _public_place(payload.birth_place),
            "source": "BaziCalculator + fortel/iztro + ZiweiCalculator",
        },
    }


def _build_evidence(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "capabilityId": "ziwei",
        "source": "iztro",
        "items": {
            "ziweiChart": {
                "source": "fortel_ziwei_integration -> iztro",
                "ruleIds": ["ziwei.iztro_chart"],
                "basis": ["ziweiChart", "palaceAnalysis", "starPositions"],
                "risk": "folk_reference",
            },
            "ziweiBasic": {
                "source": "modules/telegram/src/ziwei.py",
                "ruleIds": ["ziwei.basic_palaces"],
                "basis": ["ziweiBasic"],
                "risk": "folk_reference",
            },
            "horoscope": {
                "source": "iztro horoscope",
                "ruleIds": ["ziwei.horoscope_cycles"],
                "basis": ["ziweiHoroscope"],
                "risk": "folk_reference",
            },
        },
        "coverage": {
            "hasChart": bool(data.get("ziweiChart")),
            "hasBasic": bool(data.get("ziweiBasic")),
            "hasHoroscope": bool(data.get("ziweiHoroscope")),
        },
    }


def calculate_ziwei(payload: PureAnalysisInput) -> dict[str, Any]:
    """计算紫微斗数独立 capability。"""
    legacy_payload = LegacyBaziInput(
        birth_dt=payload.birth_dt,
        gender=normalize_gender(payload.gender),
        longitude=payload.longitude,
        latitude=payload.latitude,
        name=payload.name,
        birth_place=_public_place(payload.birth_place),
        use_true_solar_time=payload.use_true_solar_time,
    )
    # 遗留扩展会打印性能日志；CLI capability 必须保持 stdout 为纯 JSON。
    with contextlib.redirect_stdout(io.StringIO()):
        raw = calculate_legacy_bazi(legacy_payload, hide=ZIWEI_HIDE)
    data = _select_ziwei_payload(raw, payload)
    data["analysisEvidence"] = _build_evidence(data)
    return data
