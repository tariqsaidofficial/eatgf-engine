import json
from typing import Dict

from .models import (
    Registry,
    Control,
    LifecycleState,
    AuthorityClass,
    Applicability,
    RelationshipSet,
    Decomposition,
)
from .validators import run_all_validations

def load_registry(path: str) -> Registry:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    controls: Dict[str, Control] = {}

    for c in raw["controls"]:
        applicability = Applicability(
            environments=c["applicability"]["environments"],
            ai_usage=c["applicability"]["ai_usage"],
            mandatory=c["applicability"]["mandatory"],
        )

        relationships = RelationshipSet(
            implements=c["relationships"].get("implements", []),
            enforces=c["relationships"].get("enforces", []),
            requires=c["relationships"].get("requires", []),
        )

        decomposition = None
        if c.get("decomposition"):
            decomposition = Decomposition(
                clause=c["decomposition"]["clause"],
                justification=c["decomposition"]["justification"],
            )

        control = Control(
            control_id=c["control_id"],
            domain=c["domain"],
            primary_authority=c["primary_authority"],
            authority_class=AuthorityClass(c["authority_class"]),
            atomic_objective=c["atomic_objective"],
            lifecycle_state=LifecycleState(c["lifecycle_state"]),
            applicability=applicability,
            relationships=relationships,
            decomposition=decomposition,
        )

        controls[control.control_id] = control

    registry = Registry(version=raw["version"], controls=controls)

    run_all_validations(registry)

    return registry
