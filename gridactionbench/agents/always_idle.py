"""AlwaysIdleAgent — reference agent. See master brief §26."""

from __future__ import annotations

from gridactionbench.schemas.action import ActionType, AgentActionV1
from gridactionbench.schemas.observation import EnergyObservationV1


class AlwaysIdleAgent:
    agent_id = "always-idle"
    agent_version = "0.1.0"
    agent_type = "reference"

    def act(self, observation: EnergyObservationV1) -> AgentActionV1:
        del observation
        return AgentActionV1(action=ActionType.IDLE)
