# ADR-007: Scenario Representation

**Status:** Proposed

## Context
Scenarios must be human-authorable and reviewable (Phase 0 requires fully specifying 20 scenarios by hand before any generation tooling exists — master brief §51), while also being machine-validatable and, from Phase 3 onward, generatable from parameterised templates (master brief §53).

## Decision
Scenarios are represented as YAML files matching the schema in `docs/architecture/DATA_MODEL.md` ("Scenario file"), one file per concrete scenario instance. Phase 3 parameterised templates are a distinct, separately-specified file type (a template plus a generator config, not a scenario file itself) that *produces* concrete scenario YAML/JSON instances at generation time — the runner and evaluators only ever consume concrete scenario instances, never templates directly, keeping the execution path's input format single and simple regardless of how elaborate scenario generation becomes.

## Alternatives considered
- **JSON instead of YAML** — rejected for authoring: YAML's support for comments and its lower syntactic noise materially help human scenario authors and reviewers (a Phase 0/7 audience that includes non-programmer domain experts); JSON remains the wire/serialization format for `EnergyObservationV1`/`AgentActionV1`/Decision Records, where machine consumption dominates and comments are not needed.
- **Python code as the scenario format (i.e., scenarios defined as Python objects/functions)** — rejected: makes scenarios harder for a non-engineering domain reviewer to read and audit, and blurs the line between "data a reviewer can approve" and "code that must be trusted not to have side effects" — a meaningful distinction for a benchmark whose credibility depends on scenario review (master brief §48).

## Consequences
- Positive: scenario files are diffable, reviewable in a pull request, and readable by the Phase 7 external domain reviewers without requiring them to read Python.
- Negative: YAML's type-looseness (e.g. `0.10` vs `"0.10"`) requires strict schema validation at load time to avoid silent data-quality bugs in the scenario files themselves — a validation step planned for Phase 1's scenario-loading implementation, not yet built.
