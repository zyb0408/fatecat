from __future__ import annotations

from typing import Any


def evidence_item(
    *,
    conclusion: dict[str, Any],
    basis: list[str],
    sources: list[str],
    rule_ids: list[str],
    weight: str = "core",
) -> dict[str, Any]:
    """构造标准分析证据项。"""
    return {
        "conclusion": conclusion,
        "basis": basis,
        "sources": sources,
        "ruleIds": rule_ids,
        "weight": weight,
        "visibility": "audit",
        "riskBoundary": risk_boundary_for_weight(weight),
    }


def risk_boundary_for_weight(weight: str) -> str:
    """按证据权重给出统一风险边界。"""
    if weight == "folk":
        return "民俗附录只作文化材料展示，不参与核心判断。"
    if weight == "auxiliary":
        return "辅助证据只能补充结构背景，不替代核心格局、强弱或用神判断。"
    if weight == "fortune":
        return "岁运触发只说明传统结构被引动，不输出确定事件或高风险决策建议。"
    return "仅作传统文化结构分析，不输出确定性人生结论或替代专业建议。"


def ensure_evidence_risk_boundaries(raw: dict[str, Any]) -> None:
    """给旧 evidence item 补齐风险边界，保持历史输出兼容。"""
    evidence = raw.get("analysisEvidence")
    if not isinstance(evidence, dict):
        return
    items = evidence.get("items")
    if not isinstance(items, dict):
        return
    for item in items.values():
        if not isinstance(item, dict):
            continue
        weight = str(item.get("weight") or "core")
        item.setdefault("riskBoundary", risk_boundary_for_weight(weight))


def append_accuracy_evidence(runtime: Any, raw: dict[str, Any]) -> None:
    """把准确性边界守卫写入 analysisEvidence。"""
    evidence = raw.get("analysisEvidence")
    if not isinstance(evidence, dict):
        return
    items = evidence.setdefault("items", {})
    if not isinstance(items, dict):
        return

    guards = raw.get("accuracyGuards", {})
    time_pipeline = guards.get("timePipeline", {}) if isinstance(guards, dict) else {}
    solar_term = guards.get("solarTermBoundary", {}) if isinstance(guards, dict) else {}
    fortune_start = guards.get("fortuneStartBoundary", {}) if isinstance(guards, dict) else {}
    pattern_trace = guards.get("patternUseGodTrace", {}) if isinstance(guards, dict) else {}

    zi_time_analysis = time_pipeline.get("ziTimeAnalysis", {})
    items["timePipeline"] = evidence_item(
        conclusion={
            "trueSolarTime": time_pipeline.get("trueSolarTime"),
            "totalOffsetMinutes": time_pipeline.get("totalOffsetMinutes"),
            "ziTimeShift": zi_time_analysis.get("zwzShift") if isinstance(zi_time_analysis, dict) else None,
        },
        basis=[
            f"输入时间={time_pipeline.get('inputLocalTime', '')}",
            f"经度={runtime.payload.longitude}",
            f"纬度={runtime.payload.latitude}",
            f"真太阳时={time_pipeline.get('trueSolarTime', '')}",
        ],
        sources=["paipan-master 真太阳时算法", "lunar-python"],
        rule_ids=["bazi.true_solar_time_pipeline", "bazi.zi_time_boundary"],
    )
    items["solarTermBoundary"] = evidence_item(
        conclusion={
            "yearPillar": solar_term.get("yearPillar"),
            "monthPillar": solar_term.get("monthPillar"),
            "monthCommand": solar_term.get("monthCommand"),
        },
        basis=[
            f"上一节气={solar_term.get('previousTerm', {})}",
            f"下一节气={solar_term.get('nextTerm', {})}",
            f"说明={solar_term.get('description', '')}",
        ],
        sources=["lunar-python", "1900-2030 交节时间 golden fixture"],
        rule_ids=["bazi.solar_term_month_boundary", "bazi.lichun_year_boundary"],
    )
    items["fortuneStartBoundary"] = evidence_item(
        conclusion={
            "startDate": fortune_start.get("startDate"),
            "anchorTerm": fortune_start.get("anchorTerm"),
        },
        basis=[f"性别={runtime.payload.gender}", f"起运说明={fortune_start.get('description', '')}"],
        sources=["lunar-python EightChar.getYun", "项目起运边界回归"],
        rule_ids=["bazi.fortune_start_boundary"],
        weight="fortune",
    )
    items["patternUseGodTrace"] = evidence_item(
        conclusion={
            "mainPattern": pattern_trace.get("mainPattern"),
            "yongShenBasisSource": pattern_trace.get("yongShenBasisSource"),
        },
        basis=[
            f"月柱={pattern_trace.get('monthPillar', '')}",
            f"月支藏干={pattern_trace.get('monthHiddenStems', [])}",
            f"调候原始={pattern_trace.get('tiaohouRaw', '')}",
        ],
        sources=["bazi-1", "项目格局/调候规则索引"],
        rule_ids=["bazi.pattern_use_god_trace"],
    )


