from __future__ import annotations

from typing import Any

from fate_core.adapters import ZiweiIztroInput, calculate_ziwei_iztro
from fate_core.usecases.calculate_pure_analysis import (
    PureAnalysisInput,
    build_pure_analysis_input_from_payload,
    normalize_gender,
)


def build_ziwei_input_from_payload(raw_payload: dict[str, Any]) -> PureAnalysisInput:
    """从统一 payload 构造紫微斗数输入。"""
    return build_pure_analysis_input_from_payload(raw_payload)


def _public_place(place: str) -> str:
    return place if "北京" in place else "已填写（非北京地区已隐藏）"


def _star_names(stars: object) -> list[str]:
    if not isinstance(stars, list):
        return []
    names: list[str] = []
    for star in stars:
        if not isinstance(star, dict):
            continue
        name = str(star.get("name", "")).strip()
        if name:
            names.append(name)
    return names


def _all_stars(palace: dict[str, Any]) -> list[dict[str, Any]]:
    stars: list[dict[str, Any]] = []
    for key in ("majorStars", "minorStars", "adjectiveStars"):
        values = palace.get(key)
        if isinstance(values, list):
            stars.extend([item for item in values if isinstance(item, dict)])
    return stars


def _palace_marker(palace: dict[str, Any]) -> str:
    markers = []
    if palace.get("isOriginalPalace"):
        markers.append("命宫")
    if palace.get("isBodyPalace"):
        markers.append("身宫")
    return "、".join(markers)


def _summarize_surrounded_block(block: object) -> dict[str, Any]:
    if not isinstance(block, dict):
        return {}
    result: dict[str, Any] = {}
    for key, label in [("target", "本宫"), ("opposite", "对宫"), ("wealth", "财帛位"), ("career", "官禄位")]:
        palace = block.get(key)
        if not isinstance(palace, dict):
            continue
        result[key] = {
            "role": label,
            "palace": palace.get("name", ""),
            "earthlyBranch": palace.get("earthlyBranch", ""),
            "majorStars": _star_names(palace.get("majorStars")),
            "minorStars": _star_names(palace.get("minorStars")),
        }
    result["mutagenFlags"] = {
        "禄": bool(block.get("hasLu")),
        "权": bool(block.get("hasQuan")),
        "科": bool(block.get("hasKe")),
        "忌": bool(block.get("hasJi")),
    }
    return result


def _build_ziwei_interpretation(data: dict[str, Any]) -> dict[str, Any]:
    palaces = data.get("palaceAnalysis", [])
    palaces = [item for item in palaces if isinstance(item, dict)] if isinstance(palaces, list) else []
    chart = data.get("ziweiChart", {}) if isinstance(data.get("ziweiChart"), dict) else {}
    horoscope = data.get("ziweiHoroscope", {}) if isinstance(data.get("ziweiHoroscope"), dict) else {}

    main_star_combinations = []
    life_body = []
    mutagen_placements = []
    for palace in palaces:
        major = _star_names(palace.get("majorStars"))
        minor = _star_names(palace.get("minorStars"))
        adjective = _star_names(palace.get("adjectiveStars"))
        if major:
            main_star_combinations.append(
                {
                    "palace": palace.get("name", ""),
                    "combination": "、".join(major),
                    "majorStars": major,
                    "minorStars": minor,
                    "adjectiveStars": adjective,
                    "basis": ["majorStars", "minorStars", "adjectiveStars"],
                }
            )
        marker = _palace_marker(palace)
        if marker:
            life_body.append(
                {
                    "marker": marker,
                    "palace": palace.get("name", ""),
                    "earthlyBranch": palace.get("earthlyBranch", ""),
                    "heavenlyStem": palace.get("heavenlyStem", ""),
                    "majorStars": major,
                    "decadal": palace.get("decadal"),
                    "basis": ["isOriginalPalace", "isBodyPalace", "majorStars", "decadal"],
                    "statement": f"{marker}落{palace.get('name', '')}，主星为{'、'.join(major) if major else '空宫'}；此处只作盘面结构说明。",
                }
            )
        for star in _all_stars(palace):
            mutagen = str(star.get("mutagen", "")).strip()
            if mutagen:
                mutagen_placements.append(
                    {
                        "mutagen": mutagen,
                        "star": star.get("name", ""),
                        "palace": palace.get("name", ""),
                        "scope": star.get("scope", ""),
                        "basis": ["star.mutagen", "palace.name"],
                    }
                )

    surrounded = chart.get("surroundedPalaces", {}) if isinstance(chart.get("surroundedPalaces"), dict) else {}
    surrounded_summary = {
        "life": _summarize_surrounded_block(surrounded.get("life")),
        "body": _summarize_surrounded_block(surrounded.get("body")),
    }

    fortune_links = []
    for scope_key, scope_name in [
        ("decadal", "大限"),
        ("yearly", "流年"),
        ("monthly", "流月"),
        ("daily", "流日"),
        ("hourly", "流时"),
    ]:
        scope = horoscope.get(scope_key)
        if not isinstance(scope, dict) or not scope:
            continue
        fortune_links.append(
            {
                "scope": scope_name,
                "ganZhi": f"{scope.get('heavenlyStem', '')}{scope.get('earthlyBranch', '')}",
                "mutagen": scope.get("mutagen", []),
                "palaceNames": scope.get("palaceNames", []),
                "basis": [f"ziweiHoroscope.{scope_key}.mutagen", f"ziweiHoroscope.{scope_key}.palaceNames"],
            }
        )

    return {
        "schemaVersion": 1,
        "interpretationBoundary": "结构化解释层，只解释盘面证据与作用域，不输出确定性断语。",
        "mainStarCombinations": main_star_combinations,
        "lifeBody": life_body,
        "surroundedPalaces": surrounded_summary,
        "mutagenPlacements": mutagen_placements,
        "fortuneLinks": fortune_links,
    }


