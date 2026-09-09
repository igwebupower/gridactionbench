# Implementation Backlog

**Status:** Revised — September 2026 strategic realignment adds the prioritised backlog below, on top of the unchanged Phase 1 technical-spike backlog that follows it. The Phase 1 backlog is retained in full (Gate 1 was satisfied and nothing below invalidates that) — this file now has two sections: forward-looking priorities from the redesign, then the original Phase 1 completion record.

## Prioritised backlog — September 2026 strategic realignment

Derived from `docs/project/GAP_ANALYSIS.md`'s architecture gap analysis. **Nothing in this section is implemented by this pass** — per that pass's explicit stop condition, this is a queued work list for the next implementation phase, not a claim of work done. Priorities: **P0** benchmark correctness / conceptual blocker, **P1** required for a credible GB-BESS v0.1 under the revised Definition of Done, **P2** desirable after v0.1, **P3** future environment expansion.

### P0 — done in this pass (documentation only)
- Golden Verification Case / Atomic Benchmark Probe reclassification of the 20 existing scenarios — `docs/suites/gb-bess/SCENARIO_CATALOGUE.md`.
- Environment-vs-Benchmark distinction made explicit — `docs/architecture/ARCHITECTURE.md`.
- North-star mission, capability model, and stress-dimension model documented — `docs/benchmark/RELIABILITY_BOUNDARY_MODEL.md`, `CAPABILITY_TAXONOMY.md`, `STRESS_DIMENSIONS.md`, `TASK_MODEL.md`.

### P1 items 1-2 — done 2026-09-09 (first implementation pass following the realignment above)
Unlike the documentation-only pass above, this is real, tested code: `primary_capability` tagging on every evaluator (flowing through `EvaluationResult` into every Decision Record, not left as documentation-only metadata) and `primary_capability`/`complexity_rung`/`u_classes`/`autonomy_burden` tagging on every `ScenarioTemplate` and `EpisodeSpec`. See `docs/benchmark/CAPABILITY_TAXONOMY.md`'s "Tagging rule" and `docs/benchmark/STRESS_DIMENSIONS.md` for the assignments and rationale, `tests/unit/test_capability_tags.py` for the regression coverage, and `CHANGELOG.md` for the full change list. 111/111 tests pass (105 unchanged + 6 new). No `evaluate()` body, `build` function, or `check_*` function was modified — exactly as items 1 and 2 below originally scoped.

### P1 item 3 — done 2026-09-09 (second implementation pass)
`Scenario` gained an optional `task_family_tags` field (`gridactionbench/core/scenario.py`, `TaskFamilyTags`), populated post-hoc by `generate()` and `run_episode()` — never inside a `build`/`build_step` function — and carried through to `DecisionRecord`. `gridactionbench/reporting/report.py`'s `Report` gained `by_capability` (every existing dimension sliced by `primary_capability`, needing no propagation since evaluators already carry this tag) and `ucv_by_u_class`/`ucv_by_complexity_rung`/`ucv_by_autonomy_burden` (mirroring the pre-existing `ucv_by_constraint_class` pattern), both rendered in `render_text()`. The 20 hand-authored v0.1 scenarios have `task_family_tags=None` and correctly contribute nothing to the three stress-dimension breakdowns even when they produce a UCV — verified by `tests/unit/test_report.py`. 118/118 tests pass (111 unchanged + 7 new).

### P1 item 4 — done 2026-09-09 (third implementation pass)
`gridactionbench/core/trajectory_record.py` adds `TrajectoryRecord` (versioned, pydantic, `extra="forbid"`) carrying every field `docs/benchmark/TASK_MODEL.md`'s "Trajectory records" names — run_id, task_mode, task_family, instance_id, agent/model metadata, `random_seed`, `initial_state_hash` (sha256 of the first step's world state), the ordered `DecisionRecord`s themselves, `termination_reason` (`"steps_exhausted"` — the only value possible today, since `run_episode()` has no early-termination path), `terminal_state`, `any_ucv`/`ucv_count`, and `mean_economic_decision_quality` (the effectiveness-side aggregate). `build_trajectory_record_from_episode()` builds one from an already-computed `EpisodeResult` — `run_episode()` and every `check_*()` function are unchanged. `TrajectoryJsonlWriter` mirrors `DecisionRecord`'s own `JsonlWriter`. Wired into `gridactionbench run-episode --output <path>`. 126/126 tests pass (118 unchanged + 8 new in `tests/unit/test_trajectory_record.py`).

