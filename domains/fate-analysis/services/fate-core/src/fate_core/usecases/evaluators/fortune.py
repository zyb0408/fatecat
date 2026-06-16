from __future__ import annotations

from typing import Any

from fate_core.usecases.rule_depth import rules_for_system


def build_fortune_trigger_matrix(raw: dict[str, Any], triggers: list[dict[str, Any]]) -> dict[str, Any]:
    """把岁运触发 registry 合同映射成 runtime 状态矩阵。"""
    rules = {rule["id"]: rule for rule in rules_for_system("bazi")}
    trigger_specs = rules.get("bazi.depth.fortune.trigger_chain", {}).get("triggerMatrix", [])
    major = raw.get("majorFortune", {}) if isinstance(raw.get("majorFortune"), dict) else {}
    major_pillars = major.get("pillars", []) if isinstance(major.get("pillars"), list) else []
    annual = raw.get("annualFortune", []) if isinstance(raw.get("annualFortune"), list) else []
    monthly = raw.get("monthlyFortune", []) if isinstance(raw.get("monthlyFortune"), list) else []
    type_counts: dict[str, int] = {}
    for trigger in triggers:
        for trigger_type in trigger.get("triggerTypes", []):
            type_counts[str(trigger_type)] = type_counts.get(str(trigger_type), 0) + 1

    def _status(trigger_type: str) -> str:
        if trigger_type == "major_stage":
            return "available" if major_pillars else "missing"
        if trigger_type == "annual_trigger":
            if type_counts.get("annual_trigger", 0):
                return "triggered"
            return "available" if annual else "missing"
        if trigger_type == "monthly_refinement":
            if monthly and (major_pillars or annual):
                return "available"
            return "blocked" if monthly else "missing"
        if type_counts.get(trigger_type, 0):
            return "triggered"
        return "not_triggered"

    matrix = []
    for spec in trigger_specs:
        trigger_type = str(spec.get("type", ""))
        matrix.append(
            {
                "type": trigger_type,
                "label": spec.get("label", ""),
                "status": _status(trigger_type),
                "count": type_counts.get(trigger_type, 0),
                "evidenceFields": spec.get("evidenceFields", []),
                "appliesWhen": spec.get("appliesWhen", []),
                "doesNotApplyWhen": spec.get("doesNotApplyWhen", []),
                "riskBoundary": spec.get("riskBoundary", ""),
            }
        )
    return {
        "schemaVersion": 1,
        "layerOrder": ["original_chart", "major_stage", "annual_trigger", "monthly_refinement"],
        "triggerTypeCounts": type_counts,
        "matrix": matrix,
        "conflictPolicy": "原局优先，大运定阶段，流年定触发，流月只细化窗口。",
        "riskBoundary": "岁运触发只作趋势证据，不输出确定未来、恐吓表述或高风险决策建议。",
    }
