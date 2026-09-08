"""AgentAdapter interface. See docs/architecture/adr/ADR-004-agent-abstraction.md.

Provider-neutral by design — no model provider is imported by this module or by the core
runner (master brief §26).
"""

from __future__ import annotations

from typing import Protocol

from gridactionbench.schemas.action import AgentActionV1
from gridactionbench.schemas.observation import EnergyObservationV1


class AgentAdapter(Protocol):
    agent_id: str
    agent_version: str
    agent_type: str  # e.g. "reference", "rule_based", "llm"

    def act(self, observation: EnergyObservationV1) -> AgentActionV1: ...