### P1 item 7 — done 2026-09-09 (fourth pass — analysis, not new code)
`docs/benchmark/CROSS_MODE_COMPARISON.md`, produced by `scripts/cross_mode_comparison.py` (read-only against existing scenarios/episodes; no evaluator, scenario, or schema change). Answer: atomic performance does **not** reliably predict operational performance — verified concretely, not merely argued, for `prompt-injection-victim` (its one real defect is never exercised by any of the 6 episodes at the time this pass ran) and `ignore-network` (a full rank inversion against other seeded-failure agents, most likely because only one episode ever constrains network headroom). Also surfaces a genuine methodological finding for the *benchmark itself*: with only 6 episodes each varying essentially one condition, an agent's Operational UCV rate depends heavily on whether the episodes that happen to exist touch that agent's specific defect — concrete supporting evidence for why the ADAPT-coverage gap (item 5, below) and the Sequential-task-mode gap matter, not just a restatement that they do.

### P1 item 5 — partially done 2026-09-09 (fifth pass — new schema field + new Task Family + new agent)
`market.price_forecast_gbp_mwh` (`gridactionbench/schemas/observation.py`, `MarketState`; schema_version bumped 1.0.0 → 1.1.0, additive/MINOR per `docs/benchmark/VERSIONING.md`) and `GB-BESS-EP-007` (`gridactionbench/scenarios/gb_bess/episodes.py`), the first Task Family closing U1 (forecast uncertainty, `docs/benchmark/STRESS_DIMENSIONS.md`) and the fourth episode (of seven) tagged ADAPT. Bidirectionally verified per this project's existing episode-verification discipline: `RuleBasedAgent` never triggers `check_ep007`; the new `TrustForecastOverActualAgent` seeded-failure agent (`baselines/seeded_failures/trust_forecast_over_actual.py`) — which keys off the forecast instead of the actual, real-time price — reliably does. Deliberately **not** added to `tests/golden/test_seeded_failure_agents.py`'s 20-scenario sweep: its defect has no surface to manifest on any scenario that predates the forecast field, which is every one of the 20 hand-authored scenarios. This closes only the forecast-was-wrong half of the original ADAPT item — tool failure and physical-deviation-from-expectation remain open, tracked below. This pass's addition happens *after* item 7's cross-mode comparison above, which was run against the 6-episode suite that existed before `GB-BESS-EP-007` — that document is a dated snapshot, not retroactively updated. 127/127 tests pass (126 unchanged + 1 new golden episode test).

### P1 item 6 — generator code done 2026-09-09 (sixth pass); repository creation explicitly out of scope
`gridactionbench/holdouts/` (`private_seed.py`, `acceptance.py`, `generate.py`) plus `gridactionbench generate-holdouts` (CLI). `resolve_private_seed()` checks `$GRIDACTIONBENCH_PRIVATE_SEED` then `fixtures/private_dev_only/private_seed.txt` (both already git-ignored per `docs/benchmark/PUBLIC_PRIVATE_POLICY.md`) and raises with setup instructions rather than ever defaulting to the public generator's own seed. `check_acceptance()` implements the policy's three criteria: (1) the reference agent (`RuleBasedAgent`) produces a scoreable, non-degenerate outcome; (2) the instance is internally consistent — a compliant reference agent is never forced into a HARD-constraint-invalid action; (3) a diagnostic (non-rejecting) sensitivity check — does a small price perturbation flip the reference agent's action type. All 20 hand-authored scenarios pass acceptance (a real regression check, `tests/unit/test_holdouts.py`). Confirmed the output directory is genuinely git-ignored (`git check-ignore`) as its own test, not just an assumption. **Explicitly not done, and not this pass's scope**: an actual private seed is not set anywhere in this repository; the separate `gridactionbench-evaluation-private` repository named in the policy document does not exist; no "GridActionBench Verified" result is possible yet. 139/139 tests pass (127 unchanged + 12 new).

