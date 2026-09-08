# Implementation Backlog — Phase 1 Technical Spike

**Status:** Draft — Phase 0 deliverable (master brief §88, Step 11). Ordered for the technical spike (Phase 1, master brief §68), with dependencies, acceptance criteria, and explicitly deferred work.

## Ordering and dependencies

```text
1. Project scaffolding (pyproject.toml, pinned lockfile, pytest config)
   -> no dependencies

2. EnergyObservationV1 + AgentActionV1 pydantic schemas
   -> depends on (1)

3. Scenario file schema + loader (YAML -> validated in-memory Scenario)
   -> depends on (1); informs but does not block (2)

4. SimpleBessSimulator (step, validate_action)
   -> depends on (1)

5. Action Validator (hard-constraint pre-check, rejects before simulator)
   -> depends on (2), (4)

6. Evaluator interface + first 6 evaluators (PHY family, all 6)
   -> depends on (2), (4)

7. AgentAdapter interface + AlwaysIdleAgent + AlwaysEscalateAgent
   -> depends on (2)

8. RuleBasedAgent (transparent deterministic controller)
   -> depends on (2), (3), (6)

9. Runner (single-step pipeline: Scenario -> Observation -> Agent -> Action -> Validator -> Simulator -> Evaluation -> Decision Record)
   -> depends on (2)-(8)

10. Decision Record schema + JSONL writer
    -> depends on (9)

11. Remaining evaluators for the initial 20 scenarios (NET x2, OPS x4, DATA x4, ADV x1, HUM x1 = 12 more, total 18)
    -> depends on (6)'s pattern; parallelizable once (6) establishes the Evaluator interface concretely

12. Back-fill the 20 scenarios from SCENARIO_CATALOGUE.md as real scenario files under suites/gb_bess/v0_1/
    -> depends on (3), (11)

13. Golden tests for all 20 scenarios
    -> depends on (9), (12)

14. Minimal CLI (run a scenario set against an agent, print a per-dimension report per SCORING.md)
    -> depends on (9), (10)

15. LLMStructuredAgent interface + at least one provider adapter (Extended, optional for spike completion)
    -> depends on (2), (7); can slip past Phase 1 if needed without blocking Gate 1
```

## Phase 1 / Gate 1 acceptance criteria (master brief §69)

- [ ] Deterministic simulator: same `(pre_state, action, seed)` always produces the same `post_state`, verified by a property test.
- [ ] 10 golden scenarios (subset of the 20 in `SCENARIO_CATALOGUE.md`, prioritizing at least one per family) pass with documented expected results.
- [ ] Correct evaluator results: each implemented evaluator's pass/warning/failure boundary matches its `EVALUATION_SPEC.md` specification exactly, verified by unit tests.
- [ ] Oracle/Observation separation demonstrably implemented (a DATA-family scenario's Observation differs from its Oracle in code, not just in the YAML spec).
- [ ] Complete Decision Records produced for every run, matching the schema in `docs/benchmark/SPECIFICATION.md` §7.
- [ ] Deterministic reproducibility: re-running the same configuration twice produces byte-identical (or documented-tolerance-equivalent) Decision Records.
- [ ] No physical integration: confirmed by code review against `docs/architecture/SECURITY.md`.

If any of the above is not satisfied, master brief §69 requires stopping expansion and fixing the benchmark core before proceeding to Phase 2 — this backlog does not authorize proceeding past Gate 1 with a known-unreliable core.

## Explicitly deferred past Phase 1 (not backlog gaps — intentional scope boundaries)

- Parameterised scenario generation (Phase 3).
- Real GB data integration (Phase 5) — pending Elexon BMRS licence confirmation (`docs/data/DATA_SOURCES.md`).
- Seeded failure agents beyond what's needed for Phase 4 calibration design (full set: `AlwaysChargeAgent`, `IgnoreNetworkAgent`, `IgnoreMinimumSOCAgent`, `RevenueFirstConstraintIgnoringAgent`, `TrustAllTelemetryAgent`, `NeverEscalateAgent`, `PromptInjectionVictimAgent` — implement in Phase 2/4, not Phase 1).
- Episode runner implementation (architecture is designed per `ADR-016`, but the 6 designed episodes are not implemented in Phase 1's spike scope).
- Counterfactual evaluation implementation (architecture designed per `ADR-017`; not required for Gate 1).
- Private evaluation infrastructure / holdout generators (Phase 3+, separate repository, not started).
- `docs/research/BENCHMARK_DESIGN_REVIEW.md` and `docs/research/EXPERT_REVIEW_CHECKLIST.md` — Phase 0 documentation gaps, should be completed before or during Phase 1, not silently dropped.
- Root community/governance files not yet written as of this backlog's creation: `README.md`, `LICENSE`, `CITATION.cff`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `GOVERNANCE.md`, root `SECURITY.md`, `CHANGELOG.md` — tracked here, to be completed as part of closing out Phase 0.

## Non-goals for the spike (recap of master brief §68)

No frontend. No LLM comparison (calibration-only agents suffice for Gate 1). No public/private holdout infrastructure. No episode execution.
