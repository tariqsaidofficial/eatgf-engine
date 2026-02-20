from typing import Dict, Any
from eatgf_engine.registry.models import Control
from .applicability import get_applicable_controls

ALLOWED_STATUSES = {"COMPLIANT", "NON_COMPLIANT", "PARTIAL", "NOT_TESTED"}

def evaluate_compliance(controls: Dict[str, Control], org_profile: Dict[str, Any], evidence: Dict[str, Any]):
    applicable = get_applicable_controls(controls, org_profile)
    results = {}
    domain_counts = {}
    for cid, ctrl in controls.items():
        if cid not in applicable:
            results[cid] = {"status": "NOT_APPLICABLE", "domain": ctrl.domain}
            continue
        ev = evidence.get(cid)
        status = ev["status"] if ev and "status" in ev else "NOT_TESTED"
        if status not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status '{status}' for control {cid}")
        results[cid] = {"status": status, "domain": ctrl.domain}
        # Domain breakdown
        domain_counts.setdefault(ctrl.domain, {"applicable": 0, "compliant": 0})
        domain_counts[ctrl.domain]["applicable"] += 1
        if status == "COMPLIANT":
            domain_counts[ctrl.domain]["compliant"] += 1
    # Aggregation
    total_applicable = sum(1 for v in results.values() if v["status"] != "NOT_APPLICABLE")
    total_compliant = sum(1 for v in results.values() if v["status"] == "COMPLIANT")
    total_partial = sum(1 for v in results.values() if v["status"] == "PARTIAL")
    total_non_compliant = sum(1 for v in results.values() if v["status"] == "NON_COMPLIANT")
    total_not_tested = sum(1 for v in results.values() if v["status"] == "NOT_TESTED")
    compliance_percent = (total_compliant / total_applicable * 100) if total_applicable else 0.0
    domain_breakdown = {
        d: {
            "applicable": v["applicable"],
            "score_percent": (v["compliant"] / v["applicable"] * 100) if v["applicable"] else 0.0
        }
        for d, v in domain_counts.items()
    }
    return {
        "results": results,
        "total_applicable": total_applicable,
        "total_compliant": total_compliant,
        "total_partial": total_partial,
        "total_non_compliant": total_non_compliant,
        "total_not_tested": total_not_tested,
        "compliance_percent": compliance_percent,
        "domain_breakdown": domain_breakdown
    }
