# Validation Framework

**Status:** New — September 2026 strategic realignment. Names six validation properties GridActionBench must demonstrate about itself, and states current evidence for each honestly, distinguishing what has actually been checked from what is merely designed to be checkable. This document does not introduce new evaluators or new pass/fail logic — it organises validation work that is partly already done (`docs/benchmark/CALIBRATION_RESULTS.md`, the golden-test suite) and partly still pending, under the six named properties below. It is the operational counterpart to `docs/project/DEFINITION_OF_DONE.md`'s Gate 1/Gate 2 (see that document's revised gate structure).

## Why this exists as its own document

`docs/research/EXPERT_REVIEW_CHECKLIST.md` already asks domain reviewers pointed questions about specific assumptions. `docs/project/DEFINITION_OF_DONE.md` already tracks whether calibration and golden tests exist. Neither document previously organised the underlying *validation properties* being checked into a named framework a reader could audit against — "is GridActionBench itself a good benchmark" was answered implicitly, scattered across many documents, rather than against six explicit, checkable properties. This document is that checklist; it does not replace either existing document, and cross-references both.

## The six properties

### 1. Instrument validity

**Question:** do the simulator, evaluators, Oracle/Observation separation, action validation, and Decision Records actually work correctly — independent of any agent's behaviour?

**Current evidence:** yes, to the extent 105 passing tests (`python -m pytest`) can show it — `tests/unit/test_simulator.py` verifies deterministic reproducibility and physical invariants (energy conservation, efficiency direction, timestep linearity); `tests/unit/test_evaluators.py` exercises PASS/WARNING/FAIL/NOT_APPLICABLE branches across all families; `tests/golden/test_golden_scenarios.py` checks 10 scenarios' evaluator outputs against master-brief-derived worked examples; `tests/integration/test_pipeline.py` verifies the full pipeline end-to-end, including JSONL round-trips. This maps to `docs/project/DEFINITION_OF_DONE.md`'s Gate 1 ("Instrument Validity" — see that document's revised gate structure).

**Not yet covered:** no external party has independently re-derived any of these test expectations from the specification documents alone (i.e., the tests were written by the same process that wrote the specification, which is normal for Phase 1-3 work but is a real limitation until Gate 5/external review provides an independent check).

### 2. Construct validity

**Question:** does a named metric actually measure what its name claims?

**Current evidence:** `docs/benchmark/METHODOLOGY.md` §9 already states this discipline explicitly and gives a concrete example (`HUM-ESCALATE-CRITICAL-DATA-001`'s narrow statistical power on Unnecessary Escalation Rate in the hand-authored 20, later strengthened by the generator's `HUM-UNNECESSARY` template — `docs/suites/gb-bess/SCENARIO_TEMPLATES.md`). `docs/project/ASSUMPTIONS.md` tracks per-assumption confidence and domain-review status.

**Not yet covered:** no assumption in `docs/project/ASSUMPTIONS.md` has completed external domain review (every row's "Needs domain review?" column is "Yes" or explicitly "Low priority," none are closed) — construct validity claims remain provisional pending Gate 5.

### 3. Sensitivity

**Question:** do known-defective agents fail where expected?

**Current evidence:** the strongest validation category GridActionBench has today. All 8 seeded-failure agents (`baselines/seeded_failures/`) are verified against their documented expected failure mode — 7 via `tests/golden/test_seeded_failure_agents.py`'s 20-scenario sweep; the 8th, `TrustForecastOverActualAgent` (added 2026-09-09), whose defect only manifests once a price-forecast field is present, via `tests/golden/test_episodes.py`'s `GB-BESS-EP-007` check — and the parameterised generator independently *found* a real defect in `RuleBasedAgent` (the missing `telemetry.field_status.network` check) that the hand-authored 20 had not surfaced — direct evidence the sensitivity-checking process itself works, not just that it exists on paper (`docs/suites/gb-bess/SCENARIO_TEMPLATES.md`, "What generating this set actually found").

**Not yet covered:** sensitivity has only been checked at C0/Atomic+Operational scale, against a small (300-instance) generated set, using placeholder parameter ranges (`docs/project/ASSUMPTIONS.md`). A defective agent that happens to fail only outside the currently-generated parameter ranges would not currently be caught.

### 4. Discrimination

**Question:** do different, genuinely capable agent architectures produce distinguishable reliability profiles on at least some Task Families — i.e., does the benchmark avoid a ceiling or floor effect that makes all competent agents look the same?

**Current evidence:** `docs/benchmark/CALIBRATION_RESULTS.md` shows real discrimination among the three reference agents alone (`AlwaysIdleAgent`: 6/20 UCVs; `AlwaysEscalateAgent`: 0 UCVs but 85.7% escalation appropriateness; `RuleBasedAgent`: 0 UCVs, 100% on populated dimensions, 57.1% economic decision quality) — these are meaningfully different profiles, not three agents converging on the same numbers.

**Not yet covered — flagged as an open risk, not resolved:** `docs/research/BENCHMARK_DESIGN_REVIEW.md`'s existing "Task structure — assessed" finding already raises a ceiling-effect concern for competent agents specifically (as opposed to the deliberately-simple reference agents above), citing a comparable benchmark's own reported near-1.0 ceiling on frontier models against a public split. This remains untested — GridActionBench has not yet evaluated any agent architecture sophisticated enough for a ceiling effect to be a live risk (no LLM or optimisation-based agent has been run against GB-BESS as of this document). This is exactly why the redesign's own instruction to calibrate on conventional baselines before frontier comparisons (already GridActionBench policy, `docs/project/PROJECT_PLAN.md`'s Phase 8 gating) matters — discrimination among simple agents is necessary evidence but not sufficient evidence that the benchmark discriminates among strong ones.

### 5. Stability

**Question:** do deterministic baselines reproduce exactly?

**Current evidence:** yes — `tests/reproducibility/test_determinism.py` verifies deterministic re-run and fresh-load reproducibility; `capture_git_commit()`'s memoization fix (this session's CHANGELOG) was itself found by treating test-suite performance as a signal worth investigating, an example of the stability-checking discipline catching an unrelated real issue as a side effect.

