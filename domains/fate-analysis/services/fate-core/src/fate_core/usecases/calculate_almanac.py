from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any

from fate_core.adapters import build_lunar_datetime, build_lunar_day

MAX_DATE_RANGE_DAYS = 366

TIME_SLOT_HOURS: tuple[tuple[int, str], ...] = (
    (23, "子"),
    (1, "丑"),
    (3, "寅"),
    (5, "卯"),
    (7, "辰"),
    (9, "巳"),
    (11, "午"),
    (13, "未"),
    (15, "申"),
    (17, "酉"),
    (19, "戌"),
    (21, "亥"),
)

EVENT_ALIASES: dict[str, tuple[str, ...]] = {
    "开业": ("开市", "交易", "立券"),
    "开市": ("开市", "交易", "立券"),
    "签约": ("订盟", "纳采", "交易", "立券"),
    "结婚": ("嫁娶",),
    "嫁娶": ("嫁娶",),
    "搬家": ("入宅", "移徙"),
    "入宅": ("入宅",),
    "出行": ("出行",),
    "动土": ("动土", "修造"),
    "装修": ("修造", "动土"),
    "安葬": ("安葬", "破土"),
    "祭祀": ("祭祀",),
    "祈福": ("祈福",),
}

ZHIXING_SCORE: dict[str, int] = {
    "建": 0,
    "除": 1,
    "满": 1,
    "平": 0,
    "定": 1,
    "执": 0,
    "破": -1,
    "危": -1,
    "成": 1,
    "收": 1,
    "开": 1,
    "闭": -1,
}


@dataclass(frozen=True)
class AlmanacInput:
    """黄历择日用例输入。"""

    start_date: date
    end_date: date
    event_type: str
    place: str


def _first_non_empty(*values: Any) -> Any:
    for value in values:
        if value not in (None, ""):
            return value
    return None


def parse_date(value: Any) -> date:
    """解析公历日期，支持 ISO 日期或日期时间字符串。"""
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    normalized = str(value).strip()
    if not normalized:
        raise ValueError("日期不能为空")
    if "T" in normalized:
        normalized = normalized.split("T", 1)[0]
    if " " in normalized:
        normalized = normalized.split(" ", 1)[0]
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(normalized, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"无法解析日期: {value}")


def _normalize_date_range(value: Any) -> tuple[date, date]:
    if isinstance(value, dict):
        start_raw = _first_non_empty(value.get("start"), value.get("from"), value.get("startDate"))
        end_raw = _first_non_empty(value.get("end"), value.get("to"), value.get("endDate"), start_raw)
    elif isinstance(value, (list, tuple)):
        if not value:
            raise ValueError("dateRange 不能为空")
        start_raw = value[0]
        end_raw = value[1] if len(value) > 1 else value[0]
    else:
        start_raw = value
        end_raw = value

    start_date = parse_date(start_raw)
    end_date = parse_date(end_raw)
    if end_date < start_date:
        raise ValueError("dateRange.end 不能早于 dateRange.start")
    if (end_date - start_date).days + 1 > MAX_DATE_RANGE_DAYS:
        raise ValueError(f"dateRange 最多支持 {MAX_DATE_RANGE_DAYS} 天")
    return start_date, end_date


def _normalize_place(value: Any) -> str:
    if isinstance(value, dict):
        value = _first_non_empty(value.get("name"), value.get("city"), value.get("label"))
    place = str(value or "").strip()
    if not place:
        raise ValueError("place 不能为空")
    return place


def _public_place(place: str) -> str:
    return place.strip()


def _event_terms(event_type: str) -> list[str]:
    normalized = event_type.strip()
    if not normalized:
        raise ValueError("eventType 不能为空")
    terms = EVENT_ALIASES.get(normalized, (normalized,))
    return list(dict.fromkeys(term for term in terms if term))


