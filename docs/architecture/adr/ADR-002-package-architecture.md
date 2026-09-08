# ADR-002: Package Architecture

**Status:** Proposed

## Context
The benchmark must support multiple future suites beyond GB-BESS (master brief §65 separates `gridactionbench/` core from `suites/`), while GB-BESS itself needs to ship as a coherent, testable v0.1. The package boundaries need to make "what is suite-agnostic core vs. what is GB-BESS-specific" legible in the repository layout itself, not just in documentation.

## Decision
Two-tier package structure: `gridactionbench/` holds suite-agnostic core (Oracle/Observation/Action/Evaluator/Simulator/Agent interfaces, the runner, reporting, provenance — see `docs/architecture/ARCHITECTURE.md`), while `suites/gb_bess/v0_1/` holds GB-BESS's concrete scenario data, and `baselines/` holds reference/seeded-failure agent implementations that consume the core interfaces. Suite-specific evaluator *implementations* live under `gridactionbench/evaluators/gb_bess/` (a suite-namespaced subpackage of the core evaluators package), keeping the Evaluator interface itself suite-agnostic while its concrete GB-BESS instances are clearly scoped.

## Alternatives considered
- **Single flat package with no suite/core separation** — rejected: would make it structurally ambiguous, as the project grows, whether a given piece of code is safe to reuse for a future non-BESS suite or is GB-BESS-specific; contradicts the project's own stated multi-suite ambition (master brief, project name "GridActionBench" vs. first suite "GB-BESS").
- **A separate top-level repository per suite from day one** — rejected for v0.1: premature separation given only one suite exists; revisit if/when a second suite is seriously planned.

## Consequences
- Positive: a future second suite can be added by adding a new `suites/<name>/` and suite-namespaced evaluator subpackage without touching core interfaces, if those interfaces are well-designed.
- Negative: requires discipline to avoid leaking GB-BESS-specific assumptions (e.g., battery-specific field names) into the nominally suite-agnostic core `Evaluator`/`AgentAdapter` interfaces — flagged as a Phase 1/2 code-review concern, not fully preventable by structure alone.
