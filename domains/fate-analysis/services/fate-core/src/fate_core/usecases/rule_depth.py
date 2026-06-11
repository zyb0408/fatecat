from __future__ import annotations

import json
from functools import cache
from typing import Any

from fate_core.support.paths import FATE_ASSETS_DIR


@cache
def load_rule_depth_registry() -> dict[str, Any]:
    """加载八字/紫微规则深度 registry。"""
    path = FATE_ASSETS_DIR / "rule_depth_registry.json"
    with path.open("r", encoding="utf-8") as fh:
        registry = json.load(fh)
    if not isinstance(registry, dict):
        raise ValueError("rule_depth_registry.json 必须是 JSON 对象")
    rules = registry.get("rules")
    if not isinstance(rules, list) or not rules:
        raise ValueError("rule_depth_registry.json 缺少 rules")
    return registry


def rules_for_system(system: str) -> list[dict[str, Any]]:
    """按体系选择规则，保持 priority 降序稳定输出。"""
    registry = load_rule_depth_registry()
    selected = [rule for rule in registry["rules"] if isinstance(rule, dict) and rule.get("system") == system]
    return sorted(selected, key=lambda item: int(item.get("priority", 0)), reverse=True)


def registry_version() -> str:
    """返回规则深度 registry 版本。"""
    return str(load_rule_depth_registry().get("registryVersion", "unknown"))


def build_rule_application(
    rule: dict[str, Any],
    *,
    status: str,
    evidence: dict[str, Any],
    confidence: float | None = None,
    notes: list[str] | None = None,
) -> dict[str, Any]:
    """把 registry 规则和命盘证据组合成可审计应用记录。"""
    weight = float(rule.get("weight", 0.0))
    score = weight if confidence is None else round(max(0.0, min(1.0, confidence)), 2)
    return {
        "ruleId": rule.get("id", ""),
        "topic": rule.get("topic", ""),
        "layer": rule.get("layer", ""),
        "status": status,
        "weight": weight,
        "confidence": score,
        "evidenceFields": rule.get("evidenceFields", []),
        "conditions": rule.get("conditions", []),
        "evidence": evidence,
        "conflictPolicy": rule.get("conflictPolicy", ""),
        "riskBoundary": rule.get("riskBoundary", ""),
        "sourceRuleIds": rule.get("sourceRuleIds", []),
        "notes": notes or [],
    }


def collect_source_rule_ids(applied_rules: list[dict[str, Any]]) -> list[str]:
    """从应用记录中收集 classics_rule_index 可追溯规则 ID。"""
    ids: list[str] = []
    seen = set()
    for item in applied_rules:
        for rule_id in item.get("sourceRuleIds", []):
            if isinstance(rule_id, str) and rule_id and rule_id not in seen:
                ids.append(rule_id)
                seen.add(rule_id)
    return ids


def build_conflict_resolution(
    applied_rules: list[dict[str, Any]],
    conflict_matrix: list[dict[str, Any]],
) -> dict[str, Any]:
    """按层级、权重和置信度生成统一冲突裁决摘要。"""
    layer_rank = {"core": 4, "dynamic": 3, "topic": 2, "boundary": 1}
    ranked = sorted(
        applied_rules,
        key=lambda item: (
            layer_rank.get(str(item.get("layer", "")), 0),
            float(item.get("confidence", 0.0)),
            float(item.get("weight", 0.0)),
        ),
        reverse=True,
    )
    primary = [item.get("ruleId", "") for item in ranked[:3] if item.get("ruleId")]
    auxiliary = [item.get("ruleId", "") for item in ranked[3:] if item.get("ruleId")]
    indexed = {item.get("ruleId"): item for item in applied_rules}
    conflicts = []
    for conflict in conflict_matrix:
        rule_ids = [rule_id for rule_id in conflict.get("rules", []) if rule_id in indexed]
        if not rule_ids:
            continue
        rule_rank = {rule_id: rank for rank, rule_id in enumerate(primary + auxiliary)}
        ordered_rule_ids = sorted(rule_ids, key=lambda rule_id: rule_rank.get(rule_id, 10_000))
        primary_rule = ordered_rule_ids[0]
        secondary_rules = ordered_rule_ids[1:]
        conflicts.append(
            {
                "type": conflict.get("type", "priority"),
                "topic": conflict.get("topic", ""),
                "rules": rule_ids,
                "policy": conflict.get("policy", ""),
                "primaryRule": primary_rule,
                "secondaryRules": secondary_rules,
                "explanation": _conflict_explanation(
                    indexed[primary_rule], [indexed[rule_id] for rule_id in secondary_rules]
                ),
                "discounts": _conflict_discounts(
                    indexed[primary_rule], [indexed[rule_id] for rule_id in secondary_rules]
                ),
                "counterEvidence": _counter_evidence(
                    indexed[primary_rule], [indexed[rule_id] for rule_id in secondary_rules]
                ),
                "status": "resolved_by_policy",
            }
        )
    return {
        "schemaVersion": 1,
        "method": "layer_rank_then_confidence_then_weight",
        "primaryRuleIds": primary,
        "auxiliaryRuleIds": auxiliary,
        "conflicts": conflicts,
        "riskBoundary": "冲突裁决只决定解释优先级，不输出确定未来或替代专业建议。",
    }


