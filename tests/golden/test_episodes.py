"""Calibration tests for the 6 GB-BESS episodes (Mode B). See docs/suites/gb-bess/
SCENARIO_CATALOGUE.md, "Episode scenarios," and docs/architecture/adr/
ADR-016-episode-architecture.md.

Each episode's failure_signature check is verified bidirectionally: RuleBasedAgent (the
transparent, compliant reference controller) must never trigger it, and at least one
seeded failure agent whose documented defect matches the episode's design intent must
trigger it reliably. A failure_signature that never triggers for any agent would be a
dead check; a failure_signature that triggers even for a compliant agent would be a false
positive — both are equally important to rule out.
"""

from __future__ import annotations

from baselines.always_escalate.agent import AlwaysEscalateAgent
from baselines.rule_based.agent import RuleBasedAgent
from baselines.seeded_failures.always_charge import AlwaysChargeAgent
from baselines.seeded_failures.ignore_minimum_soc import IgnoreMinimumSOCAgent
from baselines.seeded_failures.ignore_network import IgnoreNetworkAgent
from baselines.seeded_failures.never_escalate import NeverEscalateAgent
from baselines.seeded_failures.revenue_first_constraint_ignoring import RevenueFirstConstraintIgnoringAgent
from baselines.seeded_failures.trust_all_telemetry import TrustAllTelemetryAgent
from gridactionbench.core.episode import run_episode
from gridactionbench.schemas.action import ActionType
from gridactionbench.scenarios.gb_bess.episodes import EPISODES

DT_HOURS = 0.5


def test_every_episode_step_produces_a_complete_decision_record():
    agent = RuleBasedAgent(dt_hours=DT_HOURS)
    for episode_id, (spec, _check) in EPISODES.items():
        result = run_episode(spec, agent, DT_HOURS)
        assert len(result.step_records) == spec.steps
        for record in result.step_records:
            assert record.schema_valid is True
            assert record.errors == []


def test_rule_based_agent_never_triggers_any_episode_failure_signature():
    agent = RuleBasedAgent(dt_hours=DT_HOURS)
    for episode_id, (spec, check) in EPISODES.items():
        result = run_episode(spec, agent, DT_HOURS)
        signature = check(result)
        assert not signature.triggered, f"{episode_id}: unexpected trigger — {signature.detail}"


def test_ep001_progressive_soc_depletion_triggers_for_ignore_minimum_soc_agent():
    spec, check = EPISODES["GB-BESS-EP-001"]
    result = run_episode(spec, IgnoreMinimumSOCAgent(dt_hours=DT_HOURS), DT_HOURS)
    assert check(result).triggered


def test_ep002_soc_ceiling_approach_triggers_for_always_charge_agent():
    spec, check = EPISODES["GB-BESS-EP-002"]
    result = run_episode(spec, AlwaysChargeAgent(), DT_HOURS)
    assert check(result).triggered


def test_ep003_network_constraint_change_triggers_for_ignore_network_agent():
    spec, check = EPISODES["GB-BESS-EP-003"]
    result = run_episode(spec, IgnoreNetworkAgent(dt_hours=DT_HOURS), DT_HOURS)
    assert check(result).triggered


def test_ep004_telemetry_degradation_triggers_for_trust_all_telemetry_agent():
    spec, check = EPISODES["GB-BESS-EP-004"]
    result = run_episode(spec, TrustAllTelemetryAgent(dt_hours=DT_HOURS), DT_HOURS)
    assert check(result).triggered


def test_ep005_temporary_restriction_triggers_for_revenue_first_agent():
    spec, check = EPISODES["GB-BESS-EP-005"]
    result = run_episode(spec, RevenueFirstConstraintIgnoringAgent(dt_hours=DT_HOURS), DT_HOURS)
    assert check(result).triggered


def test_ep006_repeated_escalation_triggers_for_never_escalate_agent():
    spec, check = EPISODES["GB-BESS-EP-006"]
    result = run_episode(spec, NeverEscalateAgent(dt_hours=DT_HOURS), DT_HOURS)
    assert check(result).triggered


def test_ep006_repeated_escalation_also_triggers_for_always_escalate_agent():
    """The other direction of EP-006's discrimination check — always escalating is
    exactly as much a failure as never escalating, per master brief §22."""
    spec, check = EPISODES["GB-BESS-EP-006"]
    result = run_episode(spec, AlwaysEscalateAgent(), DT_HOURS)
    assert check(result).triggered


def test_invalid_action_does_not_advance_episode_state():
    """Regression test for a real bug: the first version of run_episode() carried the
    simulator's hypothetical post-state SOC forward even when the action was
    hard-constraint-invalid, letting IgnoreMinimumSOCAgent drive SOC negative and crash
    the next step's schema validation. An invalid action must leave the world state
    unchanged (docs/suites/gb-bess/SPECIFICATION.md §9.9)."""
    spec, _check = EPISODES["GB-BESS-EP-001"]
    result = run_episode(spec, IgnoreMinimumSOCAgent(dt_hours=DT_HOURS), DT_HOURS)
    for record in result.step_records:
        # capacity_mwh's pydantic constraint alone guarantees soc stayed in [0, 1] for
        # every step's Oracle to have validated at all, but check explicitly too.
        assert record.observation.battery.soc >= 0.0
