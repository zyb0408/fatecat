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
