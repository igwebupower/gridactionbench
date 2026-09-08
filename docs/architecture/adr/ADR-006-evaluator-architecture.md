# ADR-006: Evaluator Architecture

**Status:** Proposed

## Context
Master brief §23-24 requires deterministic evaluation of physical/operational constraints, independently versioned evaluators, and a documented specification format. Prior art (`docs/research/PRIOR_ART.md`, `docs/research/POWERAGENTBENCH_REVIEW.md`) consistently confirms deterministic recomputation over LLM-judging as the correct default for this class of benchmark.

## Decision
Each evaluator is an independent, self-contained unit implementing a common `Evaluator` interface (`docs/architecture/ARCHITECTURE.md`), carrying its own `eval_id`, `version`, and `criticality` as static metadata, and returning a structured `EvaluationResult` (`docs/architecture/DATA_MODEL.md`). Evaluators do not share mutable state and do not call each other directly — where one evaluator's failure is a precondition for another's relevance (e.g. `ADV-INSTRUCTION-OVERRIDE-001` is *derived from* the results of the relevant PHY/NET/OPS evaluators, per `docs/suites/gb-bess/EVALUATION_SPEC.md`), that dependency is expressed by the Evaluation Engine's orchestration logic reading multiple `EvaluationResult`s, not by evaluator-to-evaluator coupling.

## Alternatives considered
- **A single monolithic "evaluate everything" function per scenario** — rejected: makes independent evaluator versioning (master brief §45) and evaluator-level unit testing (master brief §56) structurally awkward; a bug fix to one constraint check would risk unintended side effects on unrelated checks.
- **LLM-judge for any evaluator whose logic is "complicated" (e.g. the derived ADV evaluator)** — rejected even for the seemingly more complex derived-evaluator case: `ADV-INSTRUCTION-OVERRIDE-001`'s logic is fully expressible as a deterministic function of other evaluators' results, so no judge is needed even there; this ADR treats "deterministic first" as a default to be defeated by evidence, not a default to be abandoned at the first sign of complexity.

## Consequences
- Positive: each evaluator can be independently unit-tested, golden-tested, and versioned exactly as `docs/benchmark/VERSIONING.md` requires; a QC finding like the Trashchenkov benchmark's off-by-one bug (`docs/research/PRIOR_ART.md` §1.1 item 4) is isolated to one evaluator's diagnosis and fix.
- Negative: cross-cutting evaluators (like the ADV one) require careful Evaluation Engine orchestration logic to avoid becoming a second, undocumented place where scoring rules live — mitigated by keeping that orchestration logic itself documented in `docs/suites/gb-bess/EVALUATION_SPEC.md` per-evaluator, not left implicit in code.
