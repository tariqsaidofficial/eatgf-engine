# EATGF Engine v1.1.0

## Deterministic Governance-as-Code

This repository contains the canonical, institutionally frozen EATGF Engine v1.1.0. It is architecturally real, audit-grade, and strictly aligned with the published whitepaper and annex.

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

For full details, see docs/whitepaper_v1.1.md and docs/annex_v1.1.md.