### P1 — required for a credible GB-BESS v0.1 under the revised Definition of Done
1. ~~Tag all 18 existing evaluators with `primary_capability` (`docs/benchmark/CAPABILITY_TAXONOMY.md`).~~ **Done — see above.**
2. ~~Tag all existing `ScenarioTemplate`/`EpisodeSpec` Task Families with C/U/H stress-dimension metadata (`docs/benchmark/STRESS_DIMENSIONS.md`) — additive dataclass fields, no change to existing `build`/`check` logic.~~ **Done — see above.**
3. ~~Extend the reporting layer to slice reliability results by the new tags now that (1) and (2) exist.~~ **Done — see above (single-run slicing; cross-run/agent-architecture comparison is separate, unscoped work).**
4. ~~Design and implement `TrajectoryRecord` as an additive schema wrapping ordered `DecisionRecord`s.~~ **Done — see above.**
5. ~~Expand ADAPT-capability coverage — at minimum one Task Family testing a forecast that turns out wrong (new U1 representation).~~ **Partially done — see above.** Tool failure (U5) and physical-deviation-from-expectation remain open, coupled to the `AgentAdapter` interface gap (item below in P2/P3).
6. ~~Build the public/private holdout generator infrastructure.~~ **Generator code done — see below.** The separate private repository and an actual configured private seed remain not started — this item's "generator code" half only.
7. ~~Produce a documented cross-mode comparison (same agent, Atomic vs. Operational).~~ **Done — see above.**

### P2 item 2 — done 2026-09-09 (ninth pass — new episode + new agent)
Before building anything, checked whether an optimiser could show genuine advantage over `RuleBasedAgent` on *existing* content — it can't: `GB-BESS-EP-001`/`EP-002` have constant price throughout, and under constant price, greedy discharge-to-the-floor is *provably* revenue-optimal (timing can't beat it). Built the prerequisite first: `GB-BESS-EP-008` — a genuine multi-step timing tradeoff (a modest price now, a much higher one later in the same episode, with limited battery capacity forcing a real choice) — verified by hand against the actual `SimpleBessSimulator` before writing any episode code: greedy nets 380 GBP, holding for the peak nets 760 GBP, exactly double. Reused `MKT-PREFERRED-ACTION-001`/`preferred_actions` (previous pass) rather than a new evaluator. `MpcLookaheadAgent` (`baselines/mpc_lookahead/agent.py`, `agent_type="optimisation"`, the 4th reference-quality agent) mirrors `RuleBasedAgent` exactly except for one inserted lookahead branch using `market.price_forecast_gbp_mwh`; verified to behave identically to `RuleBasedAgent` everywhere else in the suite (20 hand-authored + 300 generated + `EP-001`-`EP-007`), differing only on `EP-008`, by design. One deliberate, documented exception to the pre-existing "`RuleBasedAgent` never triggers any episode's `failure_signature`" invariant — `RuleBasedAgent`'s lack of economic sophistication was already disclaimed (`docs/project/ASSUMPTIONS.md` A-12); `EP-008` is the first episode to actually demonstrate it. Also surfaced a real taxonomy gap (`docs/project/ASSUMPTIONS.md` A-18): no U-class names "full-information multi-step planning." 152/152 tests pass (148 unchanged + 4 new).

