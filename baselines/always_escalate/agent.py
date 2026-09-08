"""AlwaysEscalateAgent — reference agent. See master brief §26.

Must NOT score perfectly on GB-BESS v0.1 — see GB-BESS-HUM-020's Unnecessary Escalation
Rate check (docs/suites/gb-bess/SCENARIO_CATALOGUE.md).
"""

from __future__ import annotations

from gridactionbench.schemas.action import ActionType, AgentActionV1, ReasonCode
from gridactionbench.schemas.observation import EnergyObservationV1


class AlwaysEscalateAgent:
    agent_id = "always-escalate"
    agent_version = "0.1.0"
    agent_type = "reference"

    def act(self, observation: EnergyObservationV1) -> AgentActionV1:
        del observation
        return AgentActionV1(action=ActionType.ESCALATE, reason_code=ReasonCode.UNSUPPORTED_CONDITION)
