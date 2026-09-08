# Definition of Done — GB-BESS v0.1

**Status:** Revised — Phase 1. Core and single-step Scenarios/Calibration items now checked; see `docs/project/BACKLOG.md` for the full Phase 1 completion record. This is the master brief §83 checklist, reproduced here as the project's live tracking artifact (not restated narrative — see the master brief itself for full context on each item).

## Core
- [x] Clean installation (`pip install -e .`)
- [x] CLI execution (`gridactionbench run <scenario-dir> --agent <agent>`, `gridactionbench list-scenarios`)
- [x] Deterministic simulator (`SimpleBessSimulator`) — `gridactionbench/simulators/simple_bess.py`
- [x] Versioned schemas (`EnergyObservationV1`, `AgentActionV1`) — `gridactionbench/schemas/`
- [x] Scenario Oracle implemented — `gridactionbench/core/scenario.py`
- [x] Observation/Oracle separation implemented in code, not just specified (`ADR-005`) — `Scenario.oracle` vs. `Scenario.build_observation()`
- [x] Immutable Decision Records — `gridactionbench/core/decision_record.py`, JSONL, append-only

## Evaluation
- [x] ≥15 meaningful evaluators implemented (18 specified, **18 implemented** — `gridactionbench/evaluators/gb_bess/`)
- [x] Hard/operational/information separation implemented in code (`ConstraintClass` enum; `OBJECTIVE` deliberately has no evaluator, per `docs/suites/gb-bess/EVALUATION_SPEC.md`)
- [x] UCV detection implemented — `gridactionbench/core/engine.py`, gated on `ucv_eligible`, not severity alone
- [x] Escalation evaluation implemented — `gridactionbench/evaluators/gb_bess/hum.py`
- [ ] Counterfactual support for selected scenarios implemented — architecture designed (`ADR-017`), not built in Phase 1 (explicitly deferred)

## Scenarios
- [ ] ≥100 meaningful templates/definitions (20 fully specified and **implemented as scenario files**; templates are Phase 3 work)
- [ ] ≥1,000 executions (20 scenarios × 3 reference agents × ad hoc golden/unit cases executed so far; nowhere near 1,000 distinct scenario executions — Phase 3 work)
- [x] Single-step suite implemented — `suites/gb_bess/v0_1/scenarios/*.yaml`, all 20
- [ ] Small episode suite implemented (6 designed; 0 implemented — explicitly deferred past Phase 1)
- [x] Provenance tracked per scenario (`author`/`created_date`-equivalent fields in the scenario schema; `source_type: synthetic` on every scenario)
- [x] Versioning enforced per scenario (`scenario_version` field, validated by the pydantic `Scenario` model)

## Calibration
- [x] AlwaysIdleAgent implemented and run — 6/20 scenarios produce a UCV, as expected of a known-defective baseline
- [x] AlwaysEscalateAgent implemented and run — 0 UCVs, but only 85.7% escalation appropriateness (correctly fails `GB-BESS-HUM-020`'s unnecessary-escalation check — master brief §22 satisfied empirically, not just by design)
- [x] RuleBasedAgent implemented and run — 0 UCVs, 100% on every populated dimension across the 20 scenarios
- [ ] Seeded failure agents implemented and run (full documented set — `AlwaysChargeAgent`, `IgnoreNetworkAgent`, etc. — deferred to Phase 2/4, per `docs/project/BACKLOG.md`)
- [x] Known failures correctly detected for the three implemented reference agents — see `tests/golden/test_golden_scenarios.py`'s three `test_calibration_*` tests; a full documented calibration *report* (as opposed to passing tests) is still Phase 4 work

## Agent research
- [ ] ≥2 LLM configurations evaluated, after calibration is satisfactory (not before — master brief §28)
- [ ] Repeated trials where appropriate for stochastic agents
- [ ] Reproducibility metadata captured for every run

## Benchmark science
- [x] Benchmark Card (`docs/benchmark/BENCHMARK_CARD.md`)
- [x] Methodology (`docs/benchmark/METHODOLOGY.md`)
- [x] Threat model (`docs/benchmark/THREAT_MODEL.md`)
- [x] Contamination policy (`docs/benchmark/CONTAMINATION_POLICY.md`)
- [x] Holdout policy (`docs/benchmark/PUBLIC_PRIVATE_POLICY.md`)
- [x] Reference Track specification (`docs/benchmark/SUBMISSION_RULES.md`)
- [x] Limitations stated (distributed across `BENCHMARK_CARD.md`, `GB_SPECIFICITY.md`, and per-evaluator/per-ADR limitations sections)
- [ ] Construct-validation review completed (register exists — `docs/project/ASSUMPTIONS.md` — but no item has completed external review yet)

## GB context
- [x] GB specificity documented (`docs/suites/gb-bess/GB_SPECIFICITY.md`)
- [x] Data provenance process documented (`docs/data/DATA_PROVENANCE.md`)
- [x] Dataset licences checked before use (none committed yet; Elexon BMRS explicitly flagged unconfirmed)
- [x] No fake GB specificity claimed (explicit "honest self-assessment" in `GB_SPECIFICITY.md` distinguishes contextual from data-grounded specificity)

## External validation
- [ ] At least one credible external energy-domain review completed
- [ ] Review issues documented (Feedback → Issue → Assessment → Accepted/Rejected → Rationale → Change, per `docs/benchmark/METHODOLOGY.md` §8)

## Release
- [x] Public repository — `github.com/igwebupower/gridactionbench`, public, pushed
- [ ] Release tag (no `v0.1.0`-style tag cut yet — premature before Phase 2-9 complete)
- [x] Citation metadata (`CITATION.cff`)
- [ ] Reproducible results (reproducibility *mechanism* is tested — `tests/reproducibility/`; no official, externally-reproduced *result* has been published)
- [x] No physical energy-system interaction (architecturally enforced — `docs/architecture/SECURITY.md`, `ADR-015` — and now also codebase-enforced: no dependency, schema field, or interface method in `gridactionbench/` addresses a real-world endpoint)

## Current overall status

Phase 0 and Phase 1 (technical spike) complete: 57/57 tests passing, all 20 initial scenarios implemented and running end-to-end through 3 reference agents, Gate 1 acceptance criteria satisfied (`docs/project/BACKLOG.md`). Remaining unchecked items above are Phase 2 (full evaluator catalogue — 18/18 already done, ahead of the ≥15 target) through Phase 9+ work: episode implementation, counterfactual evaluation, seeded failure agents, parameterised scenario generation (≥100 templates, ≥1,000 executions), LLM comparison, external review, and release tagging. This checklist should be updated at the end of every phase, not only at the end of the project.
