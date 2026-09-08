"""Calibration sweep over the parameterised generated scenario set.

Complements tests/golden/test_golden_scenarios.py and test_seeded_failure_agents.py
(which cover the 20 hand-authored scenarios): this file runs the same reference agents
against the generator's ~300-scenario output. This is precisely the kind of check that
caught a real RuleBasedAgent bug during Phase 3 development (it never checked
`telemetry.field_status.network`, invisible in the hand-authored 20 because the one
scenario testing that condition also has a SOC conflict the agent already handled — see
CHANGELOG.md) — kept as a permanent regression test, not just a one-off debugging step.
"""

from __future__ import annotations

from baselines.always_escalate.agent import AlwaysEscalateAgent
from baselines.always_idle.agent import AlwaysIdleAgent
from baselines.rule_based.agent import RuleBasedAgent
from gridactionbench.runners.single_step import run_single_step
from gridactionbench.scenarios.generator import generate

DT_HOURS = 0.5
N_PER_TEMPLATE = 15
SEED = 42


def test_generated_scenarios_run_without_error():
    scenarios = generate(n_per_template=N_PER_TEMPLATE, seed=SEED)
    agent = RuleBasedAgent(dt_hours=DT_HOURS)
    for scenario in scenarios:
        record = run_single_step(scenario, agent, DT_HOURS)
        assert record.errors == []
        assert record.schema_valid is True


def test_rule_based_agent_produces_zero_ucvs_across_the_generated_set():
    """The regression test for the network-field_status bug: RuleBasedAgent must have
    zero UCVs across the full generated set, not just the hand-authored 20 — a
    template-specific regression would previously have been invisible to the smaller,
    hand-picked scenario set."""
    scenarios = generate(n_per_template=N_PER_TEMPLATE, seed=SEED)
    agent = RuleBasedAgent(dt_hours=DT_HOURS)
    ucv_scenarios = [s.scenario_id for s in scenarios if run_single_step(s, agent, DT_HOURS).ucv]
    assert ucv_scenarios == [], f"RuleBasedAgent produced UCVs on generated scenarios: {ucv_scenarios[:5]}"


def test_always_idle_agent_produces_many_ucvs_across_the_generated_set():
    """Sanity check the other direction: a known-defective baseline should still be
    caught reliably at this larger scale, not just on the hand-picked 20."""
    scenarios = generate(n_per_template=N_PER_TEMPLATE, seed=SEED)
    agent = AlwaysIdleAgent()
    ucv_count = sum(1 for s in scenarios if run_single_step(s, agent, DT_HOURS).ucv)
    assert ucv_count > 0


def test_always_escalate_agent_never_produces_a_ucv_across_the_generated_set():
    scenarios = generate(n_per_template=N_PER_TEMPLATE, seed=SEED)
    agent = AlwaysEscalateAgent()
    ucv_count = sum(1 for s in scenarios if run_single_step(s, agent, DT_HOURS).ucv)
    assert ucv_count == 0
