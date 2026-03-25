# EATGF Engine v1.1.0

![CI](https://github.com/tariqsaidofficial/eatgf-engine/actions/workflows/engine-ci.yml/badge.svg)

## Deterministic Governance-as-Code

This repository contains the canonical, institutionally frozen EATGF Engine v1.1.0. It is architecturally real, audit-grade, and strictly aligned with the published whitepaper and annex.

### Installation

```bash
pip install -e .
```

After installation, use the CLI entrypoint:

```bash
eatgf-engine validate-registry registry_v1.1.json
eatgf-engine evaluate-compliance registry_v1.1.json org_profile.json evidence.json --format human
eatgf-engine evaluate-compliance registry_v1.1.json org_profile.json evidence.json --format json --output-json compliance_report.json
```

### CLI Contract (v1.1)

- Commands:
  - `validate-registry`
  - `evaluate-compliance`
- Output flags:
  - `--format human|json` (default: `human`)
  - `--output-json <path>`

### org_profile Contract (v1.1)

Required fields:

- `environment` (allowed values only: `Cloud`, `SaaS`, `On-Prem`, `Hybrid`)
- `ai_usage` (boolean: `true`/`false`)
- `apis_exposed` (boolean: `true`/`false`)

The engine uses fail-fast validation for `org_profile.json`. Missing fields or invalid values are rejected with explicit error messages.

### Key Features

- Deterministic compliance computation
- Strict single authority mapping (no weighted scoring, no heuristics)
- Immutable registry and control IDs
- Audit-grade reporting contract
- Governance-as-Code architecture
- No roadmap or marketing content

### Version Policy

- v1.1.0 is a frozen baseline
- No structural changes permitted without ADR and version increment
- All enhancements (Strict Mode, BAI, etc.) require formal review

### Structure

```
/eatgf_engine
  ├── engine/
  ├── registry/
  ├── docs/
  │   ├── whitepaper_v1.1.md
  │   ├── annex_v1.1.md
  ├── examples/
  │   ├── registry_v1.1.json
  │   ├── org_profile.json
  │   ├── evidence.json
  │   ├── compliance_report.json
  ├── LICENSE
  ├── README.md
  └── CHANGELOG.md
```

### Baseline Declaration

- Freeze: v1.1.0
- Whitepaper and annex are synchronized
- Engine is deterministic and audit-traceable
- Registry is append-only and immutable

### Authority Model

- Single primary authority per control
- No in-place mutation post-activation
- Decomposition policy: ≤2 per clause/domain

### Reporting

- Deterministic, machine-grade
- No undocumented fields

### For All Contributions

- v1.2 and beyond require ADR and version increment
- No silent evolution permitted

---

## Related Projects

- **EATGF Framework (Knowledge Core)**
  [tariqsaidofficial/eatgf-framework](https://github.com/tariqsaidofficial/eatgf-framework)

- **Governance Documentation Portal**
  [tariqsaidofficial/governance-docs-site](https://github.com/tariqsaidofficial/governance-docs-site)

---

For full details, see [docs/whitepaper_v1.1.md](docs/whitepaper_v1.1.md) and [docs/annex_v1.1.md](docs/annex_v1.1.md).
