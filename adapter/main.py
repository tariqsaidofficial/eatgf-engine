"""
EATGF Engine Adapter v1.1
Thin FastAPI wrapper exposing the eatgf-engine evaluation pipeline over HTTP.

Endpoints:
  GET  /health    — liveness check
  GET  /controls  — full v1.1 control catalog (no input required)
  POST /evaluate  — org_profile + evidence → ComplianceReport + registry metadata

Usage:
  pip install -r adapter/requirements.txt
  uvicorn adapter.main:app --reload --port 8000
"""

from contextlib import asynccontextmanager
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from eatgf_engine.compliance.report_builder import build_report
from eatgf_engine.engine.evaluator import evaluate_compliance
from eatgf_engine.engine.org_profile_validator import (
    OrgProfileValidationError,
    validate_org_profile,
)
from eatgf_engine.registry.loader import load_registry

from .schemas import (
    EvaluateRequest,
    EvaluateResponse,
)

ENGINE_VERSION = "1.1.0"
REGISTRY_PATH = Path(__file__).parent.parent / "registry_v1.1.json"

_registry = None  # loaded once at startup


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _registry
    _registry = load_registry(str(REGISTRY_PATH))
    yield


app = FastAPI(
    title="EATGF Engine Adapter",
    description="Thin HTTP adapter for the eatgf-engine evaluation pipeline.",
    version=ENGINE_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Docusaurus dev server
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _build_controls_registry() -> Dict[str, Dict[str, Any]]:
    """Convert loaded registry controls to a serialisable dict for responses."""
    return {
        cid: {
            "control_id": ctrl.control_id,
            "domain": ctrl.domain,
            "atomic_objective": ctrl.atomic_objective,
            "primary_authority": ctrl.primary_authority,
            "authority_class": ctrl.authority_class.value,
            "applicability": {
                "environments": ctrl.applicability.environments,
                "ai_usage": ctrl.applicability.ai_usage,
                "mandatory": ctrl.applicability.mandatory,
            },
        }
        for cid, ctrl in _registry.controls.items()
    }


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    """Liveness check. Returns engine and registry version."""
    return {
        "status": "ok",
        "engine_version": ENGINE_VERSION,
        "registry_version": _registry.version if _registry else None,
    }


@app.get("/controls")
def get_controls():
    """
    Return the full v1.1 control catalog.
    Used by Screen 3 (Evidence Form) to display control titles before evaluation.
    No input required. Response is deterministic and may be cached by the client.
    """
    return {
        "registry_version": _registry.version,
        "controls": list(_build_controls_registry().values()),
    }


@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate(request: EvaluateRequest):
    """
    Evaluate compliance. Accepts org_profile + evidence, returns ComplianceReport
    enriched with controls_registry metadata (used by Screen 4 and Screen 5).

    Error codes:
      422 — org_profile_validation_error | evidence_validation_error
    """
    # 1. Validate org_profile via engine validator (fail-fast, canonical errors)
    try:
        org_profile = validate_org_profile(request.org_profile.model_dump())
    except OrgProfileValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail={"error": "org_profile_validation_error", "message": str(exc)},
        )

    # 2. Validate evidence control IDs against loaded registry
    evidence: Dict[str, Dict[str, str]] = {}
    for control_id, entry in request.evidence.items():
        if control_id not in _registry.controls:
            raise HTTPException(
                status_code=422,
                detail={
                    "error": "evidence_validation_error",
                    "message": f"Unknown control_id: {control_id!r}. "
                    f"Valid IDs: {sorted(_registry.controls.keys())}",
                },
            )
        evidence[control_id] = {"status": entry.status}

    # 3. Run evaluation
    eval_result = evaluate_compliance(_registry.controls, org_profile, evidence)

    # 4. Build structured report
    report = build_report(_registry.version, ENGINE_VERSION, eval_result)

    # 5. Enrich response with full registry metadata (required by Screen 5)
    controls_registry = _build_controls_registry()

    # 6. Construct final response from dataclass + enrichment
    report_dict = asdict(report)
    return {
        **report_dict,
        "controls_registry": controls_registry,
    }
