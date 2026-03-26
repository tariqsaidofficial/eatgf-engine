import json
from dataclasses import asdict
from typing import Optional

import typer

from eatgf_engine.engine.evaluator import evaluate_compliance
from eatgf_engine.engine.org_profile_validator import (
    OrgProfileValidationError,
    validate_org_profile,
)
from eatgf_engine.engine.report import print_compliance_report
from eatgf_engine.registry.loader import load_registry
from eatgf_engine.registry.validators import RegistryValidationError

app = typer.Typer(
    name='eatgf-engine',
    add_completion=False,
    help='Deterministic compliance CLI for EATGF Engine v1.1.0',
)


@app.command('validate-registry')
def validate_registry(registry: str = typer.Argument(..., help='Registry JSON file')) -> None:
    try:
        loaded_registry = load_registry(registry)
        typer.echo('Registry Loaded Successfully')
        typer.echo(f'Version: {loaded_registry.version}')
        typer.echo(f'Controls: {len(loaded_registry.controls)}')
        typer.echo('Validation: PASSED')
    except RegistryValidationError as exc:
        typer.echo('Validation FAILED:')
        typer.echo(str(exc))
        raise typer.Exit(code=2)


@app.command('evaluate-compliance')
def evaluate_compliance_command(
    registry: str = typer.Argument(..., help='Registry JSON file'),
    org_profile: str = typer.Argument(..., help='Organization profile JSON file'),
    evidence: str = typer.Argument(..., help='Evidence JSON file'),
    output_json: Optional[str] = typer.Option(
        None,
        '--output-json',
        help='Write compliance report JSON to a file path',
    ),
    output_format: str = typer.Option(
        'human',
        '--format',
        help='Output format for evaluate-compliance command (human|json)',
        case_sensitive=False,
    ),
) -> None:
    normalized_format = output_format.lower()
    if normalized_format not in {'human', 'json'}:
        typer.echo("Invalid --format value. Allowed values: 'human', 'json'.")
        raise typer.Exit(code=2)

    try:
        loaded_registry = load_registry(registry)
    except RegistryValidationError as exc:
        typer.echo('Registry validation FAILED:')
        typer.echo(str(exc))
        raise typer.Exit(code=2)

    with open(org_profile, 'r', encoding='utf-8') as file_obj:
        raw_org_profile = json.load(file_obj)

    try:
        validated_org_profile = validate_org_profile(raw_org_profile)
    except OrgProfileValidationError as exc:
        typer.echo('Org profile validation FAILED:')
        typer.echo(str(exc))
        raise typer.Exit(code=2)

    from eatgf_engine.engine.evidence_loader import EvidenceValidationError, load_evidence

    try:
        loaded_evidence = load_evidence(evidence, loaded_registry.controls)
    except EvidenceValidationError as exc:
        typer.echo('Evidence validation FAILED:')
        typer.echo(str(exc))
        raise typer.Exit(code=2)

    summary = evaluate_compliance(loaded_registry.controls, validated_org_profile, loaded_evidence)

    from eatgf_engine.compliance.report_builder import build_report
    from eatgf_engine.compliance.report_serializer import serialize_report

    report = build_report(
        registry_version=loaded_registry.version,
        engine_version='1.1.0',
        evaluation_result=summary,
    )

    if normalized_format == 'human':
        print_compliance_report(summary)
    else:
        typer.echo(json.dumps(asdict(report), indent=2, sort_keys=True))

    if output_json:
        serialize_report(report, output_json)
        typer.echo(f'Compliance report written to {output_json}')


def main() -> None:
    app()


if __name__ == '__main__':
    main()
