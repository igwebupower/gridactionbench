# GridActionBench

**An open benchmark for evaluating the reliability boundaries of autonomous AI agents in dynamic energy systems.**

> Do not just evaluate what an AI says. Evaluate what happens if you let it act.

GridActionBench measures how different agent architectures **perceive, decide, act, adapt, and escalate** as system complexity, operational uncertainty, and autonomy burden increase (`docs/benchmark/RELIABILITY_BOUNDARY_MODEL.md`). Initially grounded in the Great Britain electricity system, it combines executable energy environments, reproducible scenarios, consequential actions, and deterministic evaluation to identify where autonomous behaviour remains reliable and where it begins to fail. It is an open-source research project, not a SaaS product, not a certification system, and not an official government benchmark.

GridActionBench is a benchmark suite built on a reusable executable energy-agent evaluation environment/harness — the two are distinct (`docs/architecture/ARCHITECTURE.md`). The first environment is **GB-BESS v0.1**, evaluating operational decisions for a simulated grid-connected Battery Energy Storage System in a Great Britain electricity-system context — the first, deliberately narrow rung of a named future complexity progression (`docs/project/PID.md` §2.3), not the permanent scope of the project.

GridActionBench does not claim to be the first energy-agent benchmark, the first executable energy benchmark, or the first dynamic power-system AI benchmark — see `docs/research/DESIGN_EVIDENCE_BASE.md` for how prior research informs specific design choices without a novelty claim attached.

## Status

**Phase 1-3 implementation in progress; specification revised by the September 2026 strategic realignment.** The core pipeline is implemented and running: schemas, `SimpleBessSimulator`, all 18 specified evaluators, 3 reference agents, 7 seeded-failure agents, a parameterised scenario generator (20 templates, 300 instances), 6 validated episodes, a JSONL Decision Record writer, per-dimension reporting, and a CLI — **126 passing tests**, all 20 initial scenarios plus 6 episodes executable end-to-end. See `docs/project/DEFINITION_OF_DONE.md` for the current status against the five evidence-based release gates (Instrument Validity, Construct Validity, Operational Depth, GB Grounding, External Review — replacing the earlier raw scenario/execution-count targets), `docs/project/GAP_ANALYSIS.md` for the architecture gap analysis and research traceability matrix, and `docs/benchmark/CALIBRATION_RESULTS.md` for real calibration output.

```bash
pip install -e .
gridactionbench run suites/gb_bess/v0_1/scenarios --agent rule-based
```

## Why this benchmark exists

Two questions are answered in full, with evidence, in `docs/project/PID.md` §2:

- **What does this benchmark evaluate that isn't already well covered?** — see `docs/project/PID.md` §2.1 and the related-work survey in `docs/research/PRIOR_ART.md`.
- **What specifically makes GB-BESS a Great Britain benchmark, not just a generic battery benchmark in GBP?** — see `docs/suites/gb-bess/GB_SPECIFICITY.md`.

## Core idea

```text
Scenario -> Oracle -> Observation -> Agent -> Action -> Validator -> Simulator
   -> Evaluation -> Decision Record -> Report
```

Ground truth (Oracle) and what the agent actually observes (Observation) are kept strictly separate, so the benchmark can rigorously test how agents behave under missing, stale, contradictory, or adversarial information — not just whether they can compute the right answer given perfect information. See `docs/benchmark/SPECIFICATION.md`.

The benchmark reports results as independent dimensions (physical constraint adherence, network constraint adherence, operational-policy adherence, data-quality handling, adversarial resilience, escalation quality, economic decision quality, and Unrecognised Critical Violation counts) — never as a single opaque score. See `docs/benchmark/SCORING.md`.

This pipeline is the **Atomic** special case of a more general Task/Trial/Trajectory model (`docs/benchmark/TASK_MODEL.md`) spanning Atomic → Sequential → Operational task modes of increasing autonomy burden, evaluated across five capabilities — **Perceive, Decide, Act, Adapt, Escalate** (`docs/benchmark/CAPABILITY_TAXONOMY.md`) — and three stress dimensions — **System Complexity, Operational Uncertainty, Autonomy Burden** (`docs/benchmark/STRESS_DIMENSIONS.md`).

## Repository structure

```text
docs/           specification, research, architecture, project, and testing documentation
gridactionbench/ core library: schemas, simulator, evaluators, runner, reporting, CLI
baselines/       reference agents (always_idle, always_escalate, rule_based) and 7 seeded-failure agents
suites/gb_bess/  GB-BESS scenario data — all 20 initial scenarios, suites/gb_bess/v0_1/scenarios/*.yaml
data/            synthetic data and manifests
tests/           unit, integration, golden, reproducibility tests — 126 passing
scripts/         one-off utilities (e.g. the scenario-catalogue backfill script)
```

## Key documents

| Document | What it covers |
|---|---|
| `docs/benchmark/RELIABILITY_BOUNDARY_MODEL.md` | The central research object: R = f(agent architecture, complexity, uncertainty, autonomy burden) |
| `docs/benchmark/TASK_MODEL.md` | Task / Task Family / Instance / Trial / Trajectory / Outcome / Grader ontology |
| `docs/benchmark/CAPABILITY_TAXONOMY.md` | Perceive / Decide / Act / Adapt / Escalate — definitions and current coverage |
| `docs/benchmark/STRESS_DIMENSIONS.md` | System Complexity / Operational Uncertainty / Autonomy Burden |
| `docs/benchmark/VALIDATION_FRAMEWORK.md` | Instrument validity, construct validity, sensitivity, discrimination, stability, robustness |
| `docs/benchmark/BENCHMARK_CARD.md` | Purpose, intended use, out-of-scope use, limitations |
| `docs/benchmark/SPECIFICATION.md` | Core architecture and methodology |
| `docs/suites/gb-bess/SPECIFICATION.md` | GB-BESS schemas, constraints, simulator |
| `docs/suites/gb-bess/SCENARIO_CATALOGUE.md` | The initial 20 scenarios and 6 episode designs, plus Golden-Verification-Case-vs-Atomic-Benchmark-Probe classification |
| `docs/suites/gb-bess/EVALUATION_SPEC.md` | The evaluator catalogue |
| `docs/benchmark/CALIBRATION_RESULTS.md` | Real output from 10 agents (3 reference, 7 seeded-failure) against the 20 initial scenarios |
| `docs/suites/gb-bess/SCENARIO_TEMPLATES.md` | Parameterised scenario generator: 20 templates, 300 generated instances |
| `docs/project/DEFINITION_OF_DONE.md` | The five evidence-based release gates |
| `docs/project/GAP_ANALYSIS.md` | Architecture gap analysis and research traceability matrix |
| `docs/research/PRIOR_ART.md` | Prior-art research and differentiation |
| `docs/research/DESIGN_EVIDENCE_BASE.md` | Evidence → inference → design decision → assumption, for major design choices |
| `docs/architecture/adr/` | Architecture decision records |
| `GOVERNANCE.md`, `CONTRIBUTING.md` | How to participate |

## Relationship to other projects

GridActionBench runs entirely independently of any proprietary platform. It does not claim DESNZ, Ofgem, NESO, or UK government endorsement. See `docs/project/PID.md` §3.

## License

Code: Apache License 2.0 (see `LICENSE`). Data: see `DATA_LICENSES.md` — GB-BESS v0.1 currently uses synthetic data only.

## Citation

See `CITATION.cff`.
