from __future__ import annotations

from typing import Any

ELEMENT_GENERATES = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}


def build_strength_score(raw: dict[str, Any], renyuan: dict[str, Any]) -> dict[str, Any]:
    """把强弱评分整理成可审计 evaluator 输出。"""
    wuxing = raw.get("wuxingScores", {}) if isinstance(raw.get("wuxingScores"), dict) else {}
    day_master = raw.get("dayMaster", {}) if isinstance(raw.get("dayMaster"), dict) else {}
    wuxing_state = raw.get("wuxingState", {}) if isinstance(raw.get("wuxingState"), dict) else {}
    five_element_score = wuxing.get("fiveElementScore", {}) if isinstance(wuxing.get("fiveElementScore"), dict) else {}
    day_element = str(day_master.get("elementCn") or day_master.get("element") or "")
    resource_element = next((source for source, target in ELEMENT_GENERATES.items() if target == day_element), "")
    month_state = wuxing_state.get(day_element, {}) if isinstance(wuxing_state.get(day_element), dict) else {}
    strong_score = wuxing.get("strongScore")
    basis = [
        {
            "factor": "dayMaster",
            "value": day_master.get("stem", ""),
            "evidenceField": "dayMaster.stem",
        },
        {
            "factor": "monthCommand",
            "value": renyuan.get("monthCommand", ""),
            "evidenceField": "baziBenchmark.renYuanSiling.monthCommand",
        },
        {
            "factor": "currentSiling",
            "value": renyuan.get("siling", {}).get("current") if isinstance(renyuan.get("siling"), dict) else "",
            "evidenceField": "baziBenchmark.renYuanSiling.siling.current",
        },
        {
            "factor": "strongScore",
            "value": strong_score,
            "evidenceField": "wuxingScores.strongScore",
        },
        {
            "factor": "dayElementScore",
            "element": day_element,
            "value": five_element_score.get(day_element),
            "evidenceField": f"wuxingScores.fiveElementScore.{day_element}" if day_element else "",
        },
        {
            "factor": "resourceElementScore",
            "element": resource_element,
            "value": five_element_score.get(resource_element),
            "evidenceField": f"wuxingScores.fiveElementScore.{resource_element}" if resource_element else "",
        },
        {
            "factor": "twelveGrowthStatus",
            "value": wuxing.get("statusDetail", []),
            "evidenceField": "wuxingScores.statusDetail",
        },
        {
            "factor": "monthSeasonState",
            "value": month_state.get("state", ""),
            "evidenceField": f"wuxingState.{day_element}.state" if day_element else "",
        },
    ]
    conflicts = []
    label = str(day_master.get("strength") or wuxing.get("weakStrong") or "")
    if month_state.get("state") in {"休", "囚", "死"} and label in {"中和偏强", "身强"}:
        conflicts.append(
            {
                "type": "month_command_pressure",
                "explanation": "月令状态偏弱但综合标签偏强，必须保留分歧证据。",
                "counterEvidence": ["wuxingState", "baziBenchmark.renYuanSiling", "wuxingScores.strongScore"],
                "discounts": 0.15,
            }
        )
    if month_state.get("state") in {"旺", "相"} and label in {"中和偏弱", "身弱"}:
        conflicts.append(
            {
                "type": "month_command_support",
                "explanation": "月令状态支持日主但综合标签偏弱，必须保留分歧证据。",
                "counterEvidence": ["wuxingState", "baziBenchmark.renYuanSiling", "wuxingScores.strongScore"],
                "discounts": 0.15,
            }
        )
    if not conflicts:
        conflicts.append(
            {
                "type": "none_detected",
                "explanation": "未发现月令、五行分数和十二长生之间的硬冲突；保留灰度标签。",
                "counterEvidence": [],
                "discounts": 0,
            }
        )
    return {
        "label": label,
        "weak": wuxing.get("weak"),
        "strongScore": strong_score,
        "score": strong_score,
        "statusDetail": wuxing.get("statusDetail", []),
        "fiveElementScore": five_element_score,
        "basis": basis,
        "sourceRuleId": "bazi.day_master_strength",
        "conflicts": conflicts,
        "evidenceFields": [
            "dayMaster",
            "wuxingScores.strongScore",
            "wuxingScores.statusDetail",
            "wuxingScores.fiveElementScore",
            "baziBenchmark.renYuanSiling",
        ],
        "riskBoundary": "强弱评分只作结构分析证据，不输出确定性人生结论。",
        "ruleIds": ["bazi.day_master_strength", "bazi.strength_score_golden"],
    }