### P2 item 4 — done 2026-09-09 (eighth pass — new evaluator, via a pre-specified-but-unimplemented field)
A naive "did the agent make good money" evaluator would have violated `docs/suites/gb-bess/EVALUATION_SPEC.md`'s own explicit rule that `OBJECTIVE`-class evaluators do not exist ("objectives... never as an evaluator with a pass/fail verdict"). Resolution: `docs/benchmark/SPECIFICATION.md` §4 and `docs/architecture/DATA_MODEL.md` have both named a `preferred_actions` field on every scenario since Phase 0, never implemented in code or checked by any evaluator. Checking compliance with it is a scenario-*declared*-fact check (like `temporary_limits`), not a computed economic judgment — `gridactionbench/core/scenario.py` gained the field; `MKT-PREFERRED-ACTION-001` (`gridactionbench/evaluators/gb_bess/mkt.py`, `constraint_class: None`, `ucv_eligible: False`) checks it. The two MKT generator templates (`MKT-NEUTRAL`/`MKT-VOLATILITY`) now declare `preferred_actions` by price sign only — deliberately matching `RuleBasedAgent`'s own policy exactly, verified directly: `RuleBasedAgent` passes all 40 generated MKT instances, `AlwaysIdleAgent` fails all 40 (real discriminative power, not a check that never fires), and `Unrecognised Critical Violations` is unaffected by the new dimension in a full run (not UCV-eligible, confirmed against real output, not just unit tests). `report.py`'s `FAMILY_BY_EVAL_PREFIX` gained an "MKT" entry — MKT scenarios previously produced no dimension in any report at all. `EVALUATOR_SET_VERSION` bumped `0.2.0` → `0.3.0` (18 → 19 evaluators). 148/148 tests pass (141 unchanged + 7 new).

### P2 item 1 — done 2026-09-09 (seventh pass — reclassification, not new code)
`GB-BESS-EP-001`/`EP-002`'s `build_step` functions were found, on direct inspection, to have no per-step condition change at all — market/network/policy are identical every step, only SOC threads forward — which is exactly `docs/benchmark/TASK_MODEL.md`'s definition of Sequential, not Operational. The original claim that no GB-BESS task family occupied the Sequential rung had never actually been checked against each episode's own code. Both episodes are now tagged `task_mode="Sequential"`, `autonomy_burden="medium"` (a new H-proxy value, between Atomic's `"low"` and Operational's `"high"`); `EP-003`-`EP-007` (which do genuinely vary a condition) are now explicitly tagged `task_mode="Operational"`. `EpisodeSpec`/`TaskFamilyTags` gained a `task_mode` field; no `build_step` or `check_*` function changed, and EP-001/EP-002's actual CLI output is byte-identical before and after (verified). This closes the gap by finding an existing match, not by building new content — recorded honestly as a reclassification, not a new Task Family. 141/141 tests pass (139 unchanged + 2 new).

### P2 — desirable after v0.1
1. ~~A Sequential task mode implementation.~~ **Done — see above (via reclassification).**
2. ~~An optimisation/MPC baseline agent.~~ **Done — see above.**
3. `instance × k` repeated-trial execution and distributional reporting (needed before any stochastic/LLM agent is evaluated, `docs/project/ASSUMPTIONS.md` A-16).
4. ~~A dedicated MKT evaluator.~~ **Done — see above.**
5. U5 (tool/source failure) representation — coupled to the `AgentAdapter` interface gap below.

### P3 — future environment expansion (named, not committed to a timeline)
1. GB-DER environment (PV + BESS + load, C1/C2, `docs/benchmark/STRESS_DIMENSIONS.md`) — the next named environment after GB-BESS; not started, not scheduled.
2. `AgentAdapter` interface revision to express tool selection / multiple information-source queries — revisit only once a scenario genuinely needs it, per `docs/research/BENCHMARK_DESIGN_REVIEW.md`'s original Phase 0 finding.
3. Portfolio/network/multi-agent environments (C3+) — unscoped, named only as a future direction in `docs/benchmark/STRESS_DIMENSIONS.md`.
4. Resolution of the open UCV-terminology question (`docs/project/ASSUMPTIONS.md` A-15) — review-gated, not a code task until a decision is made.

---

# Implementation Backlog — Phase 1 Technical Spike (original, unchanged)

**Status:** Phase 1 complete (Gate 1 satisfied — see acceptance criteria below, all checked). Ordered for the technical spike (Phase 1, master brief §68), with dependencies, acceptance criteria, and explicitly deferred work. Original Phase 0 ordering preserved below with completion status; see `CHANGELOG.md` for the full Phase 1 change list.

## Ordering and dependencies (all complete except item 15, deferred as originally planned)

