# ADR-001: Language and Runtime

**Status:** Proposed (Phase 0 — to be confirmed at Phase 1 kickoff)

## Context
GridActionBench needs a language/runtime that: (a) is accessible to energy-domain contributors and reviewers, most of whom already work in Python-based power-systems tooling (pandapower, PyPSA, PSS/E scripting); (b) has mature, boring schema-validation and testing tooling, since correctness of evaluator logic matters more than raw performance; (c) matches the ecosystem of the prior art reviewed in `docs/research/PRIOR_ART.md` (the benchmarks and tooling surveyed there are predominantly Python-based), lowering the barrier to any future interoperability work.

## Decision
Python 3.11+, using `pydantic` (v2) for schema definition/validation (`EnergyObservationV1`, `AgentActionV1`, Decision Record), `pytest` for the full test strategy (`docs/testing/TEST_STRATEGY.md`), and a standard CLI framework (`typer` or `click`, final choice deferred to Phase 1 implementation) for the CLI entry point (master brief §68).

## Alternatives considered
- **TypeScript/Node** — rejected: weaker ecosystem overlap with power-systems domain tooling and reviewers; no material benefit for a CPU-bound, correctness-focused benchmark.
- **Rust/Go** — rejected for v0.1: performance is not the bottleneck (simulator is intentionally simple, master brief §29-30); would raise the contribution barrier for domain-expert reviewers who are not necessarily systems programmers, contradicting the "independent contributors can participate" governance goal (master brief §59).

## Consequences
- Positive: low barrier to contribution and review; directly reusable patterns from reviewed prior art; mature JSON/JSONL/YAML tooling for the data model.
- Negative: Python's packaging/dependency story requires discipline (pinned lockfile) to keep reproducibility claims (master brief §54) credible — tracked as a Phase 1 setup task in `docs/project/BACKLOG.md`.
