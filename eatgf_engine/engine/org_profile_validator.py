from typing import Any, Dict


ALLOWED_ENVIRONMENTS = {"Cloud", "SaaS", "On-Prem", "Hybrid"}


class OrgProfileValidationError(Exception):
    pass


def validate_org_profile(raw: Any) -> Dict[str, Any]:
    if not isinstance(raw, dict):
        raise OrgProfileValidationError("Invalid org_profile: expected JSON object")

    required_fields = ["environment", "ai_usage", "apis_exposed"]
    for field in required_fields:
        if field not in raw:
            raise OrgProfileValidationError(f"Missing required field: {field}")

    environment = raw["environment"]
    if environment not in ALLOWED_ENVIRONMENTS:
        raise OrgProfileValidationError(f"Invalid environment: {environment}")

    ai_usage = raw["ai_usage"]
    if not isinstance(ai_usage, bool):
        raise OrgProfileValidationError("Invalid ai_usage: expected boolean")

    apis_exposed = raw["apis_exposed"]
    if not isinstance(apis_exposed, bool):
        raise OrgProfileValidationError("Invalid apis_exposed: expected boolean")

    return {
        "environment": environment,
        "ai_usage": ai_usage,
        "apis_exposed": apis_exposed,
    }
