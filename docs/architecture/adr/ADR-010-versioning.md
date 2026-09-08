# ADR-010: Versioning

**Status:** Proposed

## Context
Master brief §45-46 requires independent versioning of framework, suite, scenario set, evaluator set, and simulator, with every published result citing all of them.

## Decision
SemVer for framework, suite, scenario set, evaluator set, and simulator, each versioned and released independently (full rationale and rules in `docs/benchmark/VERSIONING.md`, which this ADR defers to as the canonical detailed policy). This ADR records the *architectural* decision that these are five genuinely separate version axes represented by five separate fields in every Decision Record (`docs/benchmark/SPECIFICATION.md` §7) and Report (`docs/architecture/DATA_MODEL.md`), not a single combined version string that would need lossy parsing to recover the individual components.

## Alternatives considered
- **A single combined version string (e.g. `gb-bess-0.1.0-eval-0.1.0-sim-0.1.0`)** — rejected: fragile to parse, easy to get wrong when only one component changes, and obscures rather than clarifies which specific artifact changed between two results.
- **Calendar versioning (e.g. `2026.09`) instead of SemVer** — rejected: SemVer's MAJOR/MINOR/PATCH distinction directly encodes the comparability information (`docs/benchmark/VERSIONING.md`, "SemVer interpretation") that calendar versioning does not — a MAJOR bump signals "do not directly compare," which is exactly the information consumers of published results need.

## Consequences
- Positive: comparability judgments (can result A be directly compared to result B?) are answerable mechanically from version metadata alone, without needing to read a changelog narrative.
- Negative: five independent version numbers is more bookkeeping overhead than one; accepted because the alternative (one number) actively misleads by implying artifacts changed together when master brief §45 explicitly requires them not to.
