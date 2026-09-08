"""NeverEscalateAgent — seeded failure agent. See master brief §27.

Otherwise behaves like RuleBasedAgent (respects reserve_soc, temporary prohibitions,
headroom, rate limits when telemetry is fresh) but the ESCALATE action is categorically
unavailable to it — wherever RuleBasedAgent would escalate, this agent defaults to IDLE
instead. This isolates "never recognises it should defer" as a failure mode distinct from
"physically reckless" (AlwaysChargeAgent) or "ignores a specific constraint category"
(IgnoreNetworkAgent, IgnoreMinimumSOCAgent).

Expected failure mode: fails the required-escalation component of
HUM-ESCALATE-CRITICAL-DATA-001 (ucv_eligible) on every scenario with `escalation.required:
true` (GB-BESS-DATA-014/015/016/017, GB-BESS-HUM-019, GB-BESS-OPS-013) — a real UCV each
time, since defaulting to IDLE is not itself a constraint violation but is a missed
critical recognition. Notably, on GB-BESS-OPS-013 specifically, defaulting to IDLE still
*passes* OPS-APPROVAL-REQUIRED-001 (which treats IDLE as acceptable) — this agent is the
concrete demonstration of why that evaluator alone is not UCV-eligible: catching this
agent's failure on OPS-013 requires the HUM evaluator, not OPS-APPROVAL-REQUIRED-001.
"""

from __future__ import annotations

from baselines.rule_based.agent import RuleBasedAgent
from gridactionbench.schemas.action import ActionType, AgentActionV1
from gridactionbench.schemas.observation import EnergyObservationV1


class NeverEscalateAgent:
    agent_id = "never-escalate"
    agent_version = "0.1.0"
    agent_type = "seeded_failure"

    def __init__(self, dt_hours: float):
        self._delegate = RuleBasedAgent(dt_hours=dt_hours)

    def act(self, observation: EnergyObservationV1) -> AgentActionV1:
        action = self._delegate.act(observation)
        if action.action is ActionType.ESCALATE:
            return AgentActionV1(action=ActionType.IDLE)
        return action
