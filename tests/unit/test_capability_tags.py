"""Tests for capability (docs/benchmark/CAPABILITY_TAXONOMY.md) and stress-dimension
(docs/benchmark/STRESS_DIMENSIONS.md) tagging — added September 2026 strategic realignment,
closing docs/project/GAP_ANALYSIS.md's P1 tagging gap and guarding against
docs/project/RISK_REGISTER.md R-19 (tagging going unapplied to future additions).

These tests check that every evaluator and Task Family carries a valid tag, not that any
tag assignment is "correct" in some absolute sense — capability/stress-dimension
assignment is a documented judgment call (docs/benchmark/STRESS_DIMENSIONS.md, "Calibration
input, not calibration output"), reviewable but not itself computable.
"""

from __future__ import annotations

from gridactionbench.evaluators.base import Capability
from gridactionbench.evaluators.gb_bess import STANDARD_EVALUATORS
from gridactionbench.evaluators.gb_bess import adv, hum
from gridactionbench.scenarios.gb_bess.episodes import EPISODES
from gridactionbench.scenarios.generator import TEMPLATES

VALID_U_CLASSES = {f"U{i}" for i in range(8)}


def test_every_standard_evaluator_has_a_valid_primary_capability():
    for evaluator in STANDARD_EVALUATORS:
        assert isinstance(evaluator.primary_capability, Capability), evaluator.eval_id


def test_adv_and_hum_module_level_capability_constants_are_valid():
    assert isinstance(adv.PRIMARY_CAPABILITY, Capability)
    assert isinstance(hum.REQUIRED_ESCALATION_PRIMARY_CAPABILITY, Capability)
    assert isinstance(hum.UNNECESSARY_ESCALATION_PRIMARY_CAPABILITY, Capability)
    assert hum.REQUIRED_ESCALATION_SECONDARY_CAPABILITIES == (Capability.PERCEIVE,)


def test_evaluate_results_carry_the_evaluator_s_primary_capability():
    """A tag that never reaches EvaluationResult is exactly the "documentation-only
    decoration" docs/project/RISK_REGISTER.md R-19 warns against — spot-check one
    evaluator rather than re-running every branch already covered by
    tests/unit/test_evaluators.py."""
    from gridactionbench.core.scenario import EscalationSpec, Oracle, Scenario
    from gridactionbench.evaluators.base import Context
    from gridactionbench.evaluators.gb_bess.phy import PhySocMax001
    from gridactionbench.schemas.action import ActionType, AgentActionV1
    from gridactionbench.schemas.observation import BatteryState
    from gridactionbench.simulators.simple_bess import SimpleBessSimulator

    scenario = Scenario(
        scenario_id="TAG-CHECK-001",
        scenario_version="0.1.0",
        family="PHY",
        oracle=Oracle(
            battery=BatteryState(
                soc=0.5,
                capacity_mwh=10.0,
                min_soc=0.10,
                max_soc=0.90,
                max_charge_mw=2.0,
                max_discharge_mw=2.0,
                charge_efficiency=0.95,
                discharge_efficiency=0.95,
            ),
            network={"import_headroom_mw": 5.0, "export_headroom_mw": 5.0},
            operational_policy={
                "reserve_soc": None,
                "temporary_limits": {"charge_prohibited": False, "discharge_prohibited": False},
                "approval_required": False,
            },
        ),
        escalation=EscalationSpec(required=False, permitted=True),
    )
    action = AgentActionV1(action=ActionType.CHARGE, power_mw=5.0)
    observation = scenario.build_observation()
    post_state = SimpleBessSimulator().step(scenario.oracle.battery, action, 0.5)
    ctx = Context(scenario=scenario, action=action, observation=observation, post_state=post_state, dt_hours=0.5)

    result = PhySocMax001().evaluate(ctx)
    assert result.primary_capability is Capability.ACT


def test_every_scenario_template_has_valid_stress_dimension_and_capability_tags():
    for template in TEMPLATES:
        assert isinstance(template.primary_capability, Capability), template.template_id
        assert template.u_classes, template.template_id
        assert set(template.u_classes) <= VALID_U_CLASSES, template.template_id
        assert template.complexity_rung == "C0", template.template_id
        assert template.autonomy_burden == "low", template.template_id


def test_every_episode_has_valid_stress_dimension_and_capability_tags():
    for episode_id, (episode, _check_fn) in EPISODES.items():
        assert isinstance(episode.primary_capability, Capability), episode_id
        assert episode.u_classes, episode_id
        assert set(episode.u_classes) <= VALID_U_CLASSES, episode_id
        assert episode.complexity_rung == "C0", episode_id
        assert episode.autonomy_burden == "high", episode_id


def test_episodes_naming_adapt_as_primary_match_the_taxonomy_s_own_account():
    """docs/benchmark/CAPABILITY_TAXONOMY.md, "ADAPT": four of the seven existing episodes
    touch this — GB-BESS-EP-003, EP-004, EP-005 (changing conditions) and EP-007 (a
    forecast that turns out wrong, added 2026-09-09). This test pins that claim to the
    actual tags so the two cannot silently drift apart."""
    adapt_episodes = {
        episode_id for episode_id, (episode, _check_fn) in EPISODES.items() if episode.primary_capability is Capability.ADAPT
    }
    assert adapt_episodes == {"GB-BESS-EP-003", "GB-BESS-EP-004", "GB-BESS-EP-005", "GB-BESS-EP-007"}
