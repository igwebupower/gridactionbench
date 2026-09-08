"""Unit + physical-invariant tests for SimpleBessSimulator.

See docs/suites/gb-bess/SPECIFICATION.md §9 (frozen conventions) and docs/testing/
TEST_STRATEGY.md, "Physical invariants."
"""

from __future__ import annotations

import pytest

from gridactionbench.schemas.action import ActionType, AgentActionV1
from gridactionbench.schemas.observation import BatteryState
from gridactionbench.simulators.simple_bess import EPSILON, SimpleBessSimulator

DT_HOURS = 0.5


def make_battery(**overrides) -> BatteryState:
    defaults = dict(
        soc=0.5,
        capacity_mwh=10.0,
        min_soc=0.10,
        max_soc=0.90,
        max_charge_mw=2.0,
        max_discharge_mw=2.0,
        charge_efficiency=0.95,
        discharge_efficiency=0.95,
    )
    defaults.update(overrides)
    return BatteryState(**defaults)


@pytest.fixture
def sim() -> SimpleBessSimulator:
    return SimpleBessSimulator()


def test_charge_soc_transition_matches_canonical_equation(sim):
    battery = make_battery(soc=0.50, capacity_mwh=10.0, charge_efficiency=0.95)
    action = AgentActionV1(action=ActionType.CHARGE, power_mw=1.0)
    result = sim.step(battery, action, DT_HOURS)

    expected_energy = 1.0 * DT_HOURS * 0.95
    expected_soc = 0.50 + expected_energy / 10.0
    assert result.energy_stored_delta_mwh == pytest.approx(expected_energy)
    assert result.resulting_soc == pytest.approx(expected_soc)


def test_discharge_soc_transition_matches_canonical_equation(sim):
    battery = make_battery(soc=0.50, capacity_mwh=10.0, discharge_efficiency=0.95)
    action = AgentActionV1(action=ActionType.DISCHARGE, power_mw=1.0)
    result = sim.step(battery, action, DT_HOURS)

    expected_drawn = 1.0 * DT_HOURS / 0.95
    expected_soc = 0.50 - expected_drawn / 10.0
    assert result.energy_stored_delta_mwh == pytest.approx(-expected_drawn)
    assert result.resulting_soc == pytest.approx(expected_soc)


def test_idle_and_escalate_produce_no_state_change(sim):
    battery = make_battery(soc=0.42)
    for action_type in (ActionType.IDLE, ActionType.ESCALATE):
        action = (
            AgentActionV1(action=action_type)
            if action_type is ActionType.IDLE
            else AgentActionV1(action=action_type, reason_code="TOOL_FAILURE")
        )
        result = sim.step(battery, action, DT_HOURS)
        assert result.resulting_soc == battery.soc
        assert result.energy_stored_delta_mwh == 0.0


def test_zero_power_charge_is_physically_equivalent_to_idle_but_flagged(sim):
    battery = make_battery(soc=0.42)
    action = AgentActionV1(action=ActionType.CHARGE, power_mw=0.0)
    assert action.zero_power_irregularity is True
    result = sim.step(battery, action, DT_HOURS)
    assert result.resulting_soc == battery.soc
    assert result.energy_stored_delta_mwh == 0.0


def test_negative_power_mw_is_rejected_by_schema():
    with pytest.raises(ValueError):
        AgentActionV1(action=ActionType.CHARGE, power_mw=-1.0)


def test_idle_with_nonzero_power_is_rejected_by_schema():
    with pytest.raises(ValueError):
        AgentActionV1(action=ActionType.IDLE, power_mw=1.0)


def test_escalate_without_reason_code_is_rejected_by_schema():
    with pytest.raises(ValueError):
        AgentActionV1(action=ActionType.ESCALATE)


# --- Physical invariants (docs/testing/TEST_STRATEGY.md, "Physical invariants") ---


def test_energy_conservation_invariant_charge(sim):
    battery = make_battery(soc=0.30, capacity_mwh=8.0, charge_efficiency=0.9)
    action = AgentActionV1(action=ActionType.CHARGE, power_mw=1.5)
    result = sim.step(battery, action, DT_HOURS)
    delta_soc_energy = (result.resulting_soc - battery.soc) * battery.capacity_mwh
    assert delta_soc_energy == pytest.approx(result.energy_stored_delta_mwh, abs=EPSILON * 10)


def test_energy_conservation_invariant_discharge(sim):
    battery = make_battery(soc=0.70, capacity_mwh=8.0, discharge_efficiency=0.9)
    action = AgentActionV1(action=ActionType.DISCHARGE, power_mw=1.5)
    result = sim.step(battery, action, DT_HOURS)
    delta_soc_energy = (result.resulting_soc - battery.soc) * battery.capacity_mwh
    assert delta_soc_energy == pytest.approx(result.energy_stored_delta_mwh, abs=EPSILON * 10)


def test_round_trip_is_strictly_lossy_when_efficiency_below_one(sim):
    battery = make_battery(soc=0.50, capacity_mwh=10.0, charge_efficiency=0.9, discharge_efficiency=0.9)
    charged = sim.step(battery, AgentActionV1(action=ActionType.CHARGE, power_mw=1.0), DT_HOURS)
    battery_after_charge = make_battery(soc=charged.resulting_soc, capacity_mwh=10.0, charge_efficiency=0.9, discharge_efficiency=0.9)
    discharged = sim.step(battery_after_charge, AgentActionV1(action=ActionType.DISCHARGE, power_mw=1.0), DT_HOURS)
    assert discharged.resulting_soc < battery.soc, "round-trip with efficiency < 1.0 must strictly lose energy"


def test_round_trip_is_energy_neutral_at_unity_efficiency(sim):
    battery = make_battery(soc=0.50, capacity_mwh=10.0, charge_efficiency=1.0, discharge_efficiency=1.0)
    charged = sim.step(battery, AgentActionV1(action=ActionType.CHARGE, power_mw=1.0), DT_HOURS)
    battery_after_charge = make_battery(soc=charged.resulting_soc, capacity_mwh=10.0, charge_efficiency=1.0, discharge_efficiency=1.0)
    discharged = sim.step(battery_after_charge, AgentActionV1(action=ActionType.DISCHARGE, power_mw=1.0), DT_HOURS)
    assert discharged.resulting_soc == pytest.approx(battery.soc, abs=1e-9)


def test_timestep_linearity(sim):
    battery = make_battery(soc=0.50, capacity_mwh=10.0, charge_efficiency=0.95)
    action = AgentActionV1(action=ActionType.CHARGE, power_mw=1.0)
    full = sim.step(battery, action, dt_hours=1.0)
    half = sim.step(battery, action, dt_hours=0.5)
    assert half.energy_stored_delta_mwh == pytest.approx(full.energy_stored_delta_mwh / 2.0)


def test_deterministic_reproducibility(sim):
    battery = make_battery(soc=0.37)
    action = AgentActionV1(action=ActionType.DISCHARGE, power_mw=0.7)
    results = [sim.step(battery, action, DT_HOURS, seed=42).resulting_soc for _ in range(5)]
    assert len(set(results)) == 1, "identical (battery, action, dt_hours, seed) must be bit-identical across runs"
