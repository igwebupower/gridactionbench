# GridActionBench

**An open benchmark for evaluating the reliability boundaries of autonomous AI agents acting in dynamic energy systems.**

> Do not just evaluate what an AI says. Evaluate what happens if you let it act.

GridActionBench measures how agents **perceive, decide, act, adapt, and escalate** as system complexity, operational uncertainty, and autonomy burden increase (`docs/benchmark/RELIABILITY_BOUNDARY_MODEL.md`). The first environment, **GB-BESS v0.1**, evaluates a simulated grid-connected Battery Energy Storage System in a Great Britain electricity-system context — one deliberately narrow rung of a larger planned complexity progression, not the project's permanent scope.

It's an open-source research project — not a SaaS product, certification system, or government benchmark, and runs independently of any proprietary platform or DESNZ/Ofgem/NESO endorsement. See `docs/research/PRIOR_ART.md` for related work.

## Status

Phase 1-3 implementation in progress. Core pipeline implemented and running: schemas, simulator, 20 evaluators, 4 reference agents, 8 seeded-failure agents, a parameterised generator (20 templates, 300 instances), 8 episodes, Decision/Trajectory Record writers, reporting, and a CLI — **152 passing tests**. All current agents are deterministic built-in baselines; no LLM has yet been evaluated against GB-BESS. See `docs/project/DEFINITION_OF_DONE.md` for release-gate status and `docs/benchmark/CALIBRATION_RESULTS.md` for current output.

```bash
pip install -e .
gridactionbench run suites/gb_bess/v0_1/scenarios --agent rule-based
```

## Physical-system scope

GB-BESS v0.1 is simulation-only — it cannot interact with physical energy assets. See `SECURITY.md`.

## Core idea

```text
Scenario -> Oracle -> Observation -> Agent -> Action -> Validator -> Simulator
   -> Evaluation -> Decision Record -> Report
```

Ground truth (Oracle) and what the agent observes (Observation) are kept strictly separate, so the benchmark tests behaviour under missing, stale, contradictory, or adversarial information — not just correctness given perfect information. Results are reported as independent dimensions (constraint adherence, data-quality handling, adversarial resilience, escalation quality, economic decision quality, UCV counts) — never a single opaque score. See `docs/benchmark/SPECIFICATION.md` and `docs/benchmark/SCORING.md`.

This is the **Atomic** case of a broader Task/Trial/Trajectory model spanning Atomic → Sequential → Operational task modes, across five capabilities (**Perceive, Decide, Act, Adapt, Escalate**) and three stress dimensions (**System Complexity, Operational Uncertainty, Autonomy Burden**). See `docs/benchmark/TASK_MODEL.md`.

## Repository structure

```text
docs/            specification, research, architecture, project, and testing documentation
gridactionbench/ core library: schemas, simulator, evaluators, runner, reporting, CLI
baselines/       reference agents and 8 seeded-failure agents
suites/gb_bess/  GB-BESS scenario data — all 20 initial scenarios
data/            synthetic data and manifests
tests/           unit, integration, golden, reproducibility tests
scripts/         one-off utilities
```

## Key documents

| Document | What it covers |
|---|---|
| `docs/benchmark/RELIABILITY_BOUNDARY_MODEL.md` | The central research question |
| `docs/benchmark/TASK_MODEL.md` | Task / Trial / Trajectory ontology |
| `docs/benchmark/CAPABILITY_TAXONOMY.md` | Perceive / Decide / Act / Adapt / Escalate |
| `docs/benchmark/STRESS_DIMENSIONS.md` | Complexity / Uncertainty / Autonomy Burden |
| `docs/benchmark/VALIDATION_FRAMEWORK.md` | Validity, sensitivity, discrimination, stability |
| `docs/benchmark/BENCHMARK_CARD.md` | Purpose, intended use, limitations |
| `docs/benchmark/SPECIFICATION.md` | Core architecture and methodology |
| `docs/suites/gb-bess/SPECIFICATION.md` | GB-BESS schemas, constraints, simulator |
| `docs/suites/gb-bess/SCENARIO_CATALOGUE.md` | The 20 scenarios and 8 episode designs |
| `docs/suites/gb-bess/EVALUATION_SPEC.md` | The evaluator catalogue |
| `docs/benchmark/CALIBRATION_RESULTS.md` | Agent output against the 20 scenarios |
| `docs/benchmark/CROSS_MODE_COMPARISON.md` | Atomic vs. Operational performance |
| `docs/benchmark/PUBLIC_PRIVATE_POLICY.md` | Public/private split and holdout generation |
| `docs/suites/gb-bess/SCENARIO_TEMPLATES.md` | The parameterised scenario generator |
| `docs/project/DEFINITION_OF_DONE.md` | The five evidence-based release gates |
| `docs/research/PRIOR_ART.md` | Related work and differentiation |
| `docs/architecture/adr/` | Architecture decision records |
| `GOVERNANCE.md`, `CONTRIBUTING.md` | How to participate |

## License

Code: Apache License 2.0 (`LICENSE`). Data: see `DATA_LICENSES.md` — GB-BESS v0.1 uses synthetic data only.

## Citation

See `CITATION.cff`.
