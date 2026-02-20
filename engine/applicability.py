from typing import Dict, Any, Set
from eatgf_engine.registry.models import Control

def is_control_applicable(control: Control, org_profile: Dict[str, Any]) -> bool:
    # Environment check
    env = org_profile.get("environment")
    if env not in control.applicability.environments:
        return False
    # AI usage check
    ai_flag = org_profile.get("ai_usage", False)
    if control.applicability.ai_usage == "Conditional":
        if not ai_flag:
            return False
    # API trigger (future)
    # For v1.1, ignore unless control_id == "EATGF-API-SEC-01"
    if control.control_id == "EATGF-API-SEC-01":
        if not org_profile.get("apis_exposed", False):
            return False
    return True

def get_applicable_controls(controls: Dict[str, Control], org_profile: Dict[str, Any]) -> Set[str]:
    return {cid for cid, ctrl in controls.items() if is_control_applicable(ctrl, org_profile)}
