# Task Model

**Status:** New — September 2026 strategic realignment. This document generalises `docs/benchmark/SPECIFICATION.md` §1-2's Scenario→Oracle→Observation→Agent→Action→Validator→Simulator→Evaluation→Decision Record→Report pipeline into the ontology below. It does not replace that pipeline or require any code change to introduce — it names concepts that already exist in `gridactionbench/` and identifies the one rung (Sequential) that does not yet have a dedicated implementation. See `docs/project/GAP_ANALYSIS.md` for what, if anything, should change in code as a result.

## Why this document exists

Before this pass, GridActionBench's documentation described one execution mode (Mode A, single-step) as "primary," with Mode B (episodes) as "a small validated subset." That framing made the single-decision case read as the benchmark's normal mode and episodes as a secondary extension. The actual architecture (`docs/architecture/adr/ADR-016-episode-architecture.md`) was never built that way — Mode B is "a thin loop over the existing Mode A pipeline," meaning Mode A was always the atomic special case of a more general repeated-decision structure, not a separate thing episodes were bolted onto. This document makes that relationship explicit and gives the general structure a name, so future work (a Sequential task mode, a GB-DER environment, portfolio-level tasks) has a place to attach without another rename.

## Ontology

| Term | Definition | GridActionBench today |
|---|---|---|
| **Task** | A benchmark problem or objective | "Evaluate whether an agent selects a valid, appropriate action for a GB-connected BESS under constraint X and uncertainty Y" |
| **Task Family** | A parameterised class of related benchmark problems | A `ScenarioTemplate` (`gridactionbench/scenarios/generator.py`) for Atomic tasks; an `EpisodeSpec` (`gridactionbench/core/episode.py`) for Operational tasks. Both are "documented parameter-range recipes," in the generator module's own words — the task-family concept was already implemented under a domain-specific name before this document existed |
| **Instance** | A concrete parameterisation of a task family | A `Scenario` object — either hand-authored (`suites/gb_bess/v0_1/scenarios/*.yaml`) or generated (`generate()`'s output) |
| **Trial** | One attempt by one agent at one instance | One call to `run_single_step()` (Atomic/Sequential) or one full `run_episode()` (Operational) |
| **Trajectory** | The complete sequence of observations, tool calls, actions, state transitions, errors, escalations, and intermediate decisions produced by a trial | For an Atomic trial: one `DecisionRecord`. For an Operational trial: the ordered list of per-step `DecisionRecord`s plus the episode-level state thread (`EpisodeResult.world_soc_after_step`) — see "Trajectory records," below |
| **Outcome** | The resulting terminal state and accumulated consequences | `EvaluationOutcome` (single-step) plus, for episodes, `EpisodeResult`'s aggregate properties (`any_ucv`, `ucv_count`) and the episode's own `failure_signature` check |
| **Grader / Evaluator** | A component that evaluates one property of the trajectory or outcome | The 18 evaluator classes in `gridactionbench/evaluators/gb_bess/`, each returning one `EvaluationResult` (`docs/suites/gb-bess/EVALUATION_SPEC.md`) |

These terms are used consistently from this point forward in new GridActionBench documentation. Existing documents that use "scenario," "run," or "episode" are not being renamed wholesale — those words remain accurate at the GB-BESS suite level and are cross-referenced to this ontology, not replaced by it (see "Terminology mapping," below). New documents (`docs/benchmark/RELIABILITY_BOUNDARY_MODEL.md`, `CAPABILITY_TAXONOMY.md`, `STRESS_DIMENSIONS.md`) use Task/Instance/Trial/Trajectory throughout.

## Task modes

GridActionBench recognises three task modes, distinguished by autonomy burden (`docs/benchmark/STRESS_DIMENSIONS.md`), not by a fixed step count:

### Atomic
One consequential decision. `docs/benchmark/SPECIFICATION.md` §2's "Mode A." Implemented today as the 20 hand-authored scenarios (`suites/gb_bess/v0_1/scenarios/`) and the 300-instance generated set (`gridactionbench/scenarios/generator.py`).

### Sequential
Multiple linked decisions with state dependence, but without the changing-conditions/adaptation/delayed-consequence properties that define Operational. **This is a real gap, not a renamed existing thing**: GB-BESS v0.1 has no task family that occupies this middle rung today — its only multi-step tasks (the seven episodes, below) all already involve changing conditions, degrading information, or a forecast turning out wrong, which places them in Operational, not Sequential. A pure Sequential task family (e.g., "dispatch across N steps to meet a fixed energy target, with no external condition changing, so the only thing being tested is whether earlier decisions leave later ones feasible") is tracked as an open implementation gap in `docs/project/GAP_ANALYSIS.md`, not fabricated here.

### Operational
A stateful episode involving repeated decisions, changing conditions, and potentially delayed consequences and/or escalation. `docs/benchmark/SPECIFICATION.md` §2's "Mode B." Implemented today as the seven `EpisodeSpec`s in `gridactionbench/scenarios/gb_bess/episodes.py` (`GB-BESS-EP-001` through `EP-007`), run via `gridactionbench/core/episode.py::run_episode()`. Every one of the seven already varies at least one condition mid-episode (network headroom dropping and recovering, telemetry degrading, a temporary restriction appearing and clearing, a day-ahead price forecast turning out wrong) or tests cross-step escalation discrimination — none is a "pure Sequential" task in the sense above.

The task-mode ladder is: **Atomic → Sequential → Operational**, of increasing autonomy burden (H, `docs/benchmark/STRESS_DIMENSIONS.md`). GB-BESS v0.1 currently instantiates the two ends of that ladder and not the middle rung — stated plainly here rather than left implicit.

## Reclassifying GB-BESS's existing single-step scenarios

Per the same principle that separates task modes by what they test, the existing 20 single-step scenarios (`docs/suites/gb-bess/SCENARIO_CATALOGUE.md`) are reclassified — not renamed, not modified — as **Golden Verification Case**, **Atomic Benchmark Probe**, or **Both**. See that document's own new "Golden Verification Case vs. Atomic Benchmark Probe" section for the per-scenario table; the definitions:

- **Golden Verification Case** — tests whether GridActionBench's own machinery (simulator state transition, evaluator classification, headroom-constraint arithmetic, boundary tolerance) behaves correctly. The system under test is the benchmark.
- **Atomic Benchmark Probe** — tests whether an agent identifies and handles a controlled operational condition correctly. The system under test is the agent.
- **Both** — the same fixture legitimately supports both purposes at once (this is the common case for GB-BESS's initial 20, and is not a design flaw — a scenario with an unambiguous expected result is valuable precisely because it lets one fixture serve both roles, as long as the report reading it states which claim it is making).

"Does the evaluator correctly detect invalid charging?" (a Golden Verification Case question, answered by `tests/golden/test_golden_scenarios.py`'s hard-coded expected results) and "Does the agent avoid invalid charging?" (an Atomic Benchmark Probe question, answered by an agent's per-scenario pass rate in a Run report) are different claims about different systems, even when asked of the identical scenario file. No document in this repository should present a Golden Verification Case's pass as if it were evidence about agent capability, or an Atomic Benchmark Probe result as if it were evidence the benchmark itself is bug-free.

## Trajectory records

`docs/benchmark/SPECIFICATION.md` §7's `DecisionRecord` remains the atomic unit of evidence — it is not being replaced. For Operational (and, once implemented, Sequential) trials, the **trajectory** is the ordered sequence of per-step `DecisionRecord`s already produced by `run_episode()` (`EpisodeResult.step_records`), plus the episode-level state thread and aggregate outcome fields already computed (`world_soc_after_step`, `any_ucv`, `ucv_count`) and the episode's `failure_signature` check. A dedicated `TrajectoryRecord` container type that formalises this grouping (run_id, task family, instance_id, seed, agent/model metadata, initial-world-state hash, ordered `DecisionRecord`s, termination reason, terminal state, aggregate reliability/effectiveness metrics) is an additive schema change, not a replacement of `DecisionRecord`.

**Built — 2026-09-09** (`docs/project/GAP_ANALYSIS.md` P1 item 4): `gridactionbench/core/trajectory_record.py`'s `TrajectoryRecord`, populated from an `EpisodeResult` by `build_trajectory_record_from_episode()` and serialised via `TrajectoryJsonlWriter` (`gridactionbench run-episode --output <path>`). `run_episode()` itself, and every episode's `check_*()` failure-signature function, are unchanged — exactly as this section originally scoped. `task_family` and `instance_id` are identical today (every `EpisodeSpec` is a single, unparameterised instance) — kept as separate fields against the day a Task Family produces more than one instance. `termination_reason` is always `"steps_exhausted"` today, since `run_episode()` has no early-termination path yet.

## Terminology mapping (for readers of existing documents)

| Existing term | Ontology equivalent |
|---|---|
| Scenario | Instance |
| Scenario family (PHY/NET/OPS/MKT/DATA/ADV/HUM) | A cross-cutting tag on Task Families and Instances, not itself a Task Family — a single family like PHY spans many task families (SOC-ceiling boundary, charge-rate-limit boundary, etc.) |
| `ScenarioTemplate` | Task Family (Atomic) |
| `EpisodeSpec` | Task Family (Operational) |
| Run (`docs/architecture/DOMAIN_MODEL.md`) | A set of Trials under one fixed configuration |
| Mode A / Mode B | Atomic / Operational (Sequential has no existing name because it has no existing implementation) |
