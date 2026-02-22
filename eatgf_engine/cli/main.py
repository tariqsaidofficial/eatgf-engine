import sys
from eatgf_engine.registry.loader import load_registry
from eatgf_engine.registry.validators import RegistryValidationError

import json
from eatgf_engine.engine.evaluator import evaluate_compliance
from eatgf_engine.engine.report import print_compliance_report


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['validate-registry', 'evaluate-compliance'])
    parser.add_argument('registry', help='Registry JSON file')
    parser.add_argument('org_profile', nargs='?', help='Organization profile JSON file')
    parser.add_argument('evidence', nargs='?', help='Evidence JSON file')
    parser.add_argument('--output-json', dest='output_json', help='Output compliance report as JSON')
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
            print("Usage: python -m eatgf_engine.cli.main evaluate-compliance registry_v1.1.json org_profile.json evidence.json [--output-json report.json]")
            exit(1)
        try:
            registry = load_registry(args.registry)
        except RegistryValidationError as e:
            print("Registry validation FAILED:")
            print(str(e))
            exit(2)
        with open(args.org_profile, "r", encoding="utf-8") as f:
            org_profile = json.load(f)
        from eatgf_engine.engine.evidence_loader import load_evidence, EvidenceValidationError
        try:
            evidence = load_evidence(args.evidence, registry.controls)
        except EvidenceValidationError as e:
            print("Evidence validation FAILED:")
            print(str(e))
            exit(2)
        summary = evaluate_compliance(registry.controls, org_profile, evidence)
        print_compliance_report(summary)
        if args.output_json:
            from eatgf_engine.compliance.report_builder import build_report
            from eatgf_engine.compliance.report_serializer import serialize_report
            report = build_report(
                registry_version=registry.version,
                engine_version="1.1",
                evaluation_result=summary
            )
            serialize_report(report, args.output_json)
            print(f"Compliance report written to {args.output_json}")

if __name__ == "__main__":
    main()
