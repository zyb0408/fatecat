from __future__ import annotations

from typing import Any

from fate_core.usecases.evaluators.regular_pattern import pattern_matrix_contracts
from fate_core.usecases.evaluators.relation import condition
from fate_core.usecases.evaluators.ten_god import ten_god_families, ten_god_values


def _score_status(score: int, *, candidate_at: int = 80, guarded_at: int = 30) -> str:
    if score >= candidate_at:
        return "candidate"
    if score >= guarded_at:
        return "guarded"
    return "not_supported"


def build_special_pattern_candidates(raw: dict[str, Any], combine_matrix: dict[str, Any]) -> dict[str, Any]:
    """登记从格、化气、专旺、假从等高级格局候选；缺证据时不定格。"""
    day_master = raw.get("dayMaster", {}) if isinstance(raw.get("dayMaster"), dict) else {}
    strength_label = str(day_master.get("strength", ""))
    strength = raw.get("wuxingScores", {}) if isinstance(raw.get("wuxingScores"), dict) else {}
    strong_score = strength.get("strongScore")
    ten_god_counts = ten_god_families(
        {
            name: ten_god_values(raw.get("tenGods", {})).count(name)
            for name in set(ten_god_values(raw.get("tenGods", {})))
        }
    )
    support_self = int(ten_god_counts.get("印", 0)) + int(ten_god_counts.get("比劫", 0))
    dominant_family = max(ten_god_counts.items(), key=lambda item: item[1], default=("", 0))
    has_transform_candidate = bool(combine_matrix.get("candidates"))
    weak = "弱" in strength_label
    strong = bool(isinstance(strong_score, int | float) and strong_score >= 30)

    definitions = [
        (
            "从格",
            [
                condition("day_master_weak", weak, strength_label),
                condition("self_support_low", support_self <= 2, support_self),
                condition("external_family_dominant", dominant_family[0] in {"财", "官杀", "食伤"}, dominant_family),
            ],
        ),
        (
            "化气",
            [
                condition(
                    "combine_transform_candidate_exists", has_transform_candidate, combine_matrix.get("candidates", [])
                ),
                condition(
                    "candidate_has_condition_chain",
                    bool(combine_matrix.get("conditionCatalog")),
                    combine_matrix.get("conditionCatalog"),
                ),
            ],
        ),
        (
            "专旺",
            [
                condition("day_master_strong", strong, {"label": strength_label, "strongScore": strong_score}),
                condition("self_support_dominant", support_self >= max(3, dominant_family[1]), ten_god_counts),
            ],
        ),
        (
            "假从",
            [
                condition("day_master_weak", weak, strength_label),
                condition("self_support_present_but_not_dominant", 0 < support_self <= 4, support_self),
                condition("external_family_dominant", dominant_family[0] in {"财", "官杀", "食伤"}, dominant_family),
            ],
        ),
        (
            "从杀",
            [
                condition("day_master_weak", weak, strength_label),
                condition("official_killing_dominant", dominant_family[0] == "官杀", ten_god_counts),
            ],
        ),
        (
            "从财",
            [
                condition("day_master_weak", weak, strength_label),
                condition("wealth_dominant", dominant_family[0] == "财", ten_god_counts),
            ],
        ),
    ]
    candidates = []
    pattern_contracts = pattern_matrix_contracts()
    for name, conditions in definitions:
        met_count = sum(1 for item in conditions if item["met"])
        score = int(round(100 * met_count / len(conditions)))
        contract = pattern_contracts.get(name, {})
        counter_evidence = [item for item in conditions if not item["met"]]
        candidates.append(
            {
                "name": name,
                "score": score,
                "status": _score_status(score),
                "sourceRuleId": contract.get("sourceRuleId", "bazi.pattern_by_month_command"),
                "maturity": {
                    "basis": "condition_chain",
                    "metConditions": met_count,
                    "totalConditions": len(conditions),
                },
                "conditions": conditions,
                "appliesWhen": contract.get("appliesWhen", [item["name"] for item in conditions]),
                "breaksWhen": contract.get("breaksWhen", ["关键条件缺失", "反证条件存在", "缺少对应正反例 golden"]),
                "counterEvidence": counter_evidence,
                "lifecycle": "beta",
                "lifecycleGate": "提升为 production 需要对应高级格局正反例 golden、rule-depth 回归和报告风险边界同时通过。",
                "boundary": contract.get("riskBoundary", "特殊格局只登记候选成熟度；未达到完整成败条件时不得定格。"),
            }
        )
    return {
        "schemaVersion": 1,
        "candidates": candidates,
        "dominantFamily": {"name": dominant_family[0], "count": dominant_family[1]},
        "selfSupportCount": support_self,
        "riskBoundary": "从格、化气、专旺、假从等高级格局必须有专门 golden case 才能提升为定格。",
    }
