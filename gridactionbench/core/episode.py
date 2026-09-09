"""Mode B — Episode evaluation. See docs/benchmark/SPECIFICATION.md §2 and
docs/architecture/adr/ADR-016-episode-architecture.md.

Per ADR-016: the episode runner is a thin loop over the existing Mode A single-step
pipeline — battery SOC evolves across steps (each step's resulting SOC becomes the next
step's starting SOC), while every other Oracle field follows a per-step schedule the
episode itself defines. No new Scenario/Oracle/Evaluator machinery is introduced here;
this module only adds the loop and episode-level behavioural-metric computation that has
no meaning at the single-step level.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from gridactionbench.agents.base import AgentAdapter
from gridactionbench.core.decision_record import DecisionRecord
from gridactionbench.core.scenario import Scenario
from gridactionbench.evaluators.base import Capability
from gridactionbench.runners.single_step import run_single_step

StepBuilder = Callable[[int, float], Scenario]


@dataclass
class EpisodeSpec:
    episode_id: str
    episode_version: str
    family: str
    steps: int
    initial_soc: float
    build_step: StepBuilder  # (step_index, current_soc) -> Scenario for that step
    # docs/benchmark/CAPABILITY_TAXONOMY.md / docs/benchmark/STRESS_DIMENSIONS.md — added
    # September 2026 strategic realignment (docs/project/GAP_ANALYSIS.md P1), mirroring
    # ScenarioTemplate's tags (gridactionbench/scenarios/generator.py).
    primary_capability: Capability
    u_classes: tuple[str, ...]  # one or more of U0-U7, docs/benchmark/STRESS_DIMENSIONS.md
    description: str = ""
    complexity_rung: str = "C0"  # every GB-BESS v0.1 episode is C0 — single BESS, no other asset
    # Operational tasks are the highest-H proxy rung (STRESS_DIMENSIONS.md, "H — Autonomy
    # Burden"); every EpisodeSpec is Operational, so this default is never overridden.
    autonomy_burden: str = "high"


@dataclass
class EpisodeResult:
    episode_id: str
    step_records: list[DecisionRecord]
    # The actual carried-forward SOC after each step (post hard-constraint gating) —
    # distinct from each record's own simulator_post_state.resulting_soc, which is the
    # HYPOTHETICAL outcome of that step's proposed action, computed for evaluation
    # purposes regardless of validity (docs/architecture/ARCHITECTURE.md's Evaluation
    # Engine). The two only diverge when a step's action was hard-constraint-invalid —
    # exactly the case worth being unambiguous about when reading episode output.
    world_soc_after_step: list[float] = None  # type: ignore[assignment]

    @property
    def any_ucv(self) -> bool:
        return any(r.ucv for r in self.step_records)

    @property
    def ucv_count(self) -> int:
        return sum(1 for r in self.step_records if r.ucv)


def run_episode(episode: EpisodeSpec, agent: AgentAdapter, dt_hours: float, run_id: str | None = None) -> EpisodeResult:
    """Runs one episode to completion, threading SOC from each step's simulator
    post-state into the next step's Oracle. Every step still produces a complete,
    independent Decision Record via the same run_single_step() path Mode A uses — Mode B
    adds no second evaluation code path (ADR-016)."""
    soc = episode.initial_soc
    step_records: list[DecisionRecord] = []
    world_soc_after_step: list[float] = []
    for step in range(episode.steps):
        scenario = episode.build_step(step, soc)
        record = run_single_step(
            scenario, agent, dt_hours, run_id=f"{run_id or episode.episode_id}:step{step}"
        )
        step_records.append(record)
        # Only a HARD-constraint-valid action is allowed to advance the world state —
        # docs/suites/gb-bess/SPECIFICATION.md §9.9: "the simulator only ever executes
        # valid actions." In Mode A this distinction is invisible (there is no next
        # step to protect); in Mode B it is load-bearing. Getting this wrong was a real
        # bug caught immediately by running a genuinely defective agent
        # (IgnoreMinimumSOCAgent) through an episode: it drove the *hypothetical*
        # post-state SOC negative, and the first version of this loop carried that
        # physically-impossible value into the next step's Oracle regardless of
        # validity, crashing on the next step's schema validation. An invalid or
        # errored action leaves the world state unchanged — the correct real-world
        # analogue of "the invalid action never reached the simulator."
        if record.hard_constraint_valid and record.simulator_post_state is not None:
            soc = record.simulator_post_state["resulting_soc"]
        world_soc_after_step.append(soc)
    return EpisodeResult(episode_id=episode.episode_id, step_records=step_records, world_soc_after_step=world_soc_after_step)
