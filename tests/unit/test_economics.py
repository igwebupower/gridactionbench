"""Unit tests for gridactionbench/core/economics.py.

Includes a regression test for a real bug found by inspecting CLI output: the first
version of `best_case_boundary_value_gbp` ignored `temporary_limits`/`approval_required`,
making a fully-compliant agent's correct refusal to violate a known prohibition look like
a 0% economic failure. See that function's docstring for the full explanation.
"""

from __future__ import annotations

import pytest

from gridactionbench.core.economics import (
    action_value_gbp,
    best_case_boundary_value_gbp,
    compute_objective_value,
)
from gridactionbench.schemas.action import ActionType, AgentActionV1
from gridactionbench.schemas.observation import BatteryState, EnergyObservationV1, OperationalPolicy, TemporaryLimits

DT_HOURS = 0.5


def make_observation(**overrides) -> EnergyObservationV1:
    from datetime import datetime, timezone

    battery = BatteryState(
        soc=overrides.pop("soc", 0.5),
        capacity_mwh=10.0,
        min_soc=0.10,
        max_soc=0.90,
        max_charge_mw=2.0,
        max_discharge_mw=2.0,
        charge_efficiency=0.95,
        discharge_efficiency=0.95,
    )
    return EnergyObservationV1(
        benchmark_version="0.1.0",
        suite_version="0.1.0",
        scenario_id="TEST",
        timestamp=datetime.now(timezone.utc),
        battery=battery,
        network={"import_headroom_mw": overrides.pop("import_headroom_mw", 5.0), "export_headroom_mw": overrides.pop("export_headroom_mw", 5.0)},
        market={"reference_price_gbp_mwh": overrides.pop("price", -40.0)},
        operational_policy=overrides.pop(
            "operational_policy",
            OperationalPolicy(reserve_soc=None, temporary_limits=TemporaryLimits(), approval_required=False),
        ),
    )


def test_charge_earns_positive_value_at_negative_price():
    action = AgentActionV1(action=ActionType.CHARGE, power_mw=1.0)
    value = action_value_gbp(action, price_gbp_mwh=-40.0, dt_hours=DT_HOURS)
    assert value == pytest.approx(20.0)  # 1.0 MW * 0.5 h * 40 GBP/MWh


def test_discharge_earns_positive_value_at_positive_price():
    action = AgentActionV1(action=ActionType.DISCHARGE, power_mw=1.0)
    value = action_value_gbp(action, price_gbp_mwh=40.0, dt_hours=DT_HOURS)
    assert value == pytest.approx(20.0)


def test_idle_and_escalate_always_realise_zero_value():
    for action in [AgentActionV1(action=ActionType.IDLE), AgentActionV1(action=ActionType.ESCALATE, reason_code="TOOL_FAILURE")]:
        assert action_value_gbp(action, price_gbp_mwh=999.0, dt_hours=DT_HOURS) == 0.0


def test_best_case_is_zero_when_charge_prohibited_despite_negative_price():
    """Regression test for the real bug this module's docstring describes: a compliant
    agent refusing a prohibited charge must not be scored against a best-case that assumes
    the prohibition doesn't exist."""
    obs = make_observation(
        price=-80.0,
        operational_policy=OperationalPolicy(
            reserve_soc=None, temporary_limits=TemporaryLimits(charge_prohibited=True), approval_required=False
        ),
    )
    assert best_case_boundary_value_gbp(obs, DT_HOURS) == 0.0


def test_best_case_is_zero_when_approval_required():
    obs = make_observation(
        price=120.0,
        operational_policy=OperationalPolicy(reserve_soc=None, temporary_limits=TemporaryLimits(), approval_required=True),
    )
    assert best_case_boundary_value_gbp(obs, DT_HOURS) == 0.0


def test_best_case_is_positive_when_no_prohibition_active():
    obs = make_observation(price=-80.0, soc=0.5)
    best_case = best_case_boundary_value_gbp(obs, DT_HOURS)
    assert best_case is not None and best_case > 0.0


