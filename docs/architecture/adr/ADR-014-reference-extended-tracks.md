# ADR-014: Reference / Extended Tracks

**Status:** Proposed

## Context
Master brief §41 requires a controlled-comparison track and a permissive-experimentation track, explicitly never treated as equivalent.

## Decision
Two tracks, modeled directly on MLPerf's Closed/Open division precedent (`docs/research/PRIOR_ART.md` §4): **Reference Track** fixes benchmark/suite/scenario/evaluator/simulator versions, the observation/action schema, and any tool/validation budget, varying only agent architecture; **Extended Track** permits additional tools, retrieval, alternate simulators, or novel workflows, always reported with an explicit delta from the Reference configuration. Full protocol in `docs/benchmark/SUBMISSION_RULES.md`; scoring-separation rule in `docs/benchmark/SCORING.md`.

## Alternatives considered
- **A single track with a "notes" field for deviations** — rejected: a free-text notes field is too easy to omit or understate, and does not structurally prevent a report from placing incomparable results in the same table — exactly the failure mode MLPerf's Closed/Open naming and enforcement exists to prevent.
- **No Extended Track at all (Reference-only)** — rejected: would foreclose exactly the kind of experimentation (novel tool use, retrieval-augmented agents) that is itself a legitimate research question about whether such augmentation improves action validity — the benchmark should be able to measure that, just not conflate it with the controlled comparison.

## Consequences
- Positive: enables both controlled comparison (Reference) and open-ended capability exploration (Extended) without either undermining the other's interpretability.
- Negative: requires discipline in reporting tooling (`docs/architecture/ARCHITECTURE.md`, reporting layer) to enforce the track label on every result — a structural/schema-level enforcement point (the Report schema in `docs/architecture/DATA_MODEL.md` should make track a required field), not just a documentation convention.
