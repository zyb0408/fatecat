"""命理应用用例入口。"""

from .calculate_almanac import AlmanacInput, build_almanac_input_from_payload, calculate_almanac, parse_date
from .calculate_pure_analysis import (
    PureAnalysisInput,
    build_pure_analysis_input_from_payload,
    calculate_pure_analysis,
    normalize_gender,
    normalize_pure_analysis_payload,
    parse_datetime,
)
from .calculate_ziwei import build_ziwei_input_from_payload, calculate_ziwei

__all__ = [
    "AlmanacInput",
    "PureAnalysisInput",
    "build_almanac_input_from_payload",
    "build_pure_analysis_input_from_payload",
    "calculate_almanac",
    "calculate_pure_analysis",
    "calculate_ziwei",
    "build_ziwei_input_from_payload",
    "normalize_gender",
    "normalize_pure_analysis_payload",
    "parse_date",
    "parse_datetime",
]
