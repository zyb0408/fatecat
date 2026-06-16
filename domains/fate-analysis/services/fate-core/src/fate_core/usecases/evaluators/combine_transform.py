from __future__ import annotations

from typing import Any

from fate_core.usecases.evaluators.constants import (
    BRANCH_ELEMENT,
    ELEMENT_STEMS,
    GAN_ELEMENT,
    TRANSFORM_ELEMENT_BY_PAIR,
)
from fate_core.usecases.evaluators.relation import condition, relation_blockers
from fate_core.usecases.rule_depth import rules_for_system


def _pillar_items(raw: dict[str, Any]) -> list[dict[str, Any]]:
    pillars = raw.get("fourPillars", {}) if isinstance(raw.get("fourPillars"), dict) else {}
    hidden_stems = raw.get("hiddenStems", {}) if isinstance(raw.get("hiddenStems"), dict) else {}
    labels = {"year": "年柱", "month": "月柱", "day": "日柱", "hour": "时柱"}
    items: list[dict[str, Any]] = []
    for name in ["year", "month", "day", "hour"]:
        pillar = pillars.get(name, {}) if isinstance(pillars.get(name), dict) else {}
        stem = str(pillar.get("stem", ""))
        branch = str(pillar.get("branch", ""))
        hidden = hidden_stems.get(name, []) if isinstance(hidden_stems, dict) else []
        items.append(
            {
                "position": name,
                "label": labels[name],
                "stem": stem,
                "branch": branch,
                "stemElement": GAN_ELEMENT.get(stem, ""),
                "branchElement": BRANCH_ELEMENT.get(branch, ""),
                "hiddenStems": hidden if isinstance(hidden, list) else [],
            }
        )
    return items


def _branch_supports_element(branch: str, hidden: list[Any], element: str) -> bool:
    if BRANCH_ELEMENT.get(branch) == element:
        return True
    return any(GAN_ELEMENT.get(str(stem)) == element for stem in hidden)


def _state_contracts() -> dict[str, dict[str, Any]]:
    rule = next(
        (item for item in rules_for_system("bazi") if item.get("id") == "bazi.depth.relation.combine_transform_guard"),
        {},
    )
    matrix = rule.get("transformStateMatrix", []) if isinstance(rule, dict) else []
    return {str(item.get("state")): item for item in matrix if isinstance(item, dict)}


def _contested_positions(pairs: list[tuple[dict[str, Any], dict[str, Any]]]) -> set[str]:
    counts: dict[str, int] = {}
    for left, right in pairs:
        counts[left["position"]] = counts.get(left["position"], 0) + 1
        counts[right["position"]] = counts.get(right["position"], 0) + 1
    return {position for position, count in counts.items() if count > 1}


def build_combine_transform_matrix(raw: dict[str, Any]) -> dict[str, Any]:
    """登记合化候选的条件链；缺条件时只保留合象，不输出成化断语。"""
    items = _pillar_items(raw)
    stems_present = [item for item in items if item["stem"]]
    month = next((item for item in items if item["position"] == "month"), {})
    transform_pairs: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for index, left in enumerate(stems_present):
        for right in stems_present[index + 1 :]:
            if TRANSFORM_ELEMENT_BY_PAIR.get(frozenset({left["stem"], right["stem"]})):
                transform_pairs.append((left, right))
    contested_positions = _contested_positions(transform_pairs)

    candidates: list[dict[str, Any]] = []
    for left, right in transform_pairs:
        transform_element = TRANSFORM_ELEMENT_BY_PAIR[frozenset({left["stem"], right["stem"]})]
        transform_stems = ELEMENT_STEMS.get(transform_element, set())
        stem_transparent = any(item["stem"] in transform_stems for item in items)
        rooted_positions = [
            item["position"]
            for item in items
            if _branch_supports_element(item["branch"], item["hiddenStems"], transform_element)
        ]
        month_support = _branch_supports_element(
            str(month.get("branch", "")), list(month.get("hiddenStems", [])), transform_element
        )
        blockers = relation_blockers(raw, {left["position"], right["position"]})
        contested = not blockers and bool({left["position"], right["position"]} & contested_positions)
        conditions = [
            condition("paired_stems_present", True, [left["stem"], right["stem"]]),
            condition("month_command_supports_transform_element", month_support, month),
            condition("transform_element_transparent", stem_transparent, sorted(transform_stems)),
            condition("transform_element_rooted", bool(rooted_positions), rooted_positions),
            condition("no_direct_blocker", not blockers, blockers),
        ]
        score = sum([20, 25 if month_support else 0, 20 if stem_transparent else 0, 20 if rooted_positions else 0])
        if blockers or contested:
            score -= 15
        status = (
            "formed_candidate"
            if score >= 75 and not blockers and not contested
            else "guarded_candidate"
            if score >= 45
            else "weak_candidate"
        )
        state = (
            "transform_broken"
            if blockers
            else "contested_transform"
            if contested
            else "transform_success"
            if score >= 75
            else "transform_candidate"
            if score >= 45
            else "structural_relation"
        )
        candidates.append(
            {
                "pair": [left["stem"], right["stem"]],
                "positions": [left["position"], right["position"]],
                "transformElement": transform_element,
                "score": max(0, min(100, score)),
                "status": status,
                "state": state,
                "conditions": conditions,
                "boundary": "合化成败必须同时看月令、透干、通根和阻隔；这里不把合象直接写成成化。",
            }
        )

    return {
        "schemaVersion": 1,
        "status": "has_candidates" if candidates else "no_direct_stem_pair",
        "stateCatalog": [
            "structural_relation",
            "transform_candidate",
            "transform_success",
            "transform_broken",
            "contested_transform",
        ],
        "stateContracts": _state_contracts(),
        "conditionCatalog": [
            "paired_stems_present",
            "month_command_supports_transform_element",
            "transform_element_transparent",
            "transform_element_rooted",
            "no_direct_blocker",
        ],
        "candidates": candidates,
        "riskBoundary": "缺少完整条件链时只登记合象或候选，不宣称已经成化。",
    }
