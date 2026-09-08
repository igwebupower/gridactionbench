"""IgnoreNetworkAgent — seeded failure agent. See master brief §27.

Makes otherwise SOC-aware, price-responsive decisions (mirroring RuleBasedAgent's
charge/discharge trigger logic) but computes requested power from the rate limit and SOC
headroom only, never consulting `network.import_headroom_mw` / `export_headroom_mw`.

Expected failure mode: NET-IMPORT-HEADROOM-001 / NET-EXPORT-HEADROOM-001 failures (and
resulting UCVs) whenever the true network headroom is more restrictive than the rate/SOC
limit — e.g. GB-BESS-NET-007 through NET-010, where this is precisely the scenario design.
"""

from __future__ import annotations

from gridactionbench.schemas.action import ActionType, AgentActionV1
from gridactionbench.schemas.observation import EnergyObservationV1


class IgnoreNetworkAgent:
    agent_id = "ignore-network"
    agent_version = "0.1.0"
    agent_type = "seeded_failure"

    def __init__(self, dt_hours: float):
        self.dt_hours = dt_hours

    def act(self, observation: EnergyObservationV1) -> AgentActionV1:
        battery = observation.battery
        policy = observation.operational_policy
        price = observation.market.reference_price_gbp_mwh

        if price is not None and price < 0 and not policy.temporary_limits.charge_prohibited:
            power = self._max_charge_power_ignoring_network(observation)
            if power > 1e-9:
                return AgentActionV1(action=ActionType.CHARGE, power_mw=power)

        if price is not None and price > 0 and not policy.temporary_limits.discharge_prohibited:
            power = self._max_discharge_power_ignoring_network(observation)
            if power > 1e-9:
                return AgentActionV1(action=ActionType.DISCHARGE, power_mw=power)

        return AgentActionV1(action=ActionType.IDLE)

    def _max_charge_power_ignoring_network(self, observation: EnergyObservationV1) -> float:
        battery = observation.battery
        capacity_limit = (battery.max_soc - battery.soc) * battery.capacity_mwh / (
            battery.charge_efficiency * self.dt_hours
        )
        return max(0.0, min(battery.max_charge_mw, capacity_limit))  # deliberately no headroom term

    def _max_discharge_power_ignoring_network(self, observation: EnergyObservationV1) -> float:
        battery = observation.battery
        floor = max(battery.min_soc, observation.operational_policy.reserve_soc or battery.min_soc)
        energy_limit = (battery.soc - floor) * battery.capacity_mwh * battery.discharge_efficiency / self.dt_hours
        return max(0.0, min(battery.max_discharge_mw, energy_limit))  # deliberately no headroom term
