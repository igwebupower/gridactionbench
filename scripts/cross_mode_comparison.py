"""Cross-mode reliability comparison: the same 10 agents, Atomic vs. Operational.

Produces the data behind docs/benchmark/CROSS_MODE_COMPARISON.md (docs/project/
GAP_ANALYSIS.md's research traceability matrix, "Does good atomic performance predict
sequential or operational reliability?" — previously "None yet as its own analysis" since
the two evidence sources, docs/benchmark/CALIBRATION_RESULTS.md and tests/golden/
test_episodes.py, existed independently but had never been compared side by side for the
same agent). Read-only against existing scenarios/episodes — adds no new scenario content,
changes no evaluator, and does not modify run_episode() or any check_*() function.

Run:
    python scripts/cross_mode_comparison.py
"""

from __future__ import annotations

from baselines.always_escalate.agent import AlwaysEscalateAgent
from baselines.always_idle.agent import AlwaysIdleAgent
from baselines.rule_based.agent import RuleBasedAgent
from baselines.seeded_failures.always_charge import AlwaysChargeAgent
from baselines.seeded_failures.ignore_minimum_soc import IgnoreMinimumSOCAgent
from baselines.seeded_failures.ignore_network import IgnoreNetworkAgent
from baselines.seeded_failures.never_escalate import NeverEscalateAgent
from baselines.seeded_failures.prompt_injection_victim import PromptInjectionVictimAgent
from baselines.seeded_failures.revenue_first_constraint_ignoring import RevenueFirstConstraintIgnoringAgent
from baselines.seeded_failures.trust_all_telemetry import TrustAllTelemetryAgent
from gridactionbench.core.episode import run_episode
from gridactionbench.core.scenario import load_scenario_dir
from gridactionbench.reporting.report import build_report
from gridactionbench.runners.single_step import run_single_step
from gridactionbench.scenarios.gb_bess.episodes import EPISODES

DT_HOURS = 0.5
SCENARIO_DIR = "suites/gb_bess/v0_1/scenarios"

# Same 10 agents, same order, as docs/benchmark/CALIBRATION_RESULTS.md — this script
# reuses that document's exact roster so the two tables are directly comparable.
AGENTS = {
    "always-idle": lambda: AlwaysIdleAgent(),
    "always-escalate": lambda: AlwaysEscalateAgent(),
    "rule-based": lambda: RuleBasedAgent(dt_hours=DT_HOURS),
    "always-charge": lambda: AlwaysChargeAgent(),
    "ignore-network": lambda: IgnoreNetworkAgent(dt_hours=DT_HOURS),
    "ignore-minimum-soc": lambda: IgnoreMinimumSOCAgent(dt_hours=DT_HOURS),
    "revenue-first-constraint-ignoring": lambda: RevenueFirstConstraintIgnoringAgent(dt_hours=DT_HOURS),
    "trust-all-telemetry": lambda: TrustAllTelemetryAgent(dt_hours=DT_HOURS),
    "never-escalate": lambda: NeverEscalateAgent(dt_hours=DT_HOURS),
    "prompt-injection-victim": lambda: PromptInjectionVictimAgent(dt_hours=DT_HOURS),
}


def atomic_result(agent_factory) -> tuple[int, int]:
    scenarios = load_scenario_dir(SCENARIO_DIR)
    records = [run_single_step(s, agent_factory(), DT_HOURS) for s in scenarios]
    report = build_report(records)
    return report.ucv_count, report.total_scenarios


def operational_result(agent_factory) -> tuple[int, int, list[str]]:
    ucv_count = 0
    total_steps = 0
    episodes_with_ucv = []
    for episode_id, (episode, _check_fn) in EPISODES.items():
        result = run_episode(episode, agent_factory(), DT_HOURS)
        ucv_count += result.ucv_count
        total_steps += episode.steps
        if result.any_ucv:
            episodes_with_ucv.append(episode_id)
    return ucv_count, total_steps, episodes_with_ucv


def main() -> None:
    rows = []
    for name, factory in AGENTS.items():
        atomic_ucv, atomic_n = atomic_result(factory)
        op_ucv, op_n, op_episodes = operational_result(factory)
        rows.append((name, atomic_ucv, atomic_n, op_ucv, op_n, op_episodes))

    header = f"{'Agent':<36}{'Atomic UCV':<14}{'Operational UCV':<18}{'Episodes with a UCV'}"
    print(header)
    print("-" * len(header))
    for name, a_ucv, a_n, o_ucv, o_n, o_eps in rows:
        eps_str = ", ".join(e.replace("GB-BESS-", "") for e in o_eps) if o_eps else "none"
        print(f"{name:<36}{a_ucv}/{a_n:<12}{o_ucv}/{o_n:<16}{eps_str}")


if __name__ == "__main__":
    main()
