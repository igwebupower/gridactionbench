"""SimpleBessSimulator — the reference simulator.

Implements the frozen conventions in docs/suites/gb-bess/SPECIFICATION.md §9 exactly.
Any change to the equations below is a simulator version bump (docs/benchmark/VERSIONING.md)
with an explicit rationale — never a silent fix.

Simulator version: 0.1.0
"""

from __future__ import annotations

from gridactionbench.schemas.action import ActionType, AgentActionV1
from gridactionbench.schemas.observation import BatteryState
from gridactionbench.simulators.base import StepResult

SIMULATOR_VERSION = "0.1.0"

# Floating-point tolerance, fixed by SPECIFICATION.md §9.7. Applied as `value <= limit +
# EPSILON`, never subtracted from the value side.
EPSILON = 1e-6


class SimpleBessSimulator:
    """Deterministic BESS state-transition model. See module docstring."""

    version = SIMULATOR_VERSION

    def step(
        self,
        battery: BatteryState,
        action: AgentActionV1,
        dt_hours: float,
        seed: int | None = None,
    ) -> StepResult:
        """Deterministic given (battery, action, dt_hours, seed) — §9.9. `seed` is accepted
        for forward compatibility with a future stochastic extension and is unused: every
        equation here is exact arithmetic."""
        del seed  # unused in v0.1 — see docstring

        if action.action is ActionType.CHARGE:
            power_mw = action.power_mw or 0.0
            # §9.3, §9.4: grid-side power * charge_efficiency = battery-side stored energy.
            energy_stored_delta_mwh = power_mw * dt_hours * battery.charge_efficiency
            resulting_soc = battery.soc + energy_stored_delta_mwh / battery.capacity_mwh
            return StepResult(resulting_soc=resulting_soc, energy_stored_delta_mwh=energy_stored_delta_mwh)

        if action.action is ActionType.DISCHARGE:
            power_mw = action.power_mw or 0.0
            # §9.3, §9.4: grid-side power / discharge_efficiency = battery-side energy drawn
            # (more is drawn from the battery than reaches the grid, due to conversion loss).
            energy_drawn_from_battery_mwh = power_mw * dt_hours / battery.discharge_efficiency
            energy_stored_delta_mwh = -energy_drawn_from_battery_mwh
            resulting_soc = battery.soc + energy_stored_delta_mwh / battery.capacity_mwh
            return StepResult(resulting_soc=resulting_soc, energy_stored_delta_mwh=energy_stored_delta_mwh)

        # IDLE / ESCALATE — §9.3: no state transition, no self-discharge modeled in v0.1.
        return StepResult(resulting_soc=battery.soc, energy_stored_delta_mwh=0.0)

    def validate_action(self, battery: BatteryState, action: AgentActionV1) -> bool:
        """Cheap pre-check only — see gridactionbench.core.validator.ActionValidator for
        the canonical, evaluator-driven Action Validator that actually gates execution."""
        if action.action is ActionType.CHARGE:
            power_mw = action.power_mw or 0.0
            return power_mw <= battery.max_charge_mw + EPSILON
        if action.action is ActionType.DISCHARGE:
            power_mw = action.power_mw or 0.0
            return power_mw <= battery.max_discharge_mw + EPSILON
        return True