def build_almanac_input_from_payload(raw_payload: dict[str, Any]) -> AlmanacInput:
    """从统一 payload 构造黄历择日输入。"""
    date_range = _first_non_empty(
        raw_payload.get("dateRange"),
        {"start": raw_payload.get("startDate"), "end": raw_payload.get("endDate")}
        if raw_payload.get("startDate")
        else None,
        raw_payload.get("date"),
    )
    if date_range is None:
        raise ValueError("缺少必填字段: dateRange")
    event_type = str(_first_non_empty(raw_payload.get("eventType"), raw_payload.get("event"), "")).strip()
    if not event_type:
        raise ValueError("缺少必填字段: eventType")
    start_date, end_date = _normalize_date_range(date_range)
    return AlmanacInput(
        start_date=start_date,
        end_date=end_date,
        event_type=event_type,
        place=_normalize_place(raw_payload.get("place")),
    )


def _safe_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, tuple):
        return [str(item) for item in value]
    if value in (None, ""):
        return []
    return [str(value)]


def _lunar_label(lunar: Any) -> str:
    return f"{lunar.getYearInGanZhi()}年 {lunar.getMonthInGanZhi()}月 {lunar.getDayInGanZhi()}日"


def _time_slots(current: date, event_terms: list[str]) -> list[dict[str, Any]]:
    slots: list[dict[str, Any]] = []
    for hour, zhi in TIME_SLOT_HOURS:
        lunar = build_lunar_datetime(current.year, current.month, current.day, hour)
        yi = _safe_list(lunar.getTimeYi())
        ji = _safe_list(lunar.getTimeJi())
        matched_yi = [term for term in event_terms if term in yi]
        matched_ji = [term for term in event_terms if term in ji]
        if matched_ji:
            suitability = "avoid"
            score = -1
            reason = f"时辰命中忌项：{'、'.join(matched_ji)}"
        elif matched_yi:
            suitability = "recommended"
            score = 1
            reason = f"时辰命中宜项：{'、'.join(matched_yi)}"
        else:
            suitability = "neutral"
            score = 0
            reason = "时辰宜忌未直接命中事件关键词"
        slots.append(
            {
                "hour": hour,
                "zhi": zhi,
                "timeRange": "23:00-00:59" if hour == 23 else f"{hour:02d}:00-{(hour + 1):02d}:59",
                "yi": yi,
                "ji": ji,
                "suitability": suitability,
                "score": score,
                "reason": reason,
            }
        )
    return slots


def _score_breakdown(
    *,
    suitability: str,
    zhi_xing: str,
    matched_yi: list[str],
    matched_ji: list[str],
    slots: list[dict[str, Any]],
) -> dict[str, Any]:
    day_score = 2 if suitability == "recommended" else -2 if suitability == "avoid" else 0
    zhi_xing_score = ZHIXING_SCORE.get(zhi_xing, 0)
    recommended_slots = [item for item in slots if item["suitability"] == "recommended"]
    avoid_slots = [item for item in slots if item["suitability"] == "avoid"]
    time_score = min(2, len(recommended_slots)) - min(2, len(avoid_slots))
    total = day_score + zhi_xing_score + time_score
    return {
        "dayYiJi": day_score,
        "zhiXing": zhi_xing_score,
        "timeSlots": time_score,
        "total": total,
        "matchedYi": matched_yi,
        "matchedJi": matched_ji,
        "recommendedSlotCount": len(recommended_slots),
        "avoidSlotCount": len(avoid_slots),
    }


