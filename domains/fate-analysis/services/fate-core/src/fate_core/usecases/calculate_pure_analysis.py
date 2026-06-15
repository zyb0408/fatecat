from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from fate_core.adapters import LegacyBaziInput
from fate_core.kernel import project_by_profile
from fate_core.providers import (
    build_base_chart_section,
    build_classical_section,
    build_fortune_section,
    build_pure_analysis_runtime,
)
from fate_core.usecases.rule_depth import (
    build_combination_statement,
    build_conflict_resolution,
    build_narrative_summary,
    build_rule_application,
    build_weight_profile,
    collect_source_rule_ids,
    registry_version,
    rules_for_system,
)


@dataclass(frozen=True)
class PureAnalysisInput:
    """纯命理分析用例输入。"""

    birth_dt: datetime
    gender: str
    longitude: float
    latitude: float
    name: str | None = None
    birth_place: str = ""
    use_true_solar_time: bool = True


def _first_non_empty(*values: Any) -> Any:
    for value in values:
        if value not in (None, ""):
            return value
    return None


def _parse_bool(value: Any, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "y", "on", "是"}:
        return True
    if normalized in {"0", "false", "no", "n", "off", "否"}:
        return False
    raise ValueError(f"无法解析布尔值: {value}")


def parse_datetime(value: str) -> datetime:
    """解析出生时间，兼容 CLI/API 常见输入格式。"""
    normalized = value.strip()
    if not normalized:
        raise ValueError("birthDateTime 不能为空")
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
        return parsed.replace(tzinfo=None) if parsed.tzinfo else parsed
    except ValueError:
        pass
    for time_format in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M:%S", "%Y/%m/%d %H:%M"):
        try:
            return datetime.strptime(normalized, time_format)
        except ValueError:
            continue
    raise ValueError(f"无法解析出生时间: {value}")


def normalize_gender(gender: str) -> str:
    """把人类输入统一成底层计算器使用的性别枚举。"""
    normalized = str(gender).strip().lower()
    if normalized in {"male", "m", "man", "boy", "男", "男性", "乾", "乾造"}:
        return "male"
    if normalized in {"female", "f", "woman", "girl", "女", "女性", "坤", "坤造"}:
        return "female"
    raise ValueError(f"无法识别性别: {gender}")


def normalize_pure_analysis_payload(raw_payload: dict[str, Any]) -> dict[str, Any]:
    """把 CLI/API/Capability 输入统一成纯分析用例字段。"""
    birth_place_value = raw_payload.get("birthPlace")
    birth_place_object: dict[str, Any] = birth_place_value if isinstance(birth_place_value, dict) else {}
    raw_options = raw_payload.get("options")
    options: dict[str, Any] = raw_options if isinstance(raw_options, dict) else {}

    birth_datetime = _first_non_empty(
        raw_payload.get("birthDateTime"),
        raw_payload.get("birth_datetime"),
        raw_payload.get("birth_dt"),
        raw_payload.get("datetime"),
    )
    if not birth_datetime and raw_payload.get("birthDate") and raw_payload.get("birthTime"):
        birth_datetime = f"{raw_payload['birthDate']} {raw_payload['birthTime']}"

    longitude = _first_non_empty(
        raw_payload.get("longitude"),
        raw_payload.get("lng"),
        birth_place_object.get("longitude"),
        birth_place_object.get("lng"),
    )
    latitude = _first_non_empty(
        raw_payload.get("latitude"),
        raw_payload.get("lat"),
        birth_place_object.get("latitude"),
        birth_place_object.get("lat"),
    )
    birth_place_name = _first_non_empty(
        raw_payload.get("birth_place"),
        raw_payload.get("birthPlaceName"),
        birth_place_value if isinstance(birth_place_value, str) else None,
        birth_place_object.get("name"),
    )
    use_true_solar_time = _first_non_empty(
        raw_payload.get("useTrueSolarTime"),
        raw_payload.get("use_true_solar_time"),
        options.get("useTrueSolarTime"),
    )

    normalized = {
        "birthDateTime": birth_datetime,
        "gender": _first_non_empty(raw_payload.get("gender"), raw_payload.get("sex")),
        "longitude": longitude,
        "latitude": latitude,
        "name": raw_payload.get("name"),
        "birthPlace": birth_place_name or "",
        "useTrueSolarTime": _parse_bool(use_true_solar_time, default=True),
    }
    missing = [
        field for field in ("birthDateTime", "gender", "longitude", "latitude") if normalized[field] in (None, "")
    ]
    if missing:
        raise ValueError(f"缺少必填字段: {', '.join(missing)}")
    normalized["longitude"] = float(normalized["longitude"])
    normalized["latitude"] = float(normalized["latitude"])
    normalized["gender"] = normalize_gender(str(normalized["gender"]))
    return normalized


def build_pure_analysis_input_from_payload(raw_payload: dict[str, Any]) -> PureAnalysisInput:
    """从统一 payload 构造纯分析输入。"""
    normalized = normalize_pure_analysis_payload(raw_payload)
    return PureAnalysisInput(
        birth_dt=parse_datetime(str(normalized["birthDateTime"])),
        gender=str(normalized["gender"]),
        longitude=normalized["longitude"],
        latitude=normalized["latitude"],
        name=normalized["name"],
        birth_place=str(normalized["birthPlace"]),
        use_true_solar_time=normalized["useTrueSolarTime"],
    )


def _evidence_item(
    *,
    conclusion: dict[str, Any],
    basis: list[str],
    sources: list[str],
    rule_ids: list[str],
    weight: str = "core",
) -> dict[str, Any]:
    return {
        "conclusion": conclusion,
        "basis": basis,
        "sources": sources,
        "ruleIds": rule_ids,
        "weight": weight,
        "visibility": "audit",
    }


def _build_accuracy_guards(runtime: Any, raw: dict[str, Any]) -> dict[str, Any]:
    """装配综合八字准确性二期的关键边界证据。"""
    calculator = runtime.calculator
    ec = runtime.ec
    true_solar_detail = raw.get("completeTrueSolarTime", {})
    jieqi_detail = raw.get("jieqiDetail", {})
    jiao_yun = raw.get("jiaoYun", {})
    geju = raw.get("geju", {})
    yong_shen = raw.get("yongShen", {})

    return {
        "schemaVersion": 1,
        "timePipeline": {
            "inputLocalTime": runtime.payload.birth_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "useTrueSolarTime": runtime.payload.use_true_solar_time,
            "trueSolarTime": calculator.true_solar_time.strftime("%Y-%m-%d %H:%M:%S"),
            "longitude": runtime.payload.longitude,
            "latitude": runtime.payload.latitude,
            "longitudeOffsetMinutes": true_solar_detail.get("longitudeOffsetMinutes"),
            "astronomicalOffsetMinutes": true_solar_detail.get("astronomicalOffsetMinutes"),
            "totalOffsetMinutes": true_solar_detail.get("totalOffsetMinutes"),
            "ziTimeAnalysis": raw.get("ziTimeAnalysis", {}),
        },
        "solarTermBoundary": {
            "yearPillar": ec.getYear(),
            "monthPillar": ec.getMonth(),
            "monthCommand": ec.getMonthZhi(),
            "previousTerm": jieqi_detail.get("prevJieQi", {}),
            "nextTerm": jieqi_detail.get("nextJieQi", {}),
            "description": jieqi_detail.get("description", ""),
        },
        "fortuneStartBoundary": {
            "gender": runtime.payload.gender,
            "startDate": jiao_yun.get("startDate"),
            "description": jiao_yun.get("description", ""),
            "anchorTerm": jiao_yun.get("jiaoJieQi", ""),
        },
        "patternUseGodTrace": {
            "mainPattern": geju.get("main", "") if isinstance(geju, dict) else "",
            "patterns": geju.get("patterns", []) if isinstance(geju, dict) else [],
            "monthPillar": ec.getMonth(),
            "monthHiddenStems": runtime.hidden_stems.get("month", []),
            "yongShenBasis": yong_shen.get("basis", "") if isinstance(yong_shen, dict) else "",
            "yongShenBasisSource": yong_shen.get("basisSource", "") if isinstance(yong_shen, dict) else "",
            "tiaohouRaw": yong_shen.get("tiaohouRaw", "") if isinstance(yong_shen, dict) else "",
        },
    }