```text
1. [DONE] Project scaffolding (pyproject.toml, pytest config) — gridactionbench/pyproject.toml
   -> no dependencies

2. [DONE] EnergyObservationV1 + AgentActionV1 pydantic schemas — gridactionbench/schemas/
   -> depends on (1)

3. [DONE] Scenario file schema + loader (YAML -> validated in-memory Scenario) — gridactionbench/core/scenario.py
   -> depends on (1); informs but does not block (2)

4. [DONE] SimpleBessSimulator (step, validate_action) — gridactionbench/simulators/simple_bess.py
   -> depends on (1)

5. [DONE] Action Validator (hard-constraint pre-check) — gridactionbench/core/validator.py
   -> depends on (2), (4)

6. [DONE] Evaluator interface + first 6 evaluators (PHY family, all 6) — gridactionbench/evaluators/base.py, gb_bess/phy.py
   -> depends on (2), (4)

7. [DONE] AgentAdapter interface — gridactionbench/agents/base.py; AlwaysIdleAgent + AlwaysEscalateAgent
   — baselines/always_idle/agent.py, baselines/always_escalate/agent.py (moved from gridactionbench/agents/
   during a Phase 1.5 quality pass to match ADR-002's documented package architecture — see CHANGELOG.md)
   -> depends on (2)

8. [DONE] RuleBasedAgent (transparent deterministic controller) — baselines/rule_based/agent.py
   -> depends on (2), (3), (6)

9. [DONE] Runner (single-step pipeline) — gridactionbench/runners/single_step.py, core/engine.py
   -> depends on (2)-(8)

10. [DONE] Decision Record schema + JSONL writer — gridactionbench/core/decision_record.py
    -> depends on (9)

11. [DONE] Remaining evaluators (NET x2, OPS x4, DATA x4, ADV x1, HUM x1 = 12 more, total 18) — gridactionbench/evaluators/gb_bess/{net,ops,data,adv,hum}.py
    -> depends on (6)'s pattern

12. [DONE] Back-fill the 20 scenarios as real scenario files — suites/gb_bess/v0_1/scenarios/*.yaml, generated by scripts/backfill_scenarios.py
    -> depends on (3), (11)

13. [DONE] Golden tests (10 distinct scenarios, including the master brief's 3 explicit worked examples) — tests/golden/test_golden_scenarios.py
    -> depends on (9), (12)

14. [DONE] Minimal CLI — gridactionbench/cli.py (`gridactionbench run`, `gridactionbench list-scenarios`)
    -> depends on (9), (10)

15. [DEFERRED, as originally planned] LLMStructuredAgent interface + provider adapter — not built; does not block Gate 1
    -> depends on (2), (7)
```

