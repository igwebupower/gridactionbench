"""AlwaysChargeAgent — seeded failure agent. See master brief §27.

Expected failure mode: charges at max_charge_mw on every scenario, regardless of SOC,
network headroom, or operational policy. Should trigger PHY-SOC-MAX-001,
PHY-CAPACITY-AVAILABLE-001, NET-IMPORT-HEADROOM-001, and OPS-TEMP-CHARGE-PROHIBITION-001
failures (and resulting UCVs) on every scenario where those constraints are binding for a
large charge request. Never escalates under any circumstance, so also fails every
required-escalation HUM/DATA case.
"""

from __future__ import annotations

from gridactionbench.schemas.action import ActionType, AgentActionV1
from gridactionbench.schemas.observation import EnergyObservationV1


class AlwaysChargeAgent:
    agent_id = "always-charge"
    agent_version = "0.1.0"
    agent_type = "seeded_failure"

    def act(self, observation: EnergyObservationV1) -> AgentActionV1:
        return AgentActionV1(action=ActionType.CHARGE, power_mw=observation.battery.max_charge_mw)
