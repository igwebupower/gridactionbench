# ADR-005: Oracle / Observation Separation

**Status:** Proposed

## Context
Master brief §9 requires a strict separation between ground truth (Oracle) and what the agent believes (Observation), explicitly to enable rigorous testing of stale, missing, incorrect, and contradictory data. This is arguably the single most load-bearing design decision in the entire benchmark — without it, the DATA and HUM scenario families (7 of the initial 20 scenarios, plus 2 of 6 episodes) have no coherent definition.

## Decision
`Oracle` and `EnergyObservationV1` are modeled as two distinct data structures, both derived from a single `Scenario` definition but never conflated into one object at any point in the pipeline (`docs/architecture/ARCHITECTURE.md`, "Oracle / Observation separation"). The `Evaluation Engine` receives both; the `AgentAdapter` receives only the Observation. A scenario's `observation_generation` spec explicitly declares how the Observation relates to the Oracle for that scenario (identity, redaction, or deliberate corruption) — never a generic, implicit "observations are always a truncated oracle" rule.

## Alternatives considered
- **Single unified state object, with agent access mediated by a generic field-visibility mask** — rejected: cannot express DATA-scenario cases where the Observation is not merely incomplete but actively wrong (e.g. `GB-BESS-DATA-017`'s implausible headroom value, which does not exist in the Oracle at all) — a visibility mask can hide fields, but cannot substitute a false value for a hidden one.
- **Generate Observations by a fixed, scenario-independent noise/corruption model** — rejected: would make scenario authors unable to precisely control which specific failure mode (missing vs. stale vs. conflicting vs. implausible) each DATA scenario tests, undermining construct validity (master brief §49) for that entire scenario family.

## Consequences
- Positive: every DATA/HUM scenario's grading condition is unambiguous and independently verifiable by a reviewer reading the scenario file, since Oracle and Observation are both explicit, not derived.
- Negative: scenario authoring requires specifying both structures explicitly, which is more verbose than a single-state-plus-mask design — accepted as a worthwhile cost for construct validity.
