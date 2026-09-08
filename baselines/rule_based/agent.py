"""RuleBasedAgent — transparent deterministic controller. See master brief §26.

Policy, in priority order:
1. Escalate on any recognised information-sufficiency red flag (missing/stale/conflicting
   SOC telemetry, missing network-headroom telemetry, an implausible quality flag, an
   approval requirement, or the presence of an adversarial injected_field).
2. Otherwise, charge at the boundary-maximal valid power when price is negative and
   charging is not prohibited; discharge at the boundary-maximal valid power (respecting
   reserve_soc) when price is positive and discharging is not prohibited.
3. Otherwise, idle.

Phase 3 fix: this agent did not check `telemetry.field_status.network` at all — a real
gap invisible in the hand-authored initial 20 (where the one scenario testing missing
network headroom, GB-BESS-HUM-019, also happens to have conflicting SOC, which this agent
*did* already check, masking the network-specific gap). The parameterised scenario
generator (gridactionbench/scenarios/generator.py)'s `DATA-MISSING-NETWORK` template
isolates network-missingness without a SOC conflict and caught this immediately — 15 UCVs
out of 300 generated scenarios, all from this one template, all fixed by adding the check
below. See CHANGELOG.md.

Boundary-maximal power is computed by inverting the SOC-transition equations in
docs/suites/gb-bess/SPECIFICATION.md §9.4 — this agent needs its own dt_hours (a real
controller would know its own control-loop timestep) to do so.
"""

from __future__ import annotations

from gridactionbench.schemas.action import ActionType, AgentActionV1, ReasonCode
from gridactionbench.schemas.observation import EnergyObservationV1


class RuleBasedAgent:
    agent_id = "rule-based"
    agent_version = "0.1.0"
    agent_type = "rule_based"

    def __init__(self, dt_hours: float):
        self.dt_hours = dt_hours

    def act(self, observation: EnergyObservationV1) -> AgentActionV1:
        escalation = self._check_information_sufficiency(observation)
        if escalation is not None:
            return escalation

        battery = observation.battery
        policy = observation.operational_policy
        price = observation.market.reference_price_gbp_mwh

        if price is not None and price < 0 and not policy.temporary_limits.charge_prohibited:
            power = self._max_charge_power(observation)
            if power > 1e-9:
                return AgentActionV1(action=ActionType.CHARGE, power_mw=power)

        if price is not None and price > 0 and not policy.temporary_limits.discharge_prohibited:
            power = self._max_discharge_power(observation)
            if power > 1e-9:
                return AgentActionV1(action=ActionType.DISCHARGE, power_mw=power)

        return AgentActionV1(action=ActionType.IDLE)

    def _check_information_sufficiency(self, observation: EnergyObservationV1) -> AgentActionV1 | None:
        telem = observation.telemetry
        if telem.field_status.soc == "missing":
            return AgentActionV1(action=ActionType.ESCALATE, reason_code=ReasonCode.MISSING_CRITICAL_DATA)
        if telem.field_status.soc == "stale":
            return AgentActionV1(action=ActionType.ESCALATE, reason_code=ReasonCode.STALE_CRITICAL_DATA)
        if telem.field_status.soc == "conflicting":
            return AgentActionV1(action=ActionType.ESCALATE, reason_code=ReasonCode.TELEMETRY_CONFLICT)
        if telem.field_status.network == "missing":
            return AgentActionV1(action=ActionType.ESCALATE, reason_code=ReasonCode.MISSING_CRITICAL_DATA)
        if any("implausible" in flag for flag in telem.quality_flags):
            return AgentActionV1(action=ActionType.ESCALATE, reason_code=ReasonCode.IMPLAUSIBLE_TELEMETRY)
        if observation.operational_policy.approval_required:
            return AgentActionV1(action=ActionType.ESCALATE, reason_code=ReasonCode.APPROVAL_REQUIRED)
        if observation.injected_field:
            return AgentActionV1(action=ActionType.ESCALATE, reason_code=ReasonCode.SUSPECTED_ADVERSARIAL_INPUT)
        return None

    def _max_charge_power(self, observation: EnergyObservationV1) -> float:
        battery = observation.battery
        candidates = [battery.max_charge_mw]
        if observation.network.import_headroom_mw is not None:
            candidates.append(observation.network.import_headroom_mw)
        if battery.charge_efficiency > 0 and self.dt_hours > 0:
            capacity_limit = (battery.max_soc - battery.soc) * battery.capacity_mwh / (
                battery.charge_efficiency * self.dt_hours
            )
            candidates.append(capacity_limit)
        return max(0.0, min(candidates))

    def _max_discharge_power(self, observation: EnergyObservationV1) -> float:
        battery = observation.battery
        policy = observation.operational_policy
        floor = max(battery.min_soc, policy.reserve_soc or battery.min_soc)
        candidates = [battery.max_discharge_mw]
        if observation.network.export_headroom_mw is not None:
            candidates.append(observation.network.export_headroom_mw)
        if self.dt_hours > 0:
            energy_limit = (battery.soc - floor) * battery.capacity_mwh * battery.discharge_efficiency / self.dt_hours
            candidates.append(energy_limit)
        return max(0.0, min(candidates))
