import sys
from eatgf_engine.registry.loader import load_registry
from eatgf_engine.registry.validators import RegistryValidationError

import json
from dataclasses import asdict
from eatgf_engine.engine.evaluator import evaluate_compliance
from eatgf_engine.engine.report import print_compliance_report
from eatgf_engine.engine.org_profile_validator import (
    validate_org_profile,
    OrgProfileValidationError,
)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog="eatgf-engine",
        description="Deterministic compliance CLI for EATGF Engine v1.1.0"
    )
    parser.add_argument('command', choices=['validate-registry', 'evaluate-compliance'])
    parser.add_argument('registry', help='Registry JSON file')
    parser.add_argument('org_profile', nargs='?', help='Organization profile JSON file')
    parser.add_argument('evidence', nargs='?', help='Evidence JSON file')
    parser.add_argument('--output-json', dest='output_json', help='Write compliance report JSON to a file path')
    parser.add_argument(
        '--format',
        choices=['human', 'json'],
        default='human',
        help='Output format for evaluate-compliance command (default: human)'
    )
    args = parser.parse_args()

    if args.command == 'validate-registry':
        try:
            registry = load_registry(args.registry)
            print("Registry Loaded Successfully")
            print(f"Version: {registry.version}")
            print(f"Controls: {len(registry.controls)}")
            print("Validation: PASSED")
        except RegistryValidationError as e:
            print("Validation FAILED:")
            print(str(e))
            exit(2)
    elif args.command == 'evaluate-compliance':
        if not (args.org_profile and args.evidence):
            print("Usage: eatgf-engine evaluate-compliance registry_v1.1.json org_profile.json evidence.json [--format human|json] [--output-json report.json]")
            exit(1)
        try:
            registry = load_registry(args.registry)
        except RegistryValidationError as e:
            print("Registry validation FAILED:")
            print(str(e))
            exit(2)
        with open(args.org_profile, "r", encoding="utf-8") as f:
            raw_org_profile = json.load(f)
        try:
            org_profile = validate_org_profile(raw_org_profile)
        except OrgProfileValidationError as e:
            print("Org profile validation FAILED:")
            print(str(e))
            exit(2)
        from eatgf_engine.engine.evidence_loader import load_evidence, EvidenceValidationError
        try:
            evidence = load_evidence(args.evidence, registry.controls)
        except EvidenceValidationError as e:
            print("Evidence validation FAILED:")
            print(str(e))
            exit(2)
        summary = evaluate_compliance(registry.controls, org_profile, evidence)
        from eatgf_engine.compliance.report_builder import build_report
        from eatgf_engine.compliance.report_serializer import serialize_report
        report = build_report(
            registry_version=registry.version,
            engine_version="1.1.0",
            evaluation_result=summary
        )

        if args.format == 'human':
            print_compliance_report(summary)
        else:
            print(json.dumps(asdict(report), indent=2, sort_keys=True))

        if args.output_json:
            serialize_report(report, args.output_json)
            print(f"Compliance report written to {args.output_json}")

if __name__ == "__main__":
    main()
