from typing import Dict
from pydantic import BaseModel, field_validator


ALLOWED_ENVIRONMENTS = {"Cloud", "SaaS", "On-Prem", "Hybrid"}
ALLOWED_STATUSES = {"COMPLIANT", "NON_COMPLIANT", "PARTIAL", "NOT_TESTED"}


# ── Request schemas ────────────────────────────────────────────────────────────

class OrgProfileRequest(BaseModel):
    environment: str
    ai_usage: bool
    apis_exposed: bool

    @field_validator("environment")
    @classmethod
    def environment_must_be_allowed(cls, v: str) -> str:
        if v not in ALLOWED_ENVIRONMENTS:
            raise ValueError(
                f"Invalid environment: {v!r}. Allowed: {sorted(ALLOWED_ENVIRONMENTS)}"
            )
        return v


class EvidenceEntryRequest(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def status_must_be_allowed(cls, v: str) -> str:
        if v not in ALLOWED_STATUSES:
            raise ValueError(
                f"Invalid status: {v!r}. Allowed: {sorted(ALLOWED_STATUSES)}"
            )
        return v


class EvaluateRequest(BaseModel):
    org_profile: OrgProfileRequest
    evidence: Dict[str, EvidenceEntryRequest]


# ── Response schemas ───────────────────────────────────────────────────────────

class SummaryResponse(BaseModel):
    applicable_controls: int
    compliant: int
    non_compliant: int
    partial: int
    not_tested: int
    compliance_score_percent: float


class DomainSummaryResponse(BaseModel):
    applicable: int
    score_percent: float


class ControlResultResponse(BaseModel):
    control_id: str
    domain: str
    status: str  # COMPLIANT | NON_COMPLIANT | PARTIAL | NOT_TESTED | NOT_APPLICABLE
    applicable: bool


class ControlApplicabilityResponse(BaseModel):
    environments: list[str]
    ai_usage: str
    mandatory: bool


class ControlRegistryEntryResponse(BaseModel):
    control_id: str
    domain: str
    atomic_objective: str
    primary_authority: str
    authority_class: str
    applicability: ControlApplicabilityResponse


class EvaluateResponse(BaseModel):
    engine_version: str
    registry_version: str
    evaluation_timestamp: str
    summary: SummaryResponse
    domain_breakdown: Dict[str, DomainSummaryResponse]
    controls: list[ControlResultResponse]
    controls_registry: Dict[str, ControlRegistryEntryResponse]


# ── Error schema ───────────────────────────────────────────────────────────────

class ErrorDetail(BaseModel):
    error: str
    message: str
