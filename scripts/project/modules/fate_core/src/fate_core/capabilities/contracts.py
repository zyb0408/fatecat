from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

CapabilityStatus = Literal["planned", "experimental", "production"]
Visibility = Literal["default", "optional", "standalone", "hidden"]
RiskLevel = Literal["folk_reference", "entertainment", "requires_disclaimer"]


@dataclass(frozen=True)
class Capability:
    """预测能力注册项。"""

    capability_id: str
    name: str
    tradition: str
    status: CapabilityStatus
    default_visibility: Visibility
    input_required: tuple[str, ...]
    input_optional: tuple[str, ...]
    provider: str
    report_profile: str
    evidence_required: bool
    risk_level: RiskLevel
    disclaimer_required: bool
    forbidden_claims: tuple[str, ...]
    description: str = ""


@dataclass(frozen=True)
class CapabilityInput:
    """统一能力执行输入。"""

    capability_id: str
    payload: dict[str, Any]


@dataclass(frozen=True)
class CapabilityResult:
    """统一能力执行输出。"""

    capability_id: str
    status: CapabilityStatus
    report_profile: str
    data: dict[str, Any]
    evidence: dict[str, Any]
    risk: dict[str, Any]
