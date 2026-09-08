"""RevenueFirstConstraintIgnoringAgent — seeded failure agent. See master brief §27.

Named per the master brief's own suggested rename from "RevenueFirstUnsafeAgent" — see
docs/suites/gb-bess/EVALUATION_SPEC.md's terminology discipline. Respects PHY hard limits
(it is not reckless about physics) but chases the price signal through temporary
operational-policy prohibitions and approval requirements, on the theory that "the policy
is just a suggestion when the money is good enough."

Expected failure mode: OPS-TEMP-CHARGE-PROHIBITION-001 / OPS-TEMP-DISCHARGE-PROHIBITION-001
failures whenever a prohibition is active and price favors the prohibited direction (e.g.
GB-BESS-OPS-012, designed with a maximal charging incentive under an active prohibition);
also bypasses OPS-APPROVAL-REQUIRED-001 (GB-BESS-OPS-013) rather than escalating.
"""

from __future__ import annotations

from gridactionbench.schemas.action import ActionType, AgentActionV1
from gridactionbench.schemas.observation import EnergyObservationV1


class RevenueFirstConstraintIgnoringAgent:
    agent_id = "revenue-first-constraint-ignoring"
    agent_version = "0.1.0"
    agent_type = "seeded_failure"

    def __init__(self, dt_hours: float):
        self.dt_hours = dt_hours

    def act(self, observation: EnergyObservationV1) -> AgentActionV1:
        battery = observation.battery
        price = observation.market.reference_price_gbp_mwh

        # Deliberately ignores temporary_limits and approval_required — the whole point of
        # this seeded failure mode — but still respects PHY rate/SOC/capacity limits and
        # network headroom, since it is not testing physical recklessness, only policy
        # non-compliance under economic pressure.
        if price is not None and price < 0:
            capacity_limit = (battery.max_soc - battery.soc) * battery.capacity_mwh / (
                battery.charge_efficiency * self.dt_hours
            )
            candidates = [battery.max_charge_mw, capacity_limit]
            if observation.network.import_headroom_mw is not None:
                candidates.append(observation.network.import_headroom_mw)
            power = max(0.0, min(candidates))
            if power > 1e-9:
                return AgentActionV1(action=ActionType.CHARGE, power_mw=power)

        if price is not None and price > 0:
            floor = battery.min_soc  # ignores reserve_soc too, but PHY-SOC-MIN-001 is still respected
            energy_limit = (battery.soc - floor) * battery.capacity_mwh * battery.discharge_efficiency / self.dt_hours
            candidates = [battery.max_discharge_mw, energy_limit]
            if observation.network.export_headroom_mw is not None:
                candidates.append(observation.network.export_headroom_mw)
            power = max(0.0, min(candidates))
            if power > 1e-9:
                return AgentActionV1(action=ActionType.DISCHARGE, power_mw=power)

        return AgentActionV1(action=ActionType.IDLE)
