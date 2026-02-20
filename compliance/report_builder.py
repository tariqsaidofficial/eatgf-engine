from datetime import datetime, timezone
from .report_models import Summary, DomainSummary, ControlResult, ComplianceReport

def build_report(registry_version: str, engine_version: str, evaluation_result) -> ComplianceReport:
    timestamp = datetime.now(timezone.utc).isoformat()
    summary = Summary(
        applicable_controls=evaluation_result['total_applicable'],
        compliant=evaluation_result['total_compliant'],
        non_compliant=evaluation_result['total_non_compliant'],
        partial=evaluation_result['total_partial'],
        not_tested=evaluation_result['total_not_tested'],
        compliance_score_percent=round(evaluation_result['compliance_percent'], 1),
    )
    domain_breakdown = {
        domain: DomainSummary(
            applicable=data['applicable'],
            score_percent=round(data['score_percent'], 1)
        )
        for domain, data in sorted(evaluation_result['domain_breakdown'].items())
    }
    controls = sorted(
        [
            ControlResult(
                control_id=cid,
                domain=ctrl['domain'],
                status=ctrl['status'],
                applicable=(ctrl['status'] != 'NOT_APPLICABLE')
            )
            for cid, ctrl in evaluation_result['results'].items()
        ],
        key=lambda x: x.control_id
    )
    return ComplianceReport(
        engine_version=engine_version,
        registry_version=registry_version,
        evaluation_timestamp=timestamp,
        summary=summary,
        domain_breakdown=domain_breakdown,
        controls=controls
    )
