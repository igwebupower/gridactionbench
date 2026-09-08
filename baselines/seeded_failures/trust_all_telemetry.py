"""TrustAllTelemetryAgent — seeded failure agent. See master brief §27.

Behaves like RuleBasedAgent's charge/discharge logic, but never inspects
`telemetry.field_status`, `missing_fields`, or `quality_flags` at all — acts on whatever
numeric values are present in the observation, however stale, conflicting, missing, or
implausible they are, at face value. Reports high self-reported confidence regardless.

Expected failure mode: fails every DATA-family evaluator (DATA-MISSING-SOC-001,
DATA-STALE-SOC-001, DATA-CONFLICT-SOC-001, DATA-IMPLAUSIBLE-HEADROOM-001) whenever their
condition is triggered and the resulting action depends on the bad field — all four are
ucv_eligible, and DATA-IMPLAUSIBLE-HEADROOM-001 is exactly the scenario
(GB-BESS-DATA-017) the master brief's own Self-Reported High-Confidence UCV worked example
is modeled on.
"""

from __future__ import annotations

from gridactionbench.schemas.action import ActionType, AgentActionV1
from gridactionbench.schemas.observation import EnergyObservationV1


class TrustAllTelemetryAgent:
    agent_id = "trust-all-telemetry"
    agent_version = "0.1.0"
    agent_type = "seeded_failure"

    def __init__(self, dt_hours: float):
        self.dt_hours = dt_hours

    def act(self, observation: EnergyObservationV1) -> AgentActionV1:
        battery = observation.battery
        policy = observation.operational_policy
        price = observation.market.reference_price_gbp_mwh

        if price is not None and price < 0 and not policy.temporary_limits.charge_prohibited:
            power = self._max_charge_power(observation)
            if power > 1e-9:
                return AgentActionV1(action=ActionType.CHARGE, power_mw=power, confidence=0.95)

        if price is not None and price > 0 and not policy.temporary_limits.discharge_prohibited:
            power = self._max_discharge_power(observation)
            if power > 1e-9:
                return AgentActionV1(action=ActionType.DISCHARGE, power_mw=power, confidence=0.95)

        return AgentActionV1(action=ActionType.IDLE)

    def _max_charge_power(self, observation: EnergyObservationV1) -> float:
        battery = observation.battery
        candidates = [battery.max_charge_mw]
        if observation.network.import_headroom_mw is not None:
            candidates.append(observation.network.import_headroom_mw)  # trusted at face value, however implausible
        capacity_limit = (battery.max_soc - battery.soc) * battery.capacity_mwh / (
            battery.charge_efficiency * self.dt_hours
        )
        candidates.append(capacity_limit)
        return max(0.0, min(candidates))

    def _max_discharge_power(self, observation: EnergyObservationV1) -> float:
        battery = observation.battery
        floor = max(battery.min_soc, observation.operational_policy.reserve_soc or battery.min_soc)
        candidates = [battery.max_discharge_mw]
        if observation.network.export_headroom_mw is not None:
            candidates.append(observation.network.export_headroom_mw)  # trusted at face value
        energy_limit = (battery.soc - floor) * battery.capacity_mwh * battery.discharge_efficiency / self.dt_hours
        candidates.append(energy_limit)
        return max(0.0, min(candidates))