**Not yet covered:** stability has not been checked across a machine/OS boundary (all testing to date has occurred in one development environment) or across a Python patch version bump.

### 6. Robustness

**Question:** do irrelevant perturbations leave results unchanged, while meaningful operational changes are correctly detected?

**Current evidence:** partial. `docs/benchmark/PUBLIC_PRIVATE_POLICY.md`'s acceptance criteria for a generated instance already include "no minor perturbation of the instance's parameters should flip its correct-action classification in an unintended way," but this is stated as an acceptance criterion for holdout instances, not yet implemented as an automated check run against the generator's actual output.

**Not yet covered:** no automated robustness sweep exists (e.g., "does adding 1e-9 to every SOC value change any evaluator's PASS/FAIL verdict" — it should not, given the documented `epsilon=1e-6` tolerance, `docs/suites/gb-bess/SPECIFICATION.md` §9.7, but this has not been explicitly tested as its own property beyond what the golden/unit tests incidentally exercise).

## Leakage resistance and evaluator correctness

Two further properties the redesign explicitly names are already covered by existing documents and are cross-referenced here rather than restated: **leakage resistance** (`docs/benchmark/CONTAMINATION_POLICY.md`, `docs/benchmark/PUBLIC_PRIVATE_POLICY.md`) and **evaluator correctness via golden tests** (covered under "Instrument validity," above, and `docs/research/PRIOR_ART.md` §1.1 item 4's "unanimous agent disagreement as evaluator QC signal" pattern, not yet exercised in practice since GridActionBench has not yet run enough independent agent architectures for unanimous disagreement to be observable).

## Standing principle

**Agent disagreement with an evaluator is not assumed to mean the agents are wrong.** This principle already exists in `docs/research/PRIOR_ART.md` §1.1 item 4 and `docs/benchmark/SCORING.md`'s treatment of `INDETERMINATE`/`EVALUATOR_ERROR` as benchmark-health signals, not agent-performance signals. This document restates it as a cross-cutting rule for all six validation properties above: a validation framework that only ever concludes "the agent was wrong" has stopped validating the benchmark and started merely grading agents.
