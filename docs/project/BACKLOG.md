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

### P1 — required for a credible GB-BESS v0.1 under the revised Definition of Done
1. ~~Tag all 18 existing evaluators with `primary_capability` (`docs/benchmark/CAPABILITY_TAXONOMY.md`).~~ **Done — see above.**
2. ~~Tag all existing `ScenarioTemplate`/`EpisodeSpec` Task Families with C/U/H stress-dimension metadata (`docs/benchmark/STRESS_DIMENSIONS.md`) — additive dataclass fields, no change to existing `build`/`check` logic.~~ **Done — see above.**
3. ~~Extend the reporting layer to slice reliability results by the new tags now that (1) and (2) exist.~~ **Done — see above (single-run slicing; cross-run/agent-architecture comparison is separate, unscoped work).**
4. ~~Design and implement `TrajectoryRecord` as an additive schema wrapping ordered `DecisionRecord`s.~~ **Done — see above.**
4. Design and implement `TrajectoryRecord` as an additive schema wrapping ordered `DecisionRecord`s (`docs/benchmark/TASK_MODEL.md`, "Trajectory records") — `EpisodeResult` already carries the needed data informally.
5. Expand ADAPT-capability coverage (`docs/benchmark/CAPABILITY_TAXONOMY.md`) — at minimum one Task Family testing a forecast that turns out wrong (new U1 representation, `docs/benchmark/STRESS_DIMENSIONS.md`).
6. Build the public/private holdout generator infrastructure (`docs/benchmark/PUBLIC_PRIVATE_POLICY.md`) — carried over from `docs/research/BENCHMARK_DESIGN_REVIEW.md`'s pre-existing higher-priority flag, unchanged by this pass.
7. Produce a documented cross-mode comparison (same agent, Atomic vs. Operational) — currently missing per `docs/project/GAP_ANALYSIS.md`'s research traceability matrix.

### P2 — desirable after v0.1
1. A Sequential task mode implementation (state-dependent, static conditions — the currently-missing middle rung, `docs/benchmark/TASK_MODEL.md`).
2. An optimisation/MPC baseline agent.
3. `instance × k` repeated-trial execution and distributional reporting (needed before any stochastic/LLM agent is evaluated, `docs/project/ASSUMPTIONS.md` A-16).
4. A dedicated MKT evaluator (carried over, unchanged, from `docs/suites/gb-bess/EVALUATION_SPEC.md`'s coverage note).
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