def _select_ziwei_payload(raw: dict[str, Any], payload: PureAnalysisInput) -> dict[str, Any]:
    input_payload = {
        "name": payload.name or "命主",
        "gender": normalize_gender(payload.gender),
        "birthDateTime": payload.birth_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "birthPlace": _public_place(payload.birth_place),
        "longitude": payload.longitude,
        "latitude": payload.latitude,
        "useTrueSolarTime": payload.use_true_solar_time,
    }

    data = {
        "capabilityId": "ziwei",
        "input": input_payload,
        "inputTrace": raw.get("inputTrace", {}),
        "birthInfo": raw.get("birthInfo", {}),
        "ziweiChart": raw.get("ziweiChart", {}),
        "palaceAnalysis": raw.get("palaceAnalysis", {}),
        "fiveElementsClass": raw.get("fiveElementsClass", ""),
        "starInfluence": raw.get("starInfluence", {}),
        "starPositions": raw.get("starPositions", []),
        "ziweiHoroscope": raw.get("ziweiHoroscope", {}),
        "meta": {
            "birthPlaceDisplay": _public_place(payload.birth_place),
            "source": "BaziCalculator true-solar pipeline + fortel/iztro",
            "legacyZiweiBasic": "disabled",
        },
    }
    data["ziweiInterpretation"] = _build_ziwei_interpretation(data)
    return data


def _build_evidence(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "capabilityId": "ziwei",
        "source": "iztro",
        "items": {
            "ziweiChart": {
                "source": "fortel_ziwei_integration -> iztro",
                "ruleIds": ["ziwei.iztro_chart", "ziwei.palace_metadata", "ziwei.decadal_ranges"],
                "basis": ["ziweiChart", "palaceAnalysis", "starPositions", "fiveElementsClass"],
                "risk": "folk_reference",
            },
            "horoscope": {
                "source": "iztro horoscope",
                "ruleIds": ["ziwei.horoscope_cycles", "ziwei.mutagen_scope"],
                "basis": ["ziweiHoroscope"],
                "risk": "folk_reference",
            },
            "timePipeline": {
                "source": "BaziCalculator true-solar pipeline",
                "ruleIds": ["bazi.true_solar_time_pipeline", "ziwei.time_index"],
                "basis": ["inputTrace.originalTime", "inputTrace.trueSolarTime", "inputTrace.timeZhi"],
                "risk": "calendar_boundary",
            },
            "interpretation": {
                "source": "iztro structured fields + FateCat interpretation boundary",
                "ruleIds": [
                    "ziwei.main_star_combination",
                    "ziwei.life_body_palaces",
                    "ziwei.surrounded_palaces",
                    "ziwei.mutagen_placement",
                    "ziwei.fortune_linkage",
                ],
                "basis": [
                    "ziweiInterpretation.mainStarCombinations",
                    "ziweiInterpretation.lifeBody",
                    "ziweiInterpretation.surroundedPalaces",
                    "ziweiInterpretation.mutagenPlacements",
                    "ziweiInterpretation.fortuneLinks",
                ],
                "risk": "folk_reference",
            },
        },
        "coverage": {
            "hasChart": bool(data.get("ziweiChart")),
            "hasHoroscope": bool(data.get("ziweiHoroscope")),
            "hasInterpretation": bool(data.get("ziweiInterpretation")),
            "palaceCount": len(data.get("palaceAnalysis", [])) if isinstance(data.get("palaceAnalysis"), list) else 0,
            "starPositionCount": len(data.get("starPositions", []))
            if isinstance(data.get("starPositions"), list)
            else 0,
            "hasInputTrace": bool(data.get("inputTrace")),
        },
    }


def calculate_ziwei(payload: PureAnalysisInput) -> dict[str, Any]:
    """计算紫微斗数独立 capability。"""
    adapter_payload = ZiweiIztroInput(
        birth_dt=payload.birth_dt,
        gender=normalize_gender(payload.gender),
        longitude=payload.longitude,
        latitude=payload.latitude,
        name=payload.name,
        birth_place=_public_place(payload.birth_place),
        use_true_solar_time=payload.use_true_solar_time,
    )
    raw = calculate_ziwei_iztro(adapter_payload)
    data = _select_ziwei_payload(raw, payload)
    data["analysisEvidence"] = _build_evidence(data)
    return data