def append_bazi_benchmark_evidence(raw: dict[str, Any]) -> None:
    """把八字 benchmark 汇总写入 analysisEvidence。"""
    evidence = raw.get("analysisEvidence")
    benchmark = raw.get("baziBenchmark")
    if not isinstance(evidence, dict) or not isinstance(benchmark, dict):
        return
    items = evidence.setdefault("items", {})
    if not isinstance(items, dict):
        return
    items["baziBenchmark"] = evidence_item(
        conclusion={
            "hasTimeBoundary": bool(benchmark.get("timeBoundaryGolden")),
            "hasRenyuan": bool(benchmark.get("renYuanSiling")),
            "hasStrengthScore": bool(benchmark.get("strengthScore")),
            "hasCombineTransformMatrix": bool(benchmark.get("combineTransformMatrix")),
            "hasYongShenDecision": bool(benchmark.get("yongShenDecision")),
            "topicProfileCount": len(benchmark.get("topicProfiles", []))
            if isinstance(benchmark.get("topicProfiles"), list)
            else 0,
            "fortuneTriggerCount": len(benchmark.get("fortuneTriggers", []))
            if isinstance(benchmark.get("fortuneTriggers"), list)
            else 0,
        },
        basis=[
            "baziBenchmark.timeBoundaryGolden",
            "baziBenchmark.renYuanSiling",
            "baziBenchmark.strengthScore",
            "baziBenchmark.ganzhiPriority",
            "baziBenchmark.combineTransformMatrix",
            "baziBenchmark.fortuneTriggers",
            "baziBenchmark.yongShenStrategies",
            "baziBenchmark.yongShenDecision",
            "baziBenchmark.topicProfiles",
        ],
        sources=["lunar-python", "bazi-1", "项目标杆加固规则"],
        rule_ids=[
            "bazi.renyuan_siling_weight",
            "bazi.strength_score_golden",
            "bazi.ganzhi_priority",
            "bazi.fortune_trigger_boundary",
            "bazi.yongshen_strategy",
            "bazi.ten_god_structure",
            "bazi.topic_profile_boundary",
        ],
    )


def append_bazi_rule_depth_evidence(raw: dict[str, Any]) -> None:
    """把八字规则深度层汇总写入 analysisEvidence。"""
    evidence = raw.get("analysisEvidence")
    rule_depth = raw.get("baziRuleDepth")
    if not isinstance(evidence, dict) or not isinstance(rule_depth, dict):
        return
    items = evidence.setdefault("items", {})
    if not isinstance(items, dict):
        return
    applied = rule_depth.get("appliedRules", [])
    items["baziRuleDepth"] = evidence_item(
        conclusion={
            "appliedRuleCount": len(applied) if isinstance(applied, list) else 0,
            "registryVersion": rule_depth.get("registryVersion"),
            "conflictCount": len(rule_depth.get("conflictMatrix", []))
            if isinstance(rule_depth.get("conflictMatrix"), list)
            else 0,
            "primaryRuleIds": rule_depth.get("conflictResolution", {}).get("primaryRuleIds", [])
            if isinstance(rule_depth.get("conflictResolution"), dict)
            else [],
        },
        basis=[
            "baziRuleDepth.appliedRules",
            "baziRuleDepth.conflictMatrix",
            "baziBenchmark",
            "accuracyGuards",
        ],
        sources=["rule_depth_registry.json", "classics_rule_index.json", "项目八字规则深度层"],
        rule_ids=rule_depth.get("sourceRuleIds", []),
    )