def _daily_almanac(current: date, event_terms: list[str]) -> tuple[dict[str, Any], dict[str, Any]]:
    lunar = build_lunar_day(current.year, current.month, current.day)
    yi = _safe_list(lunar.getDayYi())
    ji = _safe_list(lunar.getDayJi())
    matched_yi = [term for term in event_terms if term in yi]
    matched_ji = [term for term in event_terms if term in ji]

    if matched_ji:
        suitability = "avoid"
        score = -2
        reason = f"事件关键词命中忌项：{'、'.join(matched_ji)}"
    elif matched_yi:
        suitability = "recommended"
        score = 2
        reason = f"事件关键词命中宜项：{'、'.join(matched_yi)}"
    else:
        suitability = "neutral"
        score = 0
        reason = "黄历宜忌未直接命中该事件关键词"

    zhi_xing = lunar.getZhiXing()
    time_slots = _time_slots(current, event_terms)
    score_breakdown = _score_breakdown(
        suitability=suitability,
        zhi_xing=zhi_xing,
        matched_yi=matched_yi,
        matched_ji=matched_ji,
        slots=time_slots,
    )

    day = {
        "date": current.isoformat(),
        "lunarLabel": _lunar_label(lunar),
        "zhiXing": zhi_xing,
        "xiu": lunar.getXiu(),
        "xiuLuck": lunar.getXiuLuck(),
        "xiuSong": lunar.getXiuSong(),
        "yi": yi,
        "ji": ji,
        "suitability": suitability,
        "score": score + score_breakdown["zhiXing"] + score_breakdown["timeSlots"],
        "scoreBreakdown": score_breakdown,
        "reason": reason,
        "chong": lunar.getChongDesc(),
        "sha": lunar.getSha(),
        "dayChong": lunar.getDayChongDesc(),
        "daySha": lunar.getDaySha(),
        "pengZu": f"{lunar.getPengZuGan()} {lunar.getPengZuZhi()}",
        "jiShen": _safe_list(lunar.getDayJiShen()),
        "xiongSha": _safe_list(lunar.getDayXiongSha()),
        "timeSlots": time_slots,
        "positions": {
            "xi": lunar.getPositionXiDesc(),
            "yangGui": lunar.getPositionYangGuiDesc(),
            "yinGui": lunar.getPositionYinGuiDesc(),
            "fu": lunar.getPositionFuDesc(),
            "cai": lunar.getPositionCaiDesc(),
            "taiSui": lunar.getDayPositionTaiSuiDesc(),
        },
    }
    evidence = {
        "source": "lunar-python",
        "calendarDate": current.isoformat(),
        "ruleIds": [
            "almanac.day_yi_ji",
            "almanac.event_alias_mapping",
            "almanac.time_yi_ji",
            "almanac.zhi_xing_auxiliary",
            "almanac.xiu_auxiliary",
        ],
        "basis": {
            "yi": yi,
            "ji": ji,
            "matchedYi": matched_yi,
            "matchedJi": matched_ji,
            "zhiXing": day["zhiXing"],
            "xiu": day["xiu"],
            "xiuLuck": day["xiuLuck"],
            "chong": day["chong"],
            "sha": day["sha"],
            "scoreBreakdown": score_breakdown,
            "recommendedTimeSlots": [
                {"hour": item["hour"], "zhi": item["zhi"], "reason": item["reason"]}
                for item in day["timeSlots"]
                if item["suitability"] == "recommended"
            ],
            "avoidTimeSlots": [
                {"hour": item["hour"], "zhi": item["zhi"], "reason": item["reason"]}
                for item in day["timeSlots"]
                if item["suitability"] == "avoid"
            ],
        },
        "recommendReason": reason if suitability == "recommended" else "",
        "avoidReason": reason if suitability == "avoid" else "",
        "risk": "folk_reference",
    }
    return day, evidence


def calculate_almanac(payload: AlmanacInput) -> dict[str, Any]:
    """计算黄历择日独立 capability。"""
    event_terms = _event_terms(payload.event_type)
    days: list[dict[str, Any]] = []
    evidence_items: dict[str, dict[str, Any]] = {}

    current = payload.start_date
    while current <= payload.end_date:
        day, evidence = _daily_almanac(current, event_terms)
        days.append(day)
        evidence_items[current.isoformat()] = evidence
        current += timedelta(days=1)

    recommended = [day for day in days if day["suitability"] == "recommended"]
    avoid = [day for day in days if day["suitability"] == "avoid"]
    neutral = [day for day in days if day["suitability"] == "neutral"]
    recommendations = sorted(days, key=lambda item: (-int(item["score"]), str(item["date"])))[:10]
    evidence = {
        "schemaVersion": 1,
        "capabilityId": "almanac",
        "source": "lunar-python",
        "items": evidence_items,
    }
    return {
        "capabilityId": "almanac",
        "eventType": payload.event_type,
        "eventTerms": event_terms,
        "place": _public_place(payload.place),
        "dateRange": {
            "start": payload.start_date.isoformat(),
            "end": payload.end_date.isoformat(),
            "days": len(days),
        },
        "summary": {
            "recommendedCount": len(recommended),
            "avoidCount": len(avoid),
            "neutralCount": len(neutral),
        },
        "days": days,
        "recommendations": recommendations,
        "analysisEvidence": evidence,
    }
