from typing import Dict, Any

ALLOWED_STATUSES = {"COMPLIANT", "NON_COMPLIANT", "PARTIAL", "NOT_TESTED"}

class EvidenceValidationError(Exception):
    pass

def load_evidence(evidence_path: str, registry_controls: Dict[str, Any]) -> Dict[str, Any]:
    import json
    with open(evidence_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    seen = set()
    result = {}
    for control_id, record in raw.items():
        if control_id not in registry_controls:
            raise EvidenceValidationError(f"Unknown control_id in evidence: {control_id}")
        if control_id in seen:
            raise EvidenceValidationError(f"Duplicate evidence entry for control_id: {control_id}")
        seen.add(control_id)
        status = record.get("status")
        if status not in ALLOWED_STATUSES:
            raise EvidenceValidationError(f"Invalid status '{status}' for control {control_id}")
        metrics = record.get("evidence_metrics", None)
        if metrics is not None and not isinstance(metrics, dict):
            raise EvidenceValidationError(f"evidence_metrics must be dict or null for control {control_id}")
        result[control_id] = {"status": status, "evidence_metrics": metrics}
    return result