def build_weight_profile(applied_rules: list[dict[str, Any]]) -> dict[str, Any]:
    """汇总规则权重，供审计检查解释优先级。"""
    layer_weights: dict[str, float] = {}
    layer_confidences: dict[str, list[float]] = {}
    for item in applied_rules:
        layer = str(item.get("layer", "unknown") or "unknown")
        weight = float(item.get("weight", 0.0))
        confidence = float(item.get("confidence", 0.0))
        layer_weights[layer] = round(layer_weights.get(layer, 0.0) + weight, 3)
        layer_confidences.setdefault(layer, []).append(confidence)

    layer_summary = {
        layer: {
            "weight": weight,
            "avgConfidence": round(sum(layer_confidences[layer]) / len(layer_confidences[layer]), 3),
            "ruleCount": len(layer_confidences[layer]),
        }
        for layer, weight in sorted(layer_weights.items())
    }
    ranked = sorted(
        applied_rules,
        key=lambda item: (float(item.get("confidence", 0.0)), float(item.get("weight", 0.0))),
        reverse=True,
    )
    total_weight = round(sum(float(item.get("weight", 0.0)) for item in applied_rules), 3)
    weighted_confidence = (
        round(
            sum(float(item.get("weight", 0.0)) * float(item.get("confidence", 0.0)) for item in applied_rules)
            / total_weight,
            3,
        )
        if total_weight
        else 0.0
    )
    return {
        "schemaVersion": 1,
        "method": "sum_weight_and_weighted_confidence",
        "totalWeight": total_weight,
        "weightedConfidence": weighted_confidence,
        "layerSummary": layer_summary,
        "topRules": [item.get("ruleId", "") for item in ranked[:5] if item.get("ruleId")],
    }


def build_combination_statement(
    *,
    topic: str,
    statement: str,
    rule_ids: list[str],
    evidence: dict[str, Any],
    confidence: float,
    risk_boundary: str,
) -> dict[str, Any]:
    """生成克制的组合断语，不承诺确定事件。"""
    return {
        "topic": topic,
        "statement": statement,
        "ruleIds": rule_ids,
        "evidence": evidence,
        "confidence": round(max(0.0, min(1.0, confidence)), 2),
        "riskBoundary": risk_boundary,
    }


def build_narrative_summary(
    *,
    title: str,
    combination_statements: list[dict[str, Any]],
    conflict_resolution: dict[str, Any],
) -> dict[str, Any]:
    """把结构化组合断语压成可复制 Markdown 摘要，并保留追溯字段。"""
    lines = [f"### {title}"]
    rule_ids: list[str] = []
    for item in combination_statements:
        topic = str(item.get("topic", ""))
        statement = str(item.get("statement", ""))
        item_rule_ids = [str(rule_id) for rule_id in item.get("ruleIds", []) if isinstance(rule_id, str)]
        rule_ids.extend(item_rule_ids)
        lines.append(f"- **{topic}**：{statement}（依据：{', '.join(item_rule_ids)}）")

    conflicts = conflict_resolution.get("conflicts", [])
    if isinstance(conflicts, list) and conflicts:
        lines.append("- **冲突裁决**：")
        for conflict in conflicts:
            if not isinstance(conflict, dict):
                continue
            lines.append(
                f"  - {conflict.get('topic', '')}：{conflict.get('explanation', '')}"
                f" 风险边界：{conflict_resolution.get('riskBoundary', '')}"
            )

    seen = set()
    ordered_rule_ids = []
    for rule_id in rule_ids:
        if rule_id and rule_id not in seen:
            seen.add(rule_id)
            ordered_rule_ids.append(rule_id)
    return {
        "schemaVersion": 1,
        "format": "markdown",
        "markdown": "\n".join(lines),
        "ruleIds": ordered_rule_ids,
        "riskBoundary": conflict_resolution.get("riskBoundary", ""),
    }


def _conflict_explanation(primary_rule: dict[str, Any], secondary_rules: list[dict[str, Any]]) -> str:
    primary_id = str(primary_rule.get("ruleId", ""))
    secondary_ids = [str(item.get("ruleId", "")) for item in secondary_rules if item.get("ruleId")]
    if not secondary_ids:
        return f"{primary_id} 为当前冲突组唯一可用证据，按风险边界直接保留。"
    return f"{primary_id} 的层级、置信度或权重优先；{'、'.join(secondary_ids)} 作为辅助证据保留，不覆盖主规则。"


def _conflict_discounts(primary_rule: dict[str, Any], secondary_rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """给辅助规则自动降权说明，避免冲突被读成同等强结论。"""
    primary_confidence = float(primary_rule.get("confidence", 0.0))
    discounts = []
    for item in secondary_rules:
        confidence = float(item.get("confidence", 0.0))
        delta = round(max(0.0, primary_confidence - confidence), 2)
        discounts.append(
            {
                "ruleId": item.get("ruleId", ""),
                "discount": delta,
                "reason": "辅助规则置信度或层级低于主规则，只保留为旁证。",
            }
        )
    return discounts


def _counter_evidence(primary_rule: dict[str, Any], secondary_rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """解释为什么没有采用其他规则作为主结论。"""
    return [
        {
            "rejectedRule": item.get("ruleId", ""),
            "whyNotPrimary": f"{item.get('ruleId', '')} 的边界为：{item.get('riskBoundary', '')}",
            "primaryRule": primary_rule.get("ruleId", ""),
        }
        for item in secondary_rules
    ]
