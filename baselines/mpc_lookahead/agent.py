"""MpcLookaheadAgent — reference agent (added 2026-09-09).

Mirrors RuleBasedAgent's escalation/constraint-respecting logic and boundary-power
computation exactly (baselines/rule_based/agent.py), with one inserted branch before the
greedy fallback: if `market.price_forecast_gbp_mwh` signals a same-direction opportunity
at least `LOOKAHEAD_THRESHOLD` times better than the current price, hold (IDLE) now rather
than lock in the lesser price, reserving capacity for the forecast opportunity.

Built specifically to demonstrate genuine value over RuleBasedAgent on GB-BESS-EP-008
(gridactionbench/scenarios/gb_bess/episodes.py) — a two-peak-price episode designed so
greedy per-step discharge is *provably* worse than holding for the later, much higher
price. RuleBasedAgent's own economics-decision-quality limitation is already disclaimed
(docs/project/ASSUMPTIONS.md A-12: "not claimed to be an economically optimal... trading
strategy") — this agent is the first "stronger, non-LLM comparison point" GridActionBench
has (docs/project/GAP_ANALYSIS.md).

Verified by hand against every scenario that populates a forecast field (only EP-007 and
EP-008 do, as of this pass): behaves identically to RuleBasedAgent on GB-BESS-EP-007 (a
stale forecast pointing the *wrong* direction never looks like a better same-direction
opportunity, so the lookahead branch never triggers there) and on every scenario with no
forecast field at all (the 20 hand-authored scenarios, the 300 generated instances,
GB-BESS-EP-001 through EP-006) — differing from RuleBasedAgent only on GB-BESS-EP-008, by
design. This is not a general-purpose optimal-control solver — it is a single, transparent,
threshold-based lookahead heuristic, deliberately no more sophisticated than the specific
timing tradeoff it was built to solve, matching this project's existing agents' own
transparency discipline (docs/benchmark/METHODOLOGY.md §4: deterministic, inspectable
logic, never an opaque model).
"""

from __future__ import annotations

from gridactionbench.schemas.action import ActionType, AgentActionV1, ReasonCode
from gridactionbench.schemas.observation import EnergyObservationV1

# The forecast opportunity must be at least this many times better than the current price
# to justify holding back now — a deliberately simple, fixed threshold, not a calibrated
# constant (same "illustrative, not validated" status as RuleBasedAgent's own thresholds,
# docs/project/ASSUMPTIONS.md).
LOOKAHEAD_THRESHOLD = 2.0


class MpcLookaheadAgent:
    agent_id = "mpc-lookahead"
    agent_version = "0.1.0"
    agent_type = "optimisation"

    def __init__(self, dt_hours: float):
        self.dt_hours = dt_hours

    def act(self, observation: EnergyObservationV1) -> AgentActionV1:
        escalation = self._check_information_sufficiency(observation)
        if escalation is not None:
            return escalation

        battery = observation.battery
        policy = observation.operational_policy
        price = observation.market.reference_price_gbp_mwh
        forecast = observation.market.price_forecast_gbp_mwh

        if price is not None and forecast is not None:
            if price > 0 and forecast > price * LOOKAHEAD_THRESHOLD:
                # A significantly better discharge opportunity is forecast — hold back now
                # rather than lock in the lesser price.
                return AgentActionV1(action=ActionType.IDLE)
            if price < 0 and forecast < price * LOOKAHEAD_THRESHOLD:
                # Mirror for charging: a significantly better (more negative) charge
                # opportunity is forecast.
                return AgentActionV1(action=ActionType.IDLE)

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
