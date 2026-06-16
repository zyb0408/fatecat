from __future__ import annotations

from typing import Any

TEN_GOD_FAMILIES = {
    "财": ["正财", "偏财"],
    "官杀": ["正官", "七杀"],
    "印": ["正印", "偏印"],
    "食伤": ["食神", "伤官"],
    "比劫": ["比肩", "劫财"],
}


def ten_god_values(value: Any) -> list[str]:
    values: list[str] = []
    if isinstance(value, dict):
        for item in value.values():
            values.extend(ten_god_values(item))
    elif isinstance(value, list):
        for item in value:
            values.extend(ten_god_values(item))
    elif value not in (None, ""):
        values.append(str(value))
    return values


def ten_god_families(counts: Any) -> dict[str, int]:
    if not isinstance(counts, dict):
        return {}
    return {
        family: sum(int(counts.get(name, 0)) for name in names if isinstance(counts.get(name, 0), int | float))
        for family, names in TEN_GOD_FAMILIES.items()
    }


def dominant_counts(counts: Any, *, limit: int) -> list[dict[str, Any]]:
    if not isinstance(counts, dict):
        return []
    items = sorted(
        ((str(name), int(value)) for name, value in counts.items() if isinstance(value, int | float)),
        key=lambda item: item[1],
        reverse=True,
    )
    return [{"name": name, "count": count} for name, count in items[:limit]]


def _ten_god_position_evidence(raw: dict[str, Any]) -> list[dict[str, Any]]:
    """把十神统计还原到柱位、透干和藏干证据。"""
    ten_gods = raw.get("tenGods", {}) if isinstance(raw.get("tenGods"), dict) else {}
    hidden_stems = raw.get("hiddenStems", {}) if isinstance(raw.get("hiddenStems"), dict) else {}
    positions: list[dict[str, Any]] = []
    for pillar in ("year", "month", "day", "hour"):
        pillar_ten_gods = ten_gods.get(pillar, {}) if isinstance(ten_gods.get(pillar), dict) else {}
        stem_ten_god = pillar_ten_gods.get("stem")
        if stem_ten_god:
            positions.append(
                {
                    "pillar": pillar,
                    "source": "stem",
                    "tenGod": stem_ten_god,
                    "evidenceField": f"tenGods.{pillar}.stem",
                }
            )
        branch_ten_gods = pillar_ten_gods.get("branch", [])
        branch_hidden_stems = hidden_stems.get(pillar, [])
        if not isinstance(branch_ten_gods, list):
            branch_ten_gods = [branch_ten_gods]
        if not isinstance(branch_hidden_stems, list):
            branch_hidden_stems = [branch_hidden_stems]
        for index, ten_god in enumerate(branch_ten_gods):
            if not ten_god:
                continue
            positions.append(
                {
                    "pillar": pillar,
                    "source": "hiddenStem",
                    "hiddenStem": branch_hidden_stems[index] if index < len(branch_hidden_stems) else "",
                    "tenGod": ten_god,
                    "evidenceField": f"tenGods.{pillar}.branch[{index}]",
                }
            )
    return positions


def build_ten_god_structure(raw: dict[str, Any]) -> dict[str, Any]:
    ten_gods = ten_god_values(raw.get("tenGods", {}))
    ten_god_counts = {name: ten_gods.count(name) for name in sorted(set(ten_gods)) if name}
    return {
        "counts": ten_god_counts,
        "basis": "从 tenGods 字段递归统计，仅作结构摘要。",
        "basisEvidence": _ten_god_position_evidence(raw),
        "dominant": dominant_counts(ten_god_counts, limit=5),
        "families": ten_god_families(ten_god_counts),
        "sourceRuleId": "bazi.ten_god_structure",
        "evidenceFields": ["tenGods", "hiddenStems", "baziBenchmark.tenGodStructure.basisEvidence"],
        "riskBoundary": "十神结构必须回到柱位、透干和藏干证据，不用单一十神输出确定人生断语。",
        "ruleIds": ["bazi.ten_god_structure"],
    }