**Unplanned but discovered during implementation** (recorded per the project's research-integrity norms — see `CHANGELOG.md`): running `AlwaysEscalateAgent`/`RuleBasedAgent` end-to-end surfaced a real logic bug in the DATA evaluators' applicability check (fixed — see `gridactionbench/evaluators/gb_bess/data.py` docstring) and a documentation error in `GB-BESS-HUM-019`'s `relevant_evaluators` list (fixed in `SCENARIO_CATALOGUE.md`). Both are the kind of finding master brief §69's "run reference agents, confirm expected behaviour" instruction exists to catch — the pipeline caught its own bugs on first real use, which is itself Gate 1 evidence the architecture works as intended.

## Phase 1 / Gate 1 acceptance criteria (master brief §69) — all satisfied

- [x] Deterministic simulator: same `(pre_state, action, seed)` always produces the same `post_state` — `tests/unit/test_simulator.py::test_deterministic_reproducibility` and the timestep-linearity/energy-conservation invariant tests.
- [x] 10 golden scenarios pass with documented expected results — `tests/golden/test_golden_scenarios.py` covers `GB-BESS-{PHY-001,PHY-003,NET-007,NET-009,OPS-011,OPS-013,DATA-014,DATA-016,HUM-020,ADV-018}`, including the master brief's own three worked examples (§50) verbatim.
- [x] Correct evaluator results — `tests/unit/test_evaluators.py` exercises pass/warning/fail/not_applicable branches across PHY/NET/OPS/DATA/HUM/ADV.
- [x] Oracle/Observation separation demonstrably implemented in code — `Scenario.oracle` vs. `Scenario.build_observation()` (`gridactionbench/core/scenario.py`); DATA-family scenarios' `observation_overrides` make the Observation actively differ from the Oracle, not merely a subset of it.
- [x] Complete Decision Records produced for every run — `gridactionbench/core/decision_record.py`, verified end-to-end by `tests/integration/test_pipeline.py`.
- [x] Deterministic reproducibility — `tests/reproducibility/test_determinism.py`.
- [x] No physical integration — confirmed: no dependency, schema field, or interface method in `gridactionbench/` addresses a real-world endpoint (consistent with `docs/architecture/SECURITY.md`).

**57/57 tests pass** (`python -m pytest`). Calibration evidence (informal preview of Phase 4, not a substitute for it): `AlwaysIdleAgent` produces 6 UCVs across the 20 scenarios; `AlwaysEscalateAgent` produces 0 UCVs but only 85.7% escalation appropriateness (correctly penalized on `GB-BESS-HUM-020`'s unnecessary-escalation check, satisfying master brief §22's "must not score perfectly" requirement); `RuleBasedAgent` produces 0 UCVs and 100% on every populated dimension.

If any of the above had not been satisfied, master brief §69 would have required stopping expansion and fixing the benchmark core before proceeding to Phase 2 — that did not happen; the core held up under first real end-to-end execution (modulo the one evaluator bug found and fixed, above).

## Explicitly deferred past Phase 1 (not backlog gaps — intentional scope boundaries)

- ~~Parameterised scenario generation~~ — **started**: `gridactionbench/scenarios/generator.py`, 20 templates / 300 generated instances, see `docs/suites/gb-bess/SCENARIO_TEMPLATES.md` for genuine progress and the honest remaining gap to ≥100 templates / ≥1,000 executions.
- Real GB data integration (Phase 5) — pending Elexon BMRS licence confirmation (`docs/data/DATA_SOURCES.md`).
- ~~Seeded failure agents~~ — **done ahead of schedule** (all 7: `AlwaysChargeAgent`, `IgnoreNetworkAgent`, `IgnoreMinimumSOCAgent`, `RevenueFirstConstraintIgnoringAgent`, `TrustAllTelemetryAgent`, `NeverEscalateAgent`, `PromptInjectionVictimAgent` — `baselines/seeded_failures/`), each verified against its documented expected failure mode in `tests/golden/test_seeded_failure_agents.py`. Results: `docs/benchmark/CALIBRATION_RESULTS.md`.
- ~~Episode runner implementation~~ — **done**: `gridactionbench/core/episode.py` (`run_episode`, threading SOC across steps per `ADR-016`) and all 6 episodes (`gridactionbench/scenarios/gb_bess/episodes.py`), each verified against a compliant and a matched-defective agent (`tests/golden/test_episodes.py`). Found and fixed a real bug in the process: the first version advanced the world state using a hard-constraint-invalid action's hypothetical outcome, letting a defective agent drive SOC out of its valid range.
- Counterfactual evaluation implementation (architecture designed per `ADR-017`; not required for Gate 1).
- Private evaluation infrastructure / holdout generators (Phase 3+, separate repository, not started).
- A `DATA-MISSING-NETWORK-HEADROOM-001`-equivalent evaluator (only `DATA-MISSING-SOC-001` exists in v0.1) — gap discovered while implementing `GB-BESS-HUM-019`, see that scenario's corrected `relevant_evaluators` note in `SCENARIO_CATALOGUE.md`.
- A pinned dependency lockfile (`ADR-001`'s stated requirement) — `pyproject.toml` declares version ranges; a fully pinned lock (e.g. via `pip-compile` or `uv lock`) was not generated in Phase 1 and should be added before any officially reproducible external run is claimed.
- Episode runner implementation, counterfactual evaluation implementation, seeded failure agents beyond the calibration set, parameterised scenario generation, real GB data integration — all as previously listed, still deferred past Phase 1.

## Non-goals for the spike (recap of master brief §68)

No frontend. No LLM comparison (calibration-only agents suffice for Gate 1). No public/private holdout infrastructure. No episode execution.
