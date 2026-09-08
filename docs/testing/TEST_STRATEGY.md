# Test Strategy

**Status:** Draft — Phase 0 specification; implementation begins Phase 1 (master brief §68 lists "10 golden scenarios" and a CLI as spike deliverables).

## Test categories (master brief §56)

### Unit tests
Target: simulator (`SimpleBessSimulator` state-transition correctness in isolation — SOC math, efficiency application, boundary clamping-that-should-never-happen per `docs/suites/gb-bess/SPECIFICATION.md` §9) and evaluator logic (each entry in `docs/suites/gb-bess/EVALUATION_SPEC.md` tested against hand-constructed pre/post states covering pass, warning, and failure conditions independently of any scenario file or agent).

### Integration tests
Target: the full pipeline, `Scenario -> Observation -> Agent -> Action -> Simulator -> Evaluation -> Decision Record`, using a reference agent (`RuleBasedAgent` or `AlwaysIdleAgent`) to confirm the pipeline wires together correctly end-to-end, independent of whether any individual evaluator's *logic* is itself correct (that is the unit tests' job).

### Golden tests
Target: the indisputable cases from `docs/suites/gb-bess/SCENARIO_CATALOGUE.md` with unambiguous expected outcomes — starting with the master brief's own three worked examples (§50: SOC 90%/max 90% CHARGE 5MW → `PHY-SOC-MAX-001` fail; import headroom 0MW CHARGE 1MW → `NET-IMPORT-HEADROOM-001` fail; SOC 15%/reserve 20% DISCHARGE → `OPS-RESERVE-SOC-001` fail) plus the full initial-20 catalogue once implemented. A golden test's expected result is never adjusted to match an implementation's actual output — a mismatch means either the implementation or the scenario specification is wrong, and that must be resolved explicitly, not silently reconciled.

### Regression tests
Target: every previously identified real failure (a bug found in an evaluator, simulator, or scenario during Phase 4 calibration, Phase 6 adversarial testing, or Phase 7 external review) gets a permanent regression test asserting it stays fixed. Sourced from the Trashchenkov benchmark's own documented practice of finding an evaluator bug via unanimous agent disagreement (`docs/research/PRIOR_ART.md` §1.1 item 4) — any such finding in this project becomes a named regression test, not just a silent code fix.

### Property / invariant tests
At minimum, per master brief §56:
- A deterministic agent (`RuleBasedAgent`, `AlwaysIdleAgent`) given the same scenario and seed always produces the same `AgentActionV1` and the same evaluation result.
- Every valid simulated state transition preserves declared invariants (`min_soc <= soc <= max_soc` always holds post-transition for any action that passed the Action Validator).
- Irrelevant scenario metadata (e.g. `author`, `created_date`) cannot alter any evaluator's physical/operational verdict.
- Every evaluator result carries its `eval_id` and `version` (never silently omitted).
- `scenario_id` is preserved unchanged from Scenario through to Decision Record.

### Reproducibility tests
A fresh environment (clean checkout, pinned dependency install) reproduces a previously published Run's results within defined tolerance (exact match for deterministic agents; distributional match within a documented statistical tolerance for stochastic agents). This is the test category that directly operationalizes master brief §54's reproducibility metadata requirements — if the reproducibility test cannot pass using only the metadata a Decision Record captures, the Decision Record schema is missing something and must be revised.

## Coverage discipline

Every evaluator in `docs/suites/gb-bess/EVALUATION_SPEC.md` requires at least one unit test per pass/warning/failure branch before its `validation_status` may move from `UNIMPLEMENTED` to any later state (`docs/project/DEFINITION_OF_DONE.md`). Every scenario's `review_status` progression (DRAFT → ENGINEERING_REVIEWED → BENCHMARK_REVIEWED → VERIFIED, master brief §48) requires, at minimum, an integration test confirming the scenario executes end-to-end and a golden-test-style assertion of its documented `expected_ucv_behaviour` before it may leave DRAFT.

## What this strategy does not cover

LLM agent *capability* is never asserted or guaranteed by this test suite — the test suite validates that the benchmark correctly measures whatever an agent does, not that any particular agent performs well. Calibration (does the benchmark behave sensibly against known-good and known-bad reference agents) is a related but distinct activity, covered by Phase 4 calibration methodology (`docs/benchmark/METHODOLOGY.md`), not by this test strategy directly, though the golden and property tests here are a precondition for calibration being meaningful at all.
