"""Reproducibility tests. See docs/testing/TEST_STRATEGY.md, "Reproducibility tests."

A deterministic agent, given the same scenario and seed, always produces the same
AgentActionV1 and the same evaluation result (docs/testing/TEST_STRATEGY.md, "Property /
invariant tests").
"""

from __future__ import annotations

from pathlib import Path

from baselines.rule_based.agent import RuleBasedAgent
from gridactionbench.core.scenario import load_scenario_dir
from gridactionbench.runners.single_step import run_single_step

SCENARIO_DIR = Path(__file__).resolve().parent.parent.parent / "suites" / "gb_bess" / "v0_1" / "scenarios"
DT_HOURS = 0.5


def test_rule_based_agent_is_deterministic_across_repeated_runs():
    scenarios = load_scenario_dir(SCENARIO_DIR)
    agent = RuleBasedAgent(dt_hours=DT_HOURS)
    for scenario in scenarios:
        records = [run_single_step(scenario, agent, DT_HOURS, run_id="fixed") for _ in range(3)]
        actions = [r.parsed_action.model_dump() for r in records]
        assert all(a == actions[0] for a in actions), f"{scenario.scenario_id}: action not deterministic"
        results = [[e["result"] for e in r.evaluation_results] for r in records]
        assert all(r == results[0] for r in results), f"{scenario.scenario_id}: evaluation not deterministic"


def test_fresh_scenario_load_reproduces_identical_evaluation():
    """A fresh reload of the same scenario file (simulating a clean-environment re-run)
    must reproduce identical evaluation results — docs/testing/TEST_STRATEGY.md."""
    scenario_path = SCENARIO_DIR / "GB-BESS-PHY-001.yaml"
    from gridactionbench.core.scenario import load_scenario

    agent = RuleBasedAgent(dt_hours=DT_HOURS)
    r1 = run_single_step(load_scenario(scenario_path), agent, DT_HOURS)
    r2 = run_single_step(load_scenario(scenario_path), agent, DT_HOURS)
    assert [e["result"] for e in r1.evaluation_results] == [e["result"] for e in r2.evaluation_results]
