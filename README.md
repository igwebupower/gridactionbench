# GridActionBench

**An open benchmark for evaluating AI actions in energy systems.**

> Do not just evaluate what an AI says. Evaluate what happens if you let it act.

GridActionBench is a transparent, reproducible experimental framework for discovering how AI agents — and non-AI controllers — behave when making operational decisions that have real consequences within a simulated energy system. It is an open-source research project, not a SaaS product, not a certification system, and not an official government benchmark.

The first benchmark suite is **GB-BESS v0.1**, evaluating operational decisions for a simulated grid-connected Battery Energy Storage System in a Great Britain electricity-system context.

## Status

**Phase 1 complete, Gate 1 passed.** The core pipeline is implemented and running: schemas, `SimpleBessSimulator`, all 18 specified evaluators, 3 reference agents, 7 seeded-failure agents, a JSONL Decision Record writer, per-dimension reporting, and a CLI — 74 passing tests, all 20 initial scenarios executable end-to-end. See `docs/project/BACKLOG.md` for the full completion record, `docs/benchmark/CALIBRATION_RESULTS.md` for real calibration output, and `docs/project/PROJECT_PLAN.md`/`docs/project/DEFINITION_OF_DONE.md` for what remains before v0.1 is complete (parameterised scenario generation, episode execution, LLM comparison, external review — all still ahead).

```bash
pip install -e .
gridactionbench run suites/gb_bess/v0_1/scenarios --agent rule-based
```

## Why this benchmark exists

Two questions are answered in full, with evidence, in `docs/project/PID.md` §2:

- **Why should GridActionBench exist if PowerAgentBench already exists?** — see `docs/project/PID.md` §2.1 and the full comparison in `docs/research/POWERAGENTBENCH_REVIEW.md`.
- **What specifically makes GB-BESS a Great Britain benchmark, not just a generic battery benchmark in GBP?** — see `docs/suites/gb-bess/GB_SPECIFICITY.md`.

## Core idea

```text
Scenario -> Oracle -> Observation -> Agent -> Action -> Validator -> Simulator
   -> Evaluation -> Decision Record -> Report
```

Ground truth (Oracle) and what the agent actually observes (Observation) are kept strictly separate, so the benchmark can rigorously test how agents behave under missing, stale, contradictory, or adversarial information — not just whether they can compute the right answer given perfect information. See `docs/benchmark/SPECIFICATION.md`.

The benchmark reports results as independent dimensions (physical constraint adherence, network constraint adherence, operational-policy adherence, data-quality handling, adversarial resilience, escalation quality, economic decision quality, and Unrecognised Critical Violation counts) — never as a single opaque score. See `docs/benchmark/SCORING.md`.

## Repository structure

```text
docs/           specification, research, architecture, project, and testing documentation
gridactionbench/ core library: schemas, simulator, evaluators, runner, reporting, CLI
baselines/       reference agents (always_idle, always_escalate, rule_based) and 7 seeded-failure agents
suites/gb_bess/  GB-BESS scenario data — all 20 initial scenarios, suites/gb_bess/v0_1/scenarios/*.yaml
data/            synthetic data and manifests
tests/           unit, integration, golden, reproducibility tests — 74 passing
scripts/         one-off utilities (e.g. the scenario-catalogue backfill script)
```

## Key documents

| Document | What it covers |
|---|---|
| `docs/benchmark/BENCHMARK_CARD.md` | Purpose, intended use, out-of-scope use, limitations |
| `docs/benchmark/SPECIFICATION.md` | Core architecture and methodology |
| `docs/suites/gb-bess/SPECIFICATION.md` | GB-BESS schemas, constraints, simulator |
| `docs/suites/gb-bess/SCENARIO_CATALOGUE.md` | The initial 20 scenarios and 6 episode designs |
| `docs/suites/gb-bess/EVALUATION_SPEC.md` | The evaluator catalogue |
| `docs/benchmark/CALIBRATION_RESULTS.md` | Real output from 10 agents (3 reference, 7 seeded-failure) against the 20 initial scenarios |
| `docs/research/PRIOR_ART.md`, `POWERAGENTBENCH_REVIEW.md` | Prior-art research and differentiation |
| `docs/architecture/adr/` | Architecture decision records |
| `GOVERNANCE.md`, `CONTRIBUTING.md` | How to participate |

## Relationship to other projects

GridActionBench runs entirely independently of Enprompta or any proprietary platform. It acknowledges PowerAgentBench as important prior art (see `docs/research/POWERAGENTBENCH_REVIEW.md`) without forking it. It does not claim DESNZ, Ofgem, NESO, or UK government endorsement. See `docs/project/PID.md` §3.

## License

Code: Apache License 2.0 (see `LICENSE`). Data: see `DATA_LICENSES.md` — GB-BESS v0.1 currently uses synthetic data only.

## Citation

See `CITATION.cff`.