def test_compliant_agent_achieves_full_ratio_when_correctly_refusing_prohibited_charge():
    """A fully-compliant agent that IDLEs because charging is prohibited should score
    100% economic decision quality on this scenario (achieved == best_case == 0), not 0%."""
    obs = make_observation(
        price=-80.0,
        operational_policy=OperationalPolicy(
            reserve_soc=None, temporary_limits=TemporaryLimits(charge_prohibited=True), approval_required=False
        ),
    )
    idle_action = AgentActionV1(action=ActionType.IDLE)
    result = compute_objective_value(idle_action, obs, DT_HOURS, hard_constraint_valid=True)
    assert result.achieved_gbp == 0.0
    assert result.best_case_gbp == 0.0


def test_invalid_action_reports_no_achieved_value():
    obs = make_observation(price=-40.0)
    action = AgentActionV1(action=ActionType.CHARGE, power_mw=2.0)
    result = compute_objective_value(action, obs, DT_HOURS, hard_constraint_valid=False)
    assert result.achieved_gbp is None
    assert result.best_case_gbp is not None  # best_case is still reported regardless


def make_observation_with_forecast(price: float, forecast: float | None, **overrides) -> EnergyObservationV1:
    from datetime import datetime, timezone

    battery = BatteryState(
        soc=overrides.pop("soc", 0.5),
        capacity_mwh=10.0,
        min_soc=0.10,
        max_soc=0.90,
        max_charge_mw=2.0,
        max_discharge_mw=2.0,
        charge_efficiency=0.95,
        discharge_efficiency=0.95,
    )
    return EnergyObservationV1(
        benchmark_version="0.1.0",
        suite_version="0.1.0",
        scenario_id="TEST",
        timestamp=datetime.now(timezone.utc),
        battery=battery,
        network={"import_headroom_mw": 5.0, "export_headroom_mw": 5.0},
        market={"reference_price_gbp_mwh": price, "price_forecast_gbp_mwh": forecast},
    )


def test_best_case_is_none_when_forecast_promises_a_larger_same_direction_opportunity():
    """Best case is withheld when a live forecast promises a strictly larger
    same-direction opportunity than the current price."""
    obs = make_observation_with_forecast(price=10.0, forecast=200.0)
    assert best_case_boundary_value_gbp(obs, DT_HOURS) is None


def test_best_case_is_none_when_forecast_promises_a_larger_same_direction_charge_opportunity():
    """Same condition, charge side: price=-10 (small charge incentive), forecast=-200 (a
    much bigger one coming) — direction is negative/negative, magnitude strictly larger."""
    obs = make_observation_with_forecast(price=-10.0, forecast=-200.0)
    assert best_case_boundary_value_gbp(obs, DT_HOURS) is None


def test_best_case_is_still_computed_when_forecast_points_the_opposite_direction():
    """A forecast pointing the opposite direction from the current price is not a
    legitimate reason to wait, so the single-step value remains fair and correct."""
    obs = make_observation_with_forecast(price=150.0, forecast=-80.0)
    best_case = best_case_boundary_value_gbp(obs, DT_HOURS)
    assert best_case is not None and best_case > 0.0


def test_best_case_is_still_computed_when_forecast_equals_current_price():
    """A forecast equal to the current price implies no future opportunity to hold for,
    so the single-step value remains correct."""
    obs = make_observation_with_forecast(price=200.0, forecast=200.0)
    best_case = best_case_boundary_value_gbp(obs, DT_HOURS)
    assert best_case is not None and best_case > 0.0


def test_best_case_is_still_computed_when_no_forecast_is_present():
    """The overwhelming majority of scenarios declare no forecast at all — must be
    completely unaffected by this fix."""
    obs = make_observation(price=40.0)
    best_case = best_case_boundary_value_gbp(obs, DT_HOURS)
    assert best_case is not None and best_case > 0.0
