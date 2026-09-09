# Definition of Done — GB-BESS v0.1

**Status:** Revised — September 2026 strategic realignment. Reorganised around five evidence-based release gates (replacing the earlier raw "≥100 templates / ≥1,000 executions" style targets, per that pass's explicit instruction), rather than a flat checklist. Every checkbox fact from the prior version is preserved below, regrouped under the gate it actually evidences — nothing tracked as done was un-done by this reorganisation, and nothing tracked as pending was marked done. See `docs/benchmark/VALIDATION_FRAMEWORK.md` for the six validation properties (instrument validity, construct validity, sensitivity, discrimination, stability, robustness) this gate structure operationalises, and `docs/project/GAP_ANALYSIS.md` for the specific implementation gaps still open against each gate.

## Gate 1 — Instrument Validity

*Simulator, evaluators, Oracle/Observation, action validation, and Decision Records work correctly.*

- [x] Clean installation (`pip install -e .`)
- [x] CLI execution (`gridactionbench run <scenario-dir> --agent <agent>`, `list-scenarios`, `run-generated`, `coverage`, `run-episode`, `generate-holdouts`)
- [x] Deterministic simulator (`SimpleBessSimulator`) — `gridactionbench/simulators/simple_bess.py`
- [x] Versioned schemas (`EnergyObservationV1`, `AgentActionV1`) — `gridactionbench/schemas/`
- [x] Scenario Oracle implemented — `gridactionbench/core/scenario.py`
- [x] Observation/Oracle separation implemented in code, not just specified (`ADR-005`) — `Scenario.oracle` vs. `Scenario.build_observation()`
- [x] Immutable Decision Records — `gridactionbench/core/decision_record.py`, JSONL, append-only
- [x] ≥15 meaningful evaluators implemented (19 specified, 19 implemented — `gridactionbench/evaluators/gb_bess/`; 19th, `MKT-PREFERRED-ACTION-001`, added 2026-09-09)
- [x] Hard/operational/information separation implemented in code (`ConstraintClass` enum)
- [x] UCV detection implemented — `gridactionbench/core/engine.py`, gated on `ucv_eligible`, not severity alone (definition and open naming/scope question: `docs/benchmark/RELIABILITY_BOUNDARY_MODEL.md`, "UCV's place in this model")
- [x] Escalation evaluation implemented — `gridactionbench/evaluators/gb_bess/hum.py`
- [x] Single-step (Atomic) suite implemented — `suites/gb_bess/v0_1/scenarios/*.yaml`, all 20, plus 300 generated instances (`gridactionbench/scenarios/generator.py`)
- [x] Small multi-step episode suite implemented — all 8 (`gridactionbench/scenarios/gb_bess/episodes.py`; 2 Sequential, 6 Operational, `docs/benchmark/TASK_MODEL.md`), each with a bidirectionally-verified `failure_signature` (`tests/golden/test_episodes.py`)
- [x] Provenance tracked per scenario (`author`/`created_date`, `source_type: synthetic`)
- [x] Versioning enforced per scenario (`scenario_version`, validated by the pydantic `Scenario` model)
- [x] **152/152 tests pass** (`python -m pytest`)
- [ ] Counterfactual support for selected scenarios (architecture designed, `ADR-017`; not built)
- [x] `TrajectoryRecord` for multi-step trials — done 2026-09-09, `gridactionbench/core/trajectory_record.py`, `tests/unit/test_trajectory_record.py` (`docs/benchmark/TASK_MODEL.md`)

**Gate 1 status: satisfied**, with the one remaining open item above (counterfactual support, `ADR-017`) tracked as additive work, not a blocker to the gate itself — an extension, not a correction, of already-correct instrument behaviour.

## Gate 2 — Construct Validity

*Known-good and known-bad baselines behave as expected; metric names measure what they claim.*

- [x] `AlwaysIdleAgent` implemented and run — 6/20 scenarios produce a UCV, as expected of a known-defective baseline
- [x] `AlwaysEscalateAgent` implemented and run — 0 UCVs, but only 85.7% escalation appropriateness (correctly fails `GB-BESS-HUM-020`'s unnecessary-escalation check)
- [x] `RuleBasedAgent` implemented and run — 0 UCVs, 100% on every populated dimension; 57.1% economic decision quality after the best-case-boundary-value fix
- [x] All 8 seeded-failure agents implemented and run, each verified against its documented expected failure mode — 7 via `tests/golden/test_seeded_failure_agents.py`'s 20-scenario sweep, the 8th (`TrustForecastOverActualAgent`, added 2026-09-09) via its matching episode in `tests/golden/test_episodes.py`, since its defect has no surface on any scenario predating the forecast field
- [x] A real defect *found by the benchmark itself* during calibration, not merely by inspection: the parameterised generator surfaced `RuleBasedAgent`'s missing `telemetry.field_status.network` check — direct sensitivity evidence, not a hypothetical (`docs/suites/gb-bess/SCENARIO_TEMPLATES.md`)
- [x] Documented calibration report — `docs/benchmark/CALIBRATION_RESULTS.md`, explicitly marked an informal preview pending Gate 5
- [x] Discrimination shown among the 10 reference/seeded-failure agents (`docs/benchmark/VALIDATION_FRAMEWORK.md`, "Discrimination")
- [ ] Discrimination shown among genuinely capable agent architectures (LLM, optimisation, RL) — none evaluated yet; ceiling-effect risk flagged in `docs/research/BENCHMARK_DESIGN_REVIEW.md` remains untested
- [ ] Construct-validation review completed by an external party (register exists — `docs/project/ASSUMPTIONS.md` — no item has completed external review)
- [x] Capability tagging (`docs/benchmark/CAPABILITY_TAXONOMY.md`) and stress-dimension tagging (`docs/benchmark/STRESS_DIMENSIONS.md`) applied to existing evaluators/Task Families, with reporting-layer slicing (`Report.by_capability`, `ucv_by_u_class`/`ucv_by_complexity_rung`/`ucv_by_autonomy_burden`) — done 2026-09-09, `tests/unit/test_capability_tags.py`, `tests/unit/test_report.py`

**Gate 2 status: partially satisfied.** Strong sensitivity and baseline-level discrimination evidence exists; construct validity against genuinely capable agents and external reviewers remains open, consistent with the strict calibration-before-comparison phase ordering this project has maintained throughout.

## Gate 3 — Operational Depth

*Validated Atomic → Sequential → Operational task progressions exist; ADAPT is genuinely exercised.*

- [x] Atomic task family implemented and validated — 20 hand-authored + 300 generated instances
- [x] Operational task family implemented and validated — 6 episodes (`GB-BESS-EP-003`-`EP-008`), each bidirectionally verified
- [x] Sequential task family (the middle rung: state-dependent, non-changing conditions) — done 2026-09-09, by reclassification: `GB-BESS-EP-001`/`EP-002` were found to already have static conditions and are now tagged `task_mode="Sequential"` (`docs/benchmark/TASK_MODEL.md`); no new scenario content was written
- [ ] ADAPT genuinely exercised — improved but still partial: 4 of 8 episodes now touch it, including `GB-BESS-EP-007`'s forecast-turns-out-wrong case added 2026-09-09; a failed tool call and physical deviation from expectation remain untested (`docs/benchmark/CAPABILITY_TAXONOMY.md`)
- [x] Cross-mode comparison (does good Atomic performance predict Operational reliability, for the same agent) — done 2026-09-09, `docs/benchmark/CROSS_MODE_COMPARISON.md`; answer is no, not reliably, verified concretely for two agents

**Gate 3 status: still not satisfied — one of its two named gaps closes, one remains.** The Sequential-task-mode gap above is now closed, honestly, as a reclassification of existing content rather than a claim of new capability. ADAPT is not: U5 (tool/source failure) and physical-deviation-from-expectation remain untested, coupled to the unresolved `AgentAdapter` interface question (`docs/project/GAP_ANALYSIS.md`). The cross-mode comparison's finding — that a small Operational suite gives uneven exposure to different agents' defects — was reported against the 6-episode suite that existed at the time it ran; it is not retroactively invalidated by the Sequential reclassification (that suite is now known to have had 2 Sequential + 4 Operational episodes, not 6 Operational, but the comparison's actual finding concerned defect-exposure unevenness, which stands either way).

**On scenario/instance counts specifically:** the earlier "≥100 templates / ≥1,000 executions" targets are retired as release criteria. Coverage and validity of what exists — not raw volume — is the standard from this point forward, per the redesign's explicit instruction. The current 20 templates / 300 generated instances (`docs/suites/gb-bess/SCENARIO_TEMPLATES.md`) are evaluated against Gates 2 and 3 above, not against a numeric target.

## Gate 4 — GB Grounding

*At least part of the official benchmark uses frozen, licensed, reproducible GB data and/or genuinely GB-specific operating conditions.*

- [x] GB specificity documented with an explicit benchmark-affecting test — `docs/suites/gb-bess/GB_SPECIFICITY.md` (three features: dynamic network headroom, negative price as core condition, `dt_hours=0.5`)
- [x] Data provenance process documented — `docs/data/DATA_PROVENANCE.md`
- [x] No fake GB specificity claimed — explicit honest self-assessment in `GB_SPECIFICITY.md`
- [x] Current GB AI-energy policy context researched and neutrally framed, not claimed as endorsement — `docs/suites/gb-bess/GB_CONTEXT.md`, `docs/research/DESIGN_EVIDENCE_BASE.md`
- [ ] Dataset licences confirmed and real GB data frozen into the suite — none committed yet; Elexon BMRS redistribution terms remain explicitly unconfirmed (`docs/project/RISK_REGISTER.md` R-16)

**Gate 4 status: partially satisfied.** Three genuinely benchmark-affecting GB features exist at the scenario-design/implementation level; no licence-confirmed real GB dataset is frozen into v0.1 yet. This gate is not satisfied until that changes — scenario-design GB-groundedness alone is not treated as sufficient for a "GB grounding" claim at release.

## Gate 5 — External Review

*At least one credible domain-expert review, preferably multiple reviewers covering relevant areas.*

- [ ] At least one credible external energy-domain review completed
- [ ] Review issues documented (Feedback → Issue → Assessment → Accepted/Rejected → Rationale → Change, `docs/benchmark/METHODOLOGY.md` §8)
- [x] Review question set prepared in advance — `docs/research/EXPERT_REVIEW_CHECKLIST.md`

**Gate 5 status: not satisfied.** No external review has occurred. Nothing in this pass changes that; the strategic realignment is internal specification work, not a substitute for outside validation.

## Release (only after all five gates are satisfied)

- [x] Public repository — `github.com/igwebupower/gridactionbench`, public, pushed
- [ ] Release tag (no `v0.1.0`-style tag cut — premature before all five gates above are satisfied)
- [x] Citation metadata (`CITATION.cff`)
- [ ] Reproducible *results* published (the reproducibility *mechanism* is tested, `tests/reproducibility/`; no official, externally-reproduced result has been published)
- [x] No physical energy-system interaction (architecturally and code-level enforced — `docs/architecture/SECURITY.md`, `ADR-015`)
- [ ] ≥2 LLM (or other genuinely capable) agent configurations evaluated, after Gate 2 is fully satisfied — not before
- [ ] Repeated trials for stochastic agents, once any exist (`docs/project/ASSUMPTIONS.md` A-16)
- [x] Reproducibility metadata captured for every run (git commit, seed, environment — already implemented, `docs/architecture/adr/ADR-009-decision-record-format.md`)

## Current overall status

**Gate 1: satisfied** (with two additive extensions queued, not corrections). **Gate 2: partially satisfied** (strong baseline evidence; external and frontier-agent validation pending). **Gate 3: not satisfied** (Sequential task mode closed 2026-09-09 by reclassification; ADAPT depth — specifically U5/tool-failure — remains a genuine, named gap). **Gate 4: partially satisfied** (scenario-design GB-groundedness exists; licensed real data does not yet). **Gate 5: not satisfied** (no external review yet). This reflects real progress from Phase 1-3 implementation work, reorganised honestly rather than inflated by the reframing itself — moving from a flat checklist to five gates changes how the same facts are grouped, not what they are.
