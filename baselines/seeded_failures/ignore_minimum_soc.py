"""IgnoreMinimumSOCAgent — seeded failure agent. See master brief §27.

Discharges at the full rate/headroom-bounded limit purely on price signal, ignoring
min_soc and reserve_soc entirely (the one boundary a real controller must never ignore).

Expected failure mode: PHY-SOC-MIN-001 and/or PHY-ENERGY-AVAILABLE-001 failures whenever
SOC is close to min_soc; OPS-RESERVE-SOC-001 failures whenever a stricter reserve_soc is
set (e.g. GB-BESS-OPS-011) — both UCV-eligible, so this agent should register real UCVs on
exactly those scenarios.
"""

from __future__ import annotations

from gridactionbench.schemas.action import ActionType, AgentActionV1
from gridactionbench.schemas.observation import EnergyObservationV1


class IgnoreMinimumSOCAgent:
    agent_id = "ignore-minimum-soc"
    agent_version = "0.1.0"
    agent_type = "seeded_failure"

    def __init__(self, dt_hours: float):
        self.dt_hours = dt_hours

    def act(self, observation: EnergyObservationV1) -> AgentActionV1:
        battery = observation.battery
        policy = observation.operational_policy
        price = observation.market.reference_price_gbp_mwh

        if price is not None and price > 0 and not policy.temporary_limits.discharge_prohibited:
            candidates = [battery.max_discharge_mw]
            if observation.network.export_headroom_mw is not None:
                candidates.append(observation.network.export_headroom_mw)
            power = max(0.0, min(candidates))  # deliberately no min_soc/reserve_soc floor
            if power > 1e-9:
                return AgentActionV1(action=ActionType.DISCHARGE, power_mw=power)

        return AgentActionV1(action=ActionType.IDLE)
