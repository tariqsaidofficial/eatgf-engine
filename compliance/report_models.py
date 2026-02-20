from dataclasses import dataclass
from typing import Dict, List

@dataclass(frozen=True)
class Summary:
    applicable_controls: int
    compliant: int
    non_compliant: int
    partial: int
    not_tested: int
    compliance_score_percent: float

@dataclass(frozen=True)
class DomainSummary:
    applicable: int
    score_percent: float

@dataclass(frozen=True)
class ControlResult:
    control_id: str
    domain: str
    status: str
    applicable: bool

@dataclass(frozen=True)
class ComplianceReport:
    engine_version: str
    registry_version: str
    evaluation_timestamp: str
    summary: Summary
    domain_breakdown: Dict[str, DomainSummary]
    controls: List[ControlResult]