def _append_accuracy_evidence(runtime: Any, raw: dict[str, Any]) -> None:
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
    items["timePipeline"] = _evidence_item(
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
    items["solarTermBoundary"] = _evidence_item(
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
    items["fortuneStartBoundary"] = _evidence_item(
        conclusion={
            "startDate": fortune_start.get("startDate"),
            "anchorTerm": fortune_start.get("anchorTerm"),
        },
        basis=[f"性别={runtime.payload.gender}", f"起运说明={fortune_start.get('description', '')}"],
        sources=["lunar-python EightChar.getYun", "项目起运边界回归"],
        rule_ids=["bazi.fortune_start_boundary"],
        weight="fortune",
    )
    items["patternUseGodTrace"] = _evidence_item(
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


GAN_ELEMENT = {
    "甲": "木",
    "乙": "木",
    "丙": "火",
    "丁": "火",
    "戊": "土",
    "己": "土",
    "庚": "金",
    "辛": "金",
    "壬": "水",
    "癸": "水",
}
BRANCH_ELEMENT = {
    "子": "水",
    "丑": "土",
    "寅": "木",
    "卯": "木",
    "辰": "土",
    "巳": "火",
    "午": "火",
    "未": "土",
    "申": "金",
    "酉": "金",
    "戌": "土",
    "亥": "水",
}
ELEMENT_STEMS = {
    "木": {"甲", "乙"},
    "火": {"丙", "丁"},
    "土": {"戊", "己"},
    "金": {"庚", "辛"},
    "水": {"壬", "癸"},
}
TRANSFORM_ELEMENT_BY_PAIR = {
    frozenset({"甲", "己"}): "土",
    frozenset({"乙", "庚"}): "金",
    frozenset({"丙", "辛"}): "水",
    frozenset({"丁", "壬"}): "木",
    frozenset({"戊", "癸"}): "火",
}


def _ten_god_values(value: Any) -> list[str]:
    values: list[str] = []
    if isinstance(value, dict):
        for item in value.values():
            values.extend(_ten_god_values(item))
    elif isinstance(value, list):
        for item in value:
            values.extend(_ten_god_values(item))
    elif value not in (None, ""):
        values.append(str(value))
    return values


def _relation_order(raw: dict[str, Any]) -> list[dict[str, Any]]:
    """把干支关系按审计优先级整理成稳定结构。"""
    relations = raw.get("ganzhiRelations", {}) if isinstance(raw.get("ganzhiRelations"), dict) else {}
    branch_rel = raw.get("branchRelations", {}) if isinstance(raw.get("branchRelations"), dict) else {}
    extra = raw.get("ganzhiExtra", {}) if isinstance(raw.get("ganzhiExtra"), dict) else {}
    groups = [
        ("hehua", "合化", relations.get("tianGan", []), "先记录天干五合；是否成化需要后续条件字段确认。"),
        ("sanHui", "三会", branch_rel.get("sanHuiDetail") or branch_rel.get("sanHui", []), "三会优先于三合展示。"),
        ("sanHe", "三合", branch_rel.get("sanHeDetail") or branch_rel.get("sanHe", []), "完整三合优先于半合。"),
        ("liuHe", "六合", branch_rel.get("liuHeDetail") or branch_rel.get("liuHe", []), "六合作为结构辅助关系。"),
        (
            "conflict",
            "冲刑害破",
            branch_rel.get("conflictsDetail") or branch_rel.get("conflicts", []),
            "动态触发时优先进入运势证据。",
        ),
        ("ku", "入库", extra.get("kuDetail", {}), "库气与入库只作为结构证据，不单独决定喜忌。"),
    ]
    ordered = []
    for priority, (key, label, value, boundary) in enumerate(groups, start=1):
        count = len(value) if isinstance(value, (list, dict)) else (1 if value else 0)
        ordered.append(
            {
                "key": key,
                "label": label,
                "priority": priority,
                "count": count,
                "items": value,
                "boundary": boundary,
            }
        )
    return ordered


def _fortune_triggers(raw: dict[str, Any]) -> list[dict[str, Any]]:
    """抽取岁运触发点：只做结构提示，不输出确定性断语。"""
    pillars = raw.get("fourPillars", {}) if isinstance(raw.get("fourPillars"), dict) else {}
    day_pillar = pillars.get("day", {}) if isinstance(pillars.get("day"), dict) else {}
    day_gz = day_pillar.get("fullName", "")
    major = raw.get("majorFortune", {}) if isinstance(raw.get("majorFortune"), dict) else {}
    major_pillars = major.get("pillars", []) if isinstance(major.get("pillars"), list) else []
    annual = raw.get("annualFortune", []) if isinstance(raw.get("annualFortune"), list) else []
    triggers: list[dict[str, Any]] = []
    active_major = next((item for item in major_pillars if isinstance(item, dict) and item.get("isCurrent")), None)
    active_major_gz = (active_major or {}).get("ganZhi") or (active_major or {}).get("fullName", "")
    for item in annual[:24]:
        if not isinstance(item, dict):
            continue
        gz = item.get("ganZhi") or item.get("fullName", "")
        reasons = []
        if gz and gz == day_gz:
            reasons.append("流年与日柱伏吟")
        if gz and active_major_gz and gz == active_major_gz:
            reasons.append("岁运并临")
        if len(gz) >= 2 and len(day_gz) >= 2 and gz[1] == day_gz[1]:
            reasons.append("流年地支与日支同气")
        if reasons:
            triggers.append(
                {
                    "year": item.get("year"),
                    "ganZhi": gz,
                    "activeMajorFortune": active_major_gz,
                    "reasons": reasons,
                    "riskBoundary": "只作趋势触发证据，不作确定未来断语。",
                }
            )
    return triggers


def _build_yongshen_strategies(raw: dict[str, Any]) -> list[dict[str, Any]]:
    yong_shen = raw.get("yongShen", {}) if isinstance(raw.get("yongShen"), dict) else {}
    day_master = raw.get("dayMaster", {}) if isinstance(raw.get("dayMaster"), dict) else {}
    strength = str(day_master.get("strength", ""))
    tiao_hou = yong_shen.get("tiaoHou", {}) if isinstance(yong_shen.get("tiaoHou"), dict) else {}
    strategies = [
        {
            "strategy": "调候",
            "conclusion": tiao_hou,
            "basis": yong_shen.get("basis", ""),
            "source": yong_shen.get("basisSource", ""),
            "ruleIds": ["bazi.regulating_climate"],
        },
        {
            "strategy": "扶抑",
            "conclusion": "偏弱先看印比扶助；偏强先看泄耗制化；中和以格局和调候优先。",
            "basis": f"日主强弱={strength}",
            "source": "项目扶抑策略边界",
            "ruleIds": ["bazi.day_master_strength", "bazi.balance_five_elements"],
        },
        {
            "strategy": "通关",
            "conclusion": "仅在合冲克战明显时作为冲突调解策略登记。",
            "basis": raw.get("ganzhiRelations", {}),
            "source": "项目干支关系规则",
            "ruleIds": ["bazi.stem_branch_relations"],
        },
        {
            "strategy": "病药",
            "conclusion": "以五行偏枯、寒暖燥湿和格局成败共同判断，当前只登记依据不作强断。",
            "basis": raw.get("climateScores", {}),
            "source": "项目调候与五行平衡规则",
            "ruleIds": ["bazi.regulating_climate", "bazi.balance_five_elements"],
        },
    ]
    return strategies


def _pillar_items(raw: dict[str, Any]) -> list[dict[str, Any]]:
    pillars = raw.get("fourPillars", {}) if isinstance(raw.get("fourPillars"), dict) else {}
    hidden_stems = raw.get("hiddenStems", {}) if isinstance(raw.get("hiddenStems"), dict) else {}
    items: list[dict[str, Any]] = []
    for name, label in [("year", "年"), ("month", "月"), ("day", "日"), ("hour", "时")]:
        pillar = pillars.get(name, {}) if isinstance(pillars.get(name), dict) else {}
        stem = str(pillar.get("stem", ""))
        branch = str(pillar.get("branch", ""))
        hidden = hidden_stems.get(name, [])
        items.append(
            {
                "position": name,
                "label": label,
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


def _relation_blockers(raw: dict[str, Any], positions: set[str]) -> list[str]:
    blockers: list[str] = []
    branch_rel = raw.get("branchRelations", {}) if isinstance(raw.get("branchRelations"), dict) else {}
    for item in branch_rel.get("conflictsDetail", []) if isinstance(branch_rel.get("conflictsDetail"), list) else []:
        if not isinstance(item, dict):
            continue
        if item.get("rel") not in {"冲", "刑", "被刑", "害", "破"}:
            continue
        if item.get("from") in positions or any(str(target) in positions for target in item.get("to", [])):
            blockers.append(str(item.get("text", "")))
    extra = raw.get("ganzhiExtra", {}) if isinstance(raw.get("ganzhiExtra"), dict) else {}
    for item in extra.get("keDetail", []) if isinstance(extra.get("keDetail"), list) else []:
        if isinstance(item, dict) and {item.get("from"), item.get("to")} & positions:
            blockers.append(str(item.get("text", "")))
    return [item for item in blockers if item][:8]


def _condition(name: str, met: bool, evidence: Any) -> dict[str, Any]:
    return {"name": name, "met": bool(met), "evidence": evidence}


def _build_combine_transform_matrix(raw: dict[str, Any]) -> dict[str, Any]:
    """登记合化候选的条件链；缺条件时只保留合象，不输出成化断语。"""
    items = _pillar_items(raw)
    stems_present = [item for item in items if item["stem"]]
    month = next((item for item in items if item["position"] == "month"), {})
    candidates: list[dict[str, Any]] = []
    for index, left in enumerate(stems_present):
        for right in stems_present[index + 1 :]:
            transform_element = TRANSFORM_ELEMENT_BY_PAIR.get(frozenset({left["stem"], right["stem"]}))
            if not transform_element:
                continue
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
            blockers = _relation_blockers(raw, {left["position"], right["position"]})
            conditions = [
                _condition("paired_stems_present", True, [left["stem"], right["stem"]]),
                _condition("month_command_supports_transform_element", month_support, month),
                _condition("transform_element_transparent", stem_transparent, sorted(transform_stems)),
                _condition("transform_element_rooted", bool(rooted_positions), rooted_positions),
                _condition("no_direct_blocker", not blockers, blockers),
            ]
            score = sum([20, 25 if month_support else 0, 20 if stem_transparent else 0, 20 if rooted_positions else 0])
            if blockers:
                score -= 15
            status = "formed_candidate" if score >= 75 and not blockers else "guarded_candidate" if score >= 45 else "weak_candidate"
            candidates.append(
                {
                    "pair": [left["stem"], right["stem"]],
                    "positions": [left["position"], right["position"]],
                    "transformElement": transform_element,
                    "score": max(0, min(100, score)),
                    "status": status,
                    "conditions": conditions,
                    "boundary": "合化成败必须同时看月令、透干、通根和阻隔；这里不把合象直接写成成化。",
                }
            )
    return {
        "schemaVersion": 1,
        "status": "has_candidates" if candidates else "no_direct_stem_pair",
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


def _score_status(score: int, *, candidate_at: int = 80, guarded_at: int = 30) -> str:
    if score >= candidate_at:
        return "candidate"
    if score >= guarded_at:
        return "guarded"
    return "not_supported"


def _build_special_pattern_candidates(raw: dict[str, Any], combine_matrix: dict[str, Any]) -> dict[str, Any]:
    day_master = raw.get("dayMaster", {}) if isinstance(raw.get("dayMaster"), dict) else {}
    strength_label = str(day_master.get("strength", ""))
    strength = raw.get("wuxingScores", {}) if isinstance(raw.get("wuxingScores"), dict) else {}
    strong_score = strength.get("strongScore")
    ten_god_counts = _ten_god_families(
        {
            name: _ten_god_values(raw.get("tenGods", {})).count(name)
            for name in set(_ten_god_values(raw.get("tenGods", {})))
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
                _condition("day_master_weak", weak, strength_label),
                _condition("self_support_low", support_self <= 2, support_self),
                _condition("external_family_dominant", dominant_family[0] in {"财", "官杀", "食伤"}, dominant_family),
            ],
        ),
        (
            "化气",
            [
                _condition("combine_transform_candidate_exists", has_transform_candidate, combine_matrix.get("candidates", [])),
                _condition("candidate_has_condition_chain", bool(combine_matrix.get("conditionCatalog")), combine_matrix.get("conditionCatalog")),
            ],
        ),
        (
            "专旺",
            [
                _condition("day_master_strong", strong, {"label": strength_label, "strongScore": strong_score}),
                _condition("self_support_dominant", support_self >= max(3, dominant_family[1]), ten_god_counts),
            ],
        ),
        (
            "假从",
            [
                _condition("day_master_weak", weak, strength_label),
                _condition("self_support_present_but_not_dominant", 0 < support_self <= 4, support_self),
                _condition("external_family_dominant", dominant_family[0] in {"财", "官杀", "食伤"}, dominant_family),
            ],
        ),
        (
            "从杀",
            [
                _condition("day_master_weak", weak, strength_label),
                _condition("official_killing_dominant", dominant_family[0] == "官杀", ten_god_counts),
            ],
        ),
        (
            "从财",
            [
                _condition("day_master_weak", weak, strength_label),
                _condition("wealth_dominant", dominant_family[0] == "财", ten_god_counts),
            ],
        ),
    ]
    candidates = []
    for name, conditions in definitions:
        met_count = sum(1 for item in conditions if item["met"])
        score = int(round(100 * met_count / len(conditions)))
        candidates.append(
            {
                "name": name,
                "score": score,
                "status": _score_status(score),
                "conditions": conditions,
                "boundary": "特殊格局只登记候选成熟度；未达到完整成败条件时不得定格。",
            }
        )
    return {
        "schemaVersion": 1,
        "candidates": candidates,
        "dominantFamily": {"name": dominant_family[0], "count": dominant_family[1]},
        "selfSupportCount": support_self,
        "riskBoundary": "从格、化气、专旺、假从等高级格局必须有专门 golden case 才能提升为定格。",
    }


def _five_element_spread(raw: dict[str, Any]) -> int:
    scores = raw.get("wuxingScores", {}).get("fiveElementScore", {}) if isinstance(raw.get("wuxingScores"), dict) else {}
    values = [int(value) for value in scores.values() if isinstance(value, int | float)]
    return max(values) - min(values) if values else 0


def _build_yongshen_decision(raw: dict[str, Any], strategies: list[dict[str, Any]]) -> dict[str, Any]:
    strategy_names = {str(item.get("strategy")): item for item in strategies if isinstance(item, dict)}
    relation_count = sum(item.get("count", 0) for item in _relation_order(raw) if isinstance(item.get("count"), int))
    spread = _five_element_spread(raw)
    climate_band = _temperature_band(raw.get("climateScores", {}))
    strength = raw.get("wuxingScores", {}) if isinstance(raw.get("wuxingScores"), dict) else {}
    yong_shen = raw.get("yongShen", {}) if isinstance(raw.get("yongShen"), dict) else {}
    scored = [
        {
            "strategy": "调候",
            "score": min(100, 35 + (25 if yong_shen.get("basis") else 0) + (20 if yong_shen.get("tiaohouRaw") else 0)),
            "evidenceFields": ["yongShen.basis", "yongShen.tiaohouRaw", "climateScores"],
            "source": strategy_names.get("调候", {}).get("source", ""),
        },
        {
            "strategy": "扶抑",
            "score": min(100, 35 + (25 if strength.get("strongScore") is not None else 0) + (15 if strength.get("statusDetail") else 0)),
            "evidenceFields": ["dayMaster.strength", "wuxingScores.strongScore", "wuxingScores.statusDetail"],
            "source": strategy_names.get("扶抑", {}).get("source", ""),
        },
        {
            "strategy": "通关",
            "score": min(100, 25 + relation_count * 8),
            "evidenceFields": ["ganzhiRelations", "branchRelations", "baziBenchmark.ganzhiPriority"],
            "source": strategy_names.get("通关", {}).get("source", ""),
        },
        {
            "strategy": "病药",
            "score": min(100, 25 + spread * 3 + (15 if climate_band != "balanced_range" else 0)),
            "evidenceFields": ["wuxingScores.fiveElementScore", "climateScores", "geju"],
            "source": strategy_names.get("病药", {}).get("source", ""),
        },
    ]
    scored.sort(key=lambda item: item["score"], reverse=True)
    return {
        "schemaVersion": 1,
        "primaryStrategy": scored[0]["strategy"] if scored else "",
        "scoredStrategies": scored,
        "conflictPolicy": "调候、扶抑、通关、病药按证据完整度排序，但报告必须保留并列策略和风险边界。",
        "riskBoundary": "用神评分只用于解释优先级，不承诺现实事件结果。",
    }


def _build_topic_profiles(raw: dict[str, Any], ten_god_counts: dict[str, int], fortune_triggers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    families = _ten_god_families(ten_god_counts)
    relation_count = sum(item.get("count", 0) for item in _relation_order(raw) if isinstance(item.get("count"), int))
    spread = _five_element_spread(raw)
    topic_specs = [
        ("事业", ["格局", "官杀", "印星", "大运流年"], 35 + families.get("官杀", 0) * 8 + families.get("印", 0) * 5),
        ("财运", ["财星", "食伤", "用神", "岁运触发"], 35 + families.get("财", 0) * 10 + families.get("食伤", 0) * 5),
        ("婚姻", ["夫妻宫", "财官星", "合冲刑害", "岁运触发"], 30 + families.get("财", 0) * 5 + families.get("官杀", 0) * 5 + relation_count * 3),
        ("健康", ["五行偏枯", "寒暖燥湿"], 25 + spread * 3),
        ("学业", ["印星", "食伤", "文昌", "大运流年"], 35 + families.get("印", 0) * 8 + families.get("食伤", 0) * 4),
        ("迁移", ["驿马", "冲合", "岁运触发"], 30 + relation_count * 4 + len(fortune_triggers) * 3),
    ]
    profiles = []
    for topic, basis, score in topic_specs:
        profiles.append(
            {
                "topic": topic,
                "basis": basis,
                "score": max(0, min(100, int(score))),
                "status": "evidence_seed",
                "evidenceFields": ["tenGods", "geju", "yongShen", "baziBenchmark.fortuneTriggers"],
                "riskBoundary": "专题 profile 只作结构化解释入口，需独立 capability 或专门 golden 后才能输出专题断语。",
            }
        )
    return profiles


def _build_bazi_benchmark(raw: dict[str, Any]) -> dict[str, Any]:
    ten_gods = _ten_god_values(raw.get("tenGods", {}))
    ten_god_counts = {name: ten_gods.count(name) for name in sorted(set(ten_gods)) if name}
    geju = raw.get("geju", {}) if isinstance(raw.get("geju"), dict) else {}
    relation_order = _relation_order(raw)
    fortune_triggers = _fortune_triggers(raw)
    yongshen_strategies = _build_yongshen_strategies(raw)
    combine_matrix = _build_combine_transform_matrix(raw)
    special_candidates = _build_special_pattern_candidates(raw, combine_matrix)
    return {
        "schemaVersion": 1,
        "boundary": "标杆加固结构层；默认 Markdown 可选择摘要展示，核心事实仍以原始字段为准。",
        "timeBoundaryGolden": {
            "trueSolarTime": raw.get("trueSolarTime"),
            "ziTimeAnalysis": raw.get("ziTimeAnalysis", {}),
            "solarTermBoundary": raw.get("accuracyGuards", {}).get("solarTermBoundary", {})
            if isinstance(raw.get("accuracyGuards"), dict)
            else {},
            "ruleIds": ["bazi.true_solar_time_pipeline", "bazi.zi_time_boundary", "bazi.solar_term_month_boundary"],
        },
        "renYuanSiling": {
            "siling": raw.get("siling", {}),
            "monthCommand": raw.get("accuracyGuards", {}).get("solarTermBoundary", {}).get("monthCommand")
            if isinstance(raw.get("accuracyGuards"), dict)
            else "",
            "wuxingState": raw.get("wuxingState", {}),
            "monthHiddenStems": raw.get("hiddenStems", {}).get("month", {})
            if isinstance(raw.get("hiddenStems"), dict)
            else {},
            "ruleIds": ["bazi.month_command_priority", "bazi.renyuan_siling_weight"],
        },
        "strengthScore": {
            "label": raw.get("dayMaster", {}).get("strength", {}) if isinstance(raw.get("dayMaster"), dict) else "",
            "weak": raw.get("wuxingScores", {}).get("weak") if isinstance(raw.get("wuxingScores"), dict) else None,
            "strongScore": raw.get("wuxingScores", {}).get("strongScore")
            if isinstance(raw.get("wuxingScores"), dict)
            else None,
            "statusDetail": raw.get("wuxingScores", {}).get("statusDetail", [])
            if isinstance(raw.get("wuxingScores"), dict)
            else [],
            "fiveElementScore": raw.get("wuxingScores", {}).get("fiveElementScore", {})
            if isinstance(raw.get("wuxingScores"), dict)
            else {},
            "ruleIds": ["bazi.day_master_strength", "bazi.strength_score_golden"],
        },
        "ganzhiPriority": relation_order,
        "combineTransformMatrix": combine_matrix,
        "fortuneTriggers": fortune_triggers,
        "patternRegistry": {
            "main": geju.get("main", ""),
            "patterns": geju.get("patterns", []),
            "status": "seed",
            "specialPatternCandidates": special_candidates,
            "boundary": "格局事实、特殊候选和成败条件分层呈现；从格、化气等高级格局必须逐条补 golden。",
            "ruleIds": ["bazi.pattern_by_month_command", "bazi.pattern_root_transparency"],
        },
        "yongShenStrategies": yongshen_strategies,
        "yongShenDecision": _build_yongshen_decision(raw, yongshen_strategies),
        "tenGodStructure": {
            "counts": ten_god_counts,
            "basis": "从 tenGods 字段递归统计，仅作结构摘要。",
            "ruleIds": ["bazi.ten_god_structure"],
        },
        "topicProfiles": _build_topic_profiles(raw, ten_god_counts, fortune_triggers),
    }


def _append_bazi_benchmark_evidence(raw: dict[str, Any]) -> None:
    evidence = raw.get("analysisEvidence")
    benchmark = raw.get("baziBenchmark")
    if not isinstance(evidence, dict) or not isinstance(benchmark, dict):
        return
    items = evidence.setdefault("items", {})
    if not isinstance(items, dict):
        return
    items["baziBenchmark"] = _evidence_item(
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


def _rule_map(system: str) -> dict[str, dict[str, Any]]:
    return {str(rule.get("id", "")): rule for rule in rules_for_system(system)}


def _build_bazi_rule_depth(raw: dict[str, Any]) -> dict[str, Any]:
    """装配八字规则深度层：规则来自 registry，证据来自现有生产字段。"""
    rules = _rule_map("bazi")
    benchmark = raw.get("baziBenchmark", {}) if isinstance(raw.get("baziBenchmark"), dict) else {}
    strength = benchmark.get("strengthScore", {}) if isinstance(benchmark.get("strengthScore"), dict) else {}
    renyuan = benchmark.get("renYuanSiling", {}) if isinstance(benchmark.get("renYuanSiling"), dict) else {}
    pattern = benchmark.get("patternRegistry", {}) if isinstance(benchmark.get("patternRegistry"), dict) else {}
    yongshen = benchmark.get("yongShenStrategies", [])
    yongshen_decision = benchmark.get("yongShenDecision", {}) if isinstance(benchmark.get("yongShenDecision"), dict) else {}
    ten_god = benchmark.get("tenGodStructure", {}) if isinstance(benchmark.get("tenGodStructure"), dict) else {}
    relation = benchmark.get("ganzhiPriority", [])
    combine_matrix = benchmark.get("combineTransformMatrix", {}) if isinstance(benchmark.get("combineTransformMatrix"), dict) else {}
    special_candidates = (
        pattern.get("specialPatternCandidates", {}) if isinstance(pattern.get("specialPatternCandidates"), dict) else {}
    )
    fortune = benchmark.get("fortuneTriggers", [])
    monthly = raw.get("monthlyFortune", [])
    spirits = raw.get("spiritsFull", {})
    bone = raw.get("boneWeight", {})

    applied = [
        build_rule_application(
            rules["bazi.depth.strength.month_root_transparency"],
            status="applied" if strength and renyuan else "partial",
            confidence=0.9 if strength and renyuan else 0.55,
            evidence={
                "strengthLabel": strength.get("label"),
                "strongScore": strength.get("strongScore"),
                "monthCommand": renyuan.get("monthCommand"),
                "currentSiling": renyuan.get("siling", {}).get("current")
                if isinstance(renyuan.get("siling"), dict)
                else "",
                "monthHiddenStems": renyuan.get("monthHiddenStems"),
            },
            notes=["强弱仍保留灰度标签，避免单一分数硬断。"],
        ),
        build_rule_application(
            rules["bazi.depth.pattern.establishment"],
            status="applied" if pattern.get("main") or pattern.get("patterns") else "partial",
            confidence=0.82 if pattern.get("main") or pattern.get("patterns") else 0.5,
            evidence={
                "mainPattern": pattern.get("main"),
                "patterns": pattern.get("patterns", []),
                "relationPriorityKeys": [item.get("key") for item in relation if isinstance(item, dict)],
            },
            notes=["候选格局必须结合成败条件继续审查。"],
        ),
        build_rule_application(
            rules["bazi.depth.pattern.regular_vs_special"],
            status="applied" if pattern.get("main") else "partial",
            confidence=0.8 if pattern.get("main") else 0.48,
            evidence={
                "mainPattern": pattern.get("main"),
                "patternStatus": pattern.get("status"),
                "advancedPatternBoundary": pattern.get("boundary"),
            },
            notes=["正格、变格、从格、化气先走候选和边界登记。"],
        ),
        build_rule_application(
            rules["bazi.depth.pattern.follow_transform_guard"],
            status="applied" if special_candidates or combine_matrix else "guarded",
            confidence=0.76 if special_candidates or combine_matrix else 0.7,
            evidence={
                "mainPattern": pattern.get("main"),
                "specialPatternCandidates": special_candidates,
                "combineTransformMatrix": combine_matrix,
                "guard": "从格、化气、专旺具备条件矩阵后仍需 golden case，未达完整条件时不得强断。",
            },
            notes=["高级格局已有条件链字段；定格仍必须等待专门 golden 扩充后提升置信度。"],
        ),
        build_rule_application(
            rules["bazi.depth.pattern.special_pattern_checklist"],
            status="applied" if special_candidates.get("candidates") else "guarded",
            confidence=0.72 if special_candidates.get("candidates") else 0.66,
            evidence={
                "mainPattern": pattern.get("main"),
                "candidates": special_candidates.get("candidates", []),
                "dominantFamily": special_candidates.get("dominantFamily", {}),
                "guard": "特殊格局开放候选成熟度和条件链，不在缺少完整证据时定格。",
            },
            notes=["特殊格局以候选矩阵输出，不输出市场化强断。"],
        ),
        build_rule_application(
            rules["bazi.depth.pattern.finance_official_seal_food_matrix"],
            status="applied" if ten_god.get("counts") and pattern.get("main") else "partial",
            confidence=0.71 if ten_god.get("counts") and pattern.get("main") else 0.45,
            evidence={
                "mainPattern": pattern.get("main"),
                "roleFamilies": _ten_god_families(ten_god.get("counts", {})),
            },
            notes=["财官印食作为组合矩阵，不替代月令定格和成败条件。"],
        ),
        build_rule_application(
            rules["bazi.depth.yongshen.strategy_matrix"],
            status="applied" if isinstance(yongshen, list) and yongshen else "partial",
            confidence=0.84 if isinstance(yongshen, list) and len(yongshen) >= 4 else 0.6,
            evidence={
                "strategyCount": len(yongshen) if isinstance(yongshen, list) else 0,
                "strategies": [item.get("strategy") for item in yongshen if isinstance(item, dict)],
                "decision": yongshen_decision,
                "climateScores": raw.get("climateScores", {}),
                "fiveElementScore": strength.get("fiveElementScore", {}),
            },
            notes=["调候、扶抑、通关、病药按证据评分排序，但并列保留，不互相覆盖。"],
        ),
        build_rule_application(
            rules["bazi.depth.yongshen.tiaohou_priority"],
            status="applied" if raw.get("climateScores") else "partial",
            confidence=0.79 if raw.get("climateScores") else 0.52,
            evidence={
                "climateScores": raw.get("climateScores", {}),
                "tiaohouRaw": raw.get("yongShen", {}).get("tiaohouRaw")
                if isinstance(raw.get("yongShen"), dict)
                else "",
                "strategyNames": [item.get("strategy") for item in yongshen if isinstance(item, dict)]
                if isinstance(yongshen, list)
                else [],
            },
            notes=["寒暖燥湿优先作为调候证据，不直接覆盖扶抑策略。"],
        ),
        build_rule_application(
            rules["bazi.depth.yongshen.climate_detail_matrix"],
            status="applied" if raw.get("climateScores") else "partial",
            confidence=0.74 if raw.get("climateScores") else 0.46,
            evidence={
                "temperatureBand": _temperature_band(raw.get("climateScores", {})),
                "climateScores": raw.get("climateScores", {}),
                "strategyNames": [item.get("strategy") for item in yongshen if isinstance(item, dict)]
                if isinstance(yongshen, list)
                else [],
            },
            notes=["调候细分只影响解释权重，不直接输出生活处方。"],
        ),
        build_rule_application(
            rules["bazi.depth.tengod.structure_profile"],
            status="applied" if ten_god.get("counts") else "partial",
            confidence=0.76 if ten_god.get("counts") else 0.5,
            evidence={
                "counts": ten_god.get("counts", {}),
                "basis": ten_god.get("basis", ""),
            },
            notes=["十神组合以透干、藏干和位置为后续深化方向。"],
        ),
        build_rule_application(
            rules["bazi.depth.tengod.overlap_profile"],
            status="applied" if ten_god.get("counts") else "partial",
            confidence=0.72 if ten_god.get("counts") else 0.48,
            evidence={
                "counts": ten_god.get("counts", {}),
                "dominantTenGods": _dominant_counts(ten_god.get("counts", {}), limit=3),
                "basis": ten_god.get("basis", ""),
            },
            notes=["十神重叠只给组合倾向，不把单项十神写成人生定论。"],
        ),
        build_rule_application(
            rules["bazi.depth.tengod.role_family_matrix"],
            status="applied" if ten_god.get("counts") else "partial",
            confidence=0.7 if ten_god.get("counts") else 0.45,
            evidence={
                "roleFamilies": _ten_god_families(ten_god.get("counts", {})),
                "dominantTenGods": _dominant_counts(ten_god.get("counts", {}), limit=5),
            },
            notes=["财官印食、比劫、食伤、官杀等族群只作结构摘要。"],
        ),
        build_rule_application(
            rules["bazi.depth.climate.seasonal_adjustment"],
            status="applied" if raw.get("climateScores") and renyuan else "partial",
            confidence=0.73 if raw.get("climateScores") and renyuan else 0.5,
            evidence={
                "monthCommand": renyuan.get("monthCommand"),
                "climateScores": raw.get("climateScores", {}),
                "currentSiling": renyuan.get("siling", {}).get("current")
                if isinstance(renyuan.get("siling"), dict)
                else "",
            },
            notes=["季节寒暖燥湿只作为调候依据，不替代格局判定。"],
        ),
        build_rule_application(
            rules["bazi.depth.relation.collision_priority"],
            status="applied" if isinstance(relation, list) and relation else "partial",
            confidence=0.78 if isinstance(relation, list) and relation else 0.45,
            evidence={
                "priority": [
                    {
                        "key": item.get("key"),
                        "label": item.get("label"),
                        "count": item.get("count"),
                        "boundary": item.get("boundary"),
                    }
                    for item in relation
                    if isinstance(item, dict)
                ]
            },
            notes=["合化是否成化继续要求依据字段，当前不作强断。"],
        ),
        build_rule_application(
            rules["bazi.depth.relation.combine_transform_guard"],
            status="applied" if isinstance(relation, list) and relation else "partial",
            confidence=0.7 if isinstance(relation, list) and relation else 0.46,
            evidence={
                "priorityKeys": [item.get("key") for item in relation if isinstance(item, dict)],
                "combineTransformMatrix": combine_matrix,
                "guard": "合、冲、刑、害、破先登记结构触发；合化成败另需月令、透干、通根和阻隔证据。",
            },
            notes=["合化判断有条件矩阵，不从关系名称直接跳到成化结论。"],
        ),
        build_rule_application(
            rules["bazi.depth.relation.punishment_harm_break_matrix"],
            status="applied" if isinstance(relation, list) and relation else "partial",
            confidence=0.67 if isinstance(relation, list) and relation else 0.43,
            evidence={
                "relationFamilies": _relation_families(relation),
                "priorityKeys": [item.get("key") for item in relation if isinstance(item, dict)],
            },
            notes=["刑冲害破只说明结构摩擦，不输出恐吓式事件。"],
        ),
        build_rule_application(
            rules["bazi.depth.fortune.trigger_chain"],
            status="applied" if isinstance(fortune, list) else "partial",
            confidence=0.72 if isinstance(fortune, list) else 0.4,
            evidence={
                "triggerCount": len(fortune) if isinstance(fortune, list) else 0,
                "sampleTriggers": fortune[:5] if isinstance(fortune, list) else [],
                "majorFortuneAvailable": bool(raw.get("majorFortune")),
                "annualFortuneCount": len(raw.get("annualFortune", []))
                if isinstance(raw.get("annualFortune"), list)
                else 0,
            },
            notes=["动态层只说明触发链，不覆盖原局结构。"],
        ),
        build_rule_application(
            rules["bazi.depth.fortune.decade_year_month_order"],
            status="applied" if raw.get("majorFortune") and raw.get("annualFortune") else "partial",
            confidence=0.69 if raw.get("majorFortune") and raw.get("annualFortune") else 0.44,
            evidence={
                "majorFortuneAvailable": bool(raw.get("majorFortune")),
                "annualFortuneCount": len(raw.get("annualFortune", []))
                if isinstance(raw.get("annualFortune"), list)
                else 0,
                "monthlyFortuneCount": len(monthly) if isinstance(monthly, list) else 0,
            },
            notes=["大运定阶段，流年定触发，流月只细化窗口。"],
        ),
        build_rule_application(
            rules["bazi.depth.fortune.month_trigger"],
            status="applied" if isinstance(monthly, list) and monthly else "partial",
            confidence=0.68 if isinstance(monthly, list) and monthly else 0.42,
            evidence={
                "monthlyFortuneCount": len(monthly) if isinstance(monthly, list) else 0,
                "sampleMonths": monthly[:3] if isinstance(monthly, list) else [],
            },
            notes=["流月只作短周期触发证据，必须受原局和大运流年约束。"],
        ),
        build_rule_application(
            rules["bazi.depth.auxiliary.boundary_guard"],
            status="applied" if spirits or bone else "partial",
            confidence=0.8 if spirits or bone else 0.5,
            evidence={
                "hasSpirits": bool(spirits),
                "hasBoneWeight": bool(bone),
                "weightBoundary": "神煞/称骨不参与核心强弱、喜忌和格局定性。",
            },
            notes=["辅助体系保留展示边界，防止污染综合八字核心判断。"],
        ),
        build_rule_application(
            rules["bazi.depth.statement.combination_boundary"],
            status="applied",
            confidence=0.74,
            evidence={
                "statementInputs": ["日主强弱", "格局", "用神策略", "十神组合", "岁运触发"],
                "guard": "组合断语必须同时给出规则 ID、证据字段和风险边界。",
            },
            notes=["组合断语输出为审计摘要，不新增不可追溯结论。"],
        ),
        build_rule_application(
            rules["bazi.depth.statement.narrative_markdown"],
            status="applied",
            confidence=0.72,
            evidence={
                "target": "baziRuleDepth.narrativeSummary",
                "format": "markdown",
            },
            notes=["自然语言报告只从组合断语生成，保留规则 ID。"],
        ),
    ]
    conflict_matrix = [
        {
            "type": "strategy_priority",
            "topic": "用神策略冲突",
            "rules": ["bazi.depth.yongshen.strategy_matrix", "bazi.depth.yongshen.tiaohou_priority"],
            "policy": "调候、扶抑、通关、病药并列，按证据完整度和风险边界解释。",
        },
        {
            "type": "pattern_candidate",
            "topic": "格局候选冲突",
            "rules": [
                "bazi.depth.pattern.establishment",
                "bazi.depth.pattern.regular_vs_special",
                "bazi.depth.pattern.follow_transform_guard",
                "bazi.depth.pattern.special_pattern_checklist",
                "bazi.depth.pattern.finance_official_seal_food_matrix",
            ],
            "policy": "普通格局、正格、特殊格局按成败条件分层，不把候选写成定格。",
        },
        {
            "type": "relation_boundary",
            "topic": "干支合化边界",
            "rules": [
                "bazi.depth.relation.collision_priority",
                "bazi.depth.relation.combine_transform_guard",
                "bazi.depth.relation.punishment_harm_break_matrix",
            ],
            "policy": "先登记合冲刑害破，再按月令、透干、通根和阻隔证据判断是否成化；缺证据时只保留合象。",
        },
        {
            "type": "time_hierarchy",
            "topic": "动态层级顺序",
            "rules": [
                "bazi.depth.fortune.trigger_chain",
                "bazi.depth.fortune.decade_year_month_order",
                "bazi.depth.fortune.month_trigger",
            ],
            "policy": "原局优先，大运定阶段，流年定触发，流月只细化窗口。",
        },
        {
            "type": "auxiliary_boundary",
            "topic": "辅助体系边界",
            "rules": ["bazi.depth.auxiliary.boundary_guard"],
            "policy": "神煞和称骨只可辅助，不参与核心喜忌和格局裁决。",
        },
    ]
    conflict_resolution = build_conflict_resolution(applied, conflict_matrix)
    combination_statements = _build_bazi_combination_statements(raw, applied)
    return {
        "schemaVersion": 1,
        "registryVersion": registry_version(),
        "system": "bazi",
        "boundary": "规则深度层只组织可追溯证据和冲突策略；默认报告仍保持综合八字结构边界。",
        "appliedRules": applied,
        "conflictMatrix": conflict_matrix,
        "conflictResolution": conflict_resolution,
        "weightProfile": build_weight_profile(applied),
        "combinationStatements": combination_statements,
        "narrativeSummary": build_narrative_summary(
            title="综合八字规则摘要",
            combination_statements=combination_statements,
            conflict_resolution=conflict_resolution,
        ),
        "sourceRuleIds": collect_source_rule_ids(applied),
    }


def _dominant_counts(counts: Any, *, limit: int) -> list[dict[str, Any]]:
    if not isinstance(counts, dict):
        return []
    items = sorted(
        ((str(name), int(value)) for name, value in counts.items() if isinstance(value, int | float)),
        key=lambda item: item[1],
        reverse=True,
    )
    return [{"name": name, "count": count} for name, count in items[:limit]]


def _ten_god_families(counts: Any) -> dict[str, int]:
    if not isinstance(counts, dict):
        return {}
    families = {
        "财": ["正财", "偏财"],
        "官杀": ["正官", "七杀"],
        "印": ["正印", "偏印"],
        "食伤": ["食神", "伤官"],
        "比劫": ["比肩", "劫财"],
    }
    return {
        family: sum(int(counts.get(name, 0)) for name in names if isinstance(counts.get(name, 0), int | float))
        for family, names in families.items()
    }


def _temperature_band(climate_scores: Any) -> str:
    if not isinstance(climate_scores, dict):
        return "unknown"
    score = climate_scores.get("temperatureScore")
    if not isinstance(score, int | float):
        return "unknown"
    if score <= -7:
        return "cold_wet_bias"
    if score >= 7:
        return "hot_dry_bias"
    return "balanced_range"


def _relation_families(relation: Any) -> dict[str, int]:
    if not isinstance(relation, list):
        return {}
    families = {"combine": 0, "clash": 0, "punishment_harm_break": 0, "storage": 0, "other": 0}
    for item in relation:
        if not isinstance(item, dict):
            continue
        text = f"{item.get('key', '')}{item.get('label', '')}"
        count = int(item.get("count", 1)) if isinstance(item.get("count", 1), int | float) else 1
        if "合" in text:
            families["combine"] += count
        elif "冲" in text:
            families["clash"] += count
        elif any(marker in text for marker in ["刑", "害", "破"]):
            families["punishment_harm_break"] += count
        elif "库" in text or "墓" in text:
            families["storage"] += count
        else:
            families["other"] += count
    return families


def _build_bazi_combination_statements(raw: dict[str, Any], applied: list[dict[str, Any]]) -> list[dict[str, Any]]:
    benchmark = raw.get("baziBenchmark", {}) if isinstance(raw.get("baziBenchmark"), dict) else {}
    strength = benchmark.get("strengthScore", {}) if isinstance(benchmark.get("strengthScore"), dict) else {}
    pattern = benchmark.get("patternRegistry", {}) if isinstance(benchmark.get("patternRegistry"), dict) else {}
    ten_god = benchmark.get("tenGodStructure", {}) if isinstance(benchmark.get("tenGodStructure"), dict) else {}
    yongshen = benchmark.get("yongShenStrategies", [])
    yongshen_decision = benchmark.get("yongShenDecision", {}) if isinstance(benchmark.get("yongShenDecision"), dict) else {}
    relation = benchmark.get("ganzhiPriority", [])
    combine_matrix = benchmark.get("combineTransformMatrix", {}) if isinstance(benchmark.get("combineTransformMatrix"), dict) else {}
    special_candidates = (
        pattern.get("specialPatternCandidates", {}) if isinstance(pattern.get("specialPatternCandidates"), dict) else {}
    )
    applied_ids = {str(item.get("ruleId", "")) for item in applied}

    statements = [
        build_combination_statement(
            topic="强弱-格局-用神",
            statement="先以月令和日主强弱定结构背景，再用格局与用神策略解释取舍；不同策略并列保留，不压成单一喜忌。",
            rule_ids=[
                "bazi.depth.strength.month_root_transparency",
                "bazi.depth.pattern.establishment",
                "bazi.depth.yongshen.strategy_matrix",
            ],
            evidence={
                "strengthLabel": strength.get("label"),
                "mainPattern": pattern.get("main"),
                "strategyCount": len(yongshen) if isinstance(yongshen, list) else 0,
                "primaryYongShenStrategy": yongshen_decision.get("primaryStrategy"),
            },
            confidence=0.82,
            risk_boundary="该断语只说明解释顺序，不输出确定事件。",
        ),
        build_combination_statement(
            topic="十神组合",
            statement="十神数量和族群用于提示结构重心，必须回到透干、藏干和柱位；财官印食等族群只作观察入口。",
            rule_ids=[
                "bazi.depth.tengod.structure_profile",
                "bazi.depth.tengod.overlap_profile",
                "bazi.depth.tengod.role_family_matrix",
            ],
            evidence={
                "dominantTenGods": _dominant_counts(ten_god.get("counts", {}), limit=3),
                "roleFamilies": _ten_god_families(ten_god.get("counts", {})),
            },
            confidence=0.72,
            risk_boundary="不得用单一十神标签替代完整八字判断。",
        ),
        build_combination_statement(
            topic="特殊格局边界",
            statement="从格、化气、专旺等特殊格局只开放检查清单；缺少完整成败条件时，仍以普通格局和候选缺口呈现。",
            rule_ids=[
                "bazi.depth.pattern.regular_vs_special",
                "bazi.depth.pattern.special_pattern_checklist",
                "bazi.depth.pattern.follow_transform_guard",
            ],
            evidence={
                "mainPattern": pattern.get("main"),
                "advancedPatternBoundary": pattern.get("boundary"),
                "candidates": special_candidates.get("candidates", []),
            },
            confidence=0.66,
            risk_boundary="特殊格局不得在证据不足时强行定格。",
        ),
        build_combination_statement(
            topic="调候细分",
            statement="寒暖燥湿先决定调候解释权重，再和扶抑、通关、病药并列；调候细分不替代完整用神判断。",
            rule_ids=[
                "bazi.depth.yongshen.tiaohou_priority",
                "bazi.depth.yongshen.climate_detail_matrix",
                "bazi.depth.climate.seasonal_adjustment",
            ],
            evidence={
                "temperatureBand": _temperature_band(raw.get("climateScores", {})),
                "climateScores": raw.get("climateScores", {}),
            },
            confidence=0.74,
            risk_boundary="调候解释不等于医疗、养生或现实处方。",
        ),
        build_combination_statement(
            topic="干支关系",
            statement="合冲刑害破先作为结构触发排序，合化成败另看月令、透干、通根与阻隔证据；刑害破只作结构摩擦提示。",
            rule_ids=[
                "bazi.depth.relation.collision_priority",
                "bazi.depth.relation.combine_transform_guard",
                "bazi.depth.relation.punishment_harm_break_matrix",
            ],
            evidence={
                "relationKeys": [item.get("key") for item in relation if isinstance(item, dict)],
                "relationFamilies": _relation_families(relation),
                "combineTransformStatus": combine_matrix.get("status"),
                "combineTransformCandidates": combine_matrix.get("candidates", []),
            },
            confidence=0.7,
            risk_boundary="缺少成化证据时只登记合象，不写成已成化。",
        ),
        build_combination_statement(
            topic="岁运层级",
            statement="原局是底盘，大运给阶段，流年给触发，流月只细化时间窗口；动态层不得覆盖原局结构。",
            rule_ids=[
                "bazi.depth.fortune.trigger_chain",
                "bazi.depth.fortune.decade_year_month_order",
                "bazi.depth.fortune.month_trigger",
            ],
            evidence={
                "majorFortuneAvailable": bool(raw.get("majorFortune")),
                "annualFortuneCount": len(raw.get("annualFortune", []))
                if isinstance(raw.get("annualFortune"), list)
                else 0,
                "monthlyFortuneCount": len(raw.get("monthlyFortune", []))
                if isinstance(raw.get("monthlyFortune"), list)
                else 0,
            },
            confidence=0.69,
            risk_boundary="岁运只作趋势触发说明，不保证事件结果。",
        ),
    ]
    return [item for item in statements if set(item["ruleIds"]) <= applied_ids]


def _append_bazi_rule_depth_evidence(raw: dict[str, Any]) -> None:
    evidence = raw.get("analysisEvidence")
    rule_depth = raw.get("baziRuleDepth")
    if not isinstance(evidence, dict) or not isinstance(rule_depth, dict):
        return
    items = evidence.setdefault("items", {})
    if not isinstance(items, dict):
        return
    applied = rule_depth.get("appliedRules", [])
    items["baziRuleDepth"] = _evidence_item(
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


def calculate_pure_analysis(payload: PureAnalysisInput) -> dict[str, Any]:
    """计算纯命理分析字段集合。"""
    runtime = build_pure_analysis_runtime(
        LegacyBaziInput(
            birth_dt=payload.birth_dt,
            gender=normalize_gender(payload.gender),
            longitude=payload.longitude,
            latitude=payload.latitude,
            name=payload.name,
            birth_place=payload.birth_place,
            use_true_solar_time=payload.use_true_solar_time,
        )
    )
    raw = {}
    raw.update(build_base_chart_section(runtime))
    raw.update(build_fortune_section(runtime))
    raw.update(build_classical_section(runtime))
    raw["analysisEvidence"] = runtime.calculator._calc_analysis_evidence(
        four_pillars=runtime.four_pillars,
        hidden_stems=runtime.hidden_stems,
        day_master=raw.get("dayMaster", {}),
        wuxing_scores=raw.get("wuxingScores", {}),
        geju=raw.get("geju", {}),
        yongshen=raw.get("yongShen", {}),
        ganzhi_relations=raw.get("ganzhiRelations", {}),
        branch_relations=raw.get("branchRelations", {}),
        spirits=raw.get("spiritsFull", {}),
        bone_weight=raw.get("boneWeight", {}),
    )
    raw["accuracyGuards"] = _build_accuracy_guards(runtime, raw)
    _append_accuracy_evidence(runtime, raw)
    raw["baziBenchmark"] = _build_bazi_benchmark(raw)
    _append_bazi_benchmark_evidence(raw)
    raw["baziRuleDepth"] = _build_bazi_rule_depth(raw)
    _append_bazi_rule_depth_evidence(raw)
    projected = project_by_profile(raw, "pure_analysis")
    translated = runtime.calculator._translate_to_chinese(projected)
    safe_result = runtime.calculator._json_safe(translated)
    if not isinstance(safe_result, dict):
        raise RuntimeError("纯分析结果必须是 JSON 对象")
    return dict(safe_result)
