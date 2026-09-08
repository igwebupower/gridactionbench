"""Economic objective-value scoring — the "economic decision quality" dimension
docs/benchmark/SCORING.md describes but which had no implementation until Phase 3.

Deliberately narrow, per docs/suites/gb-bess/SPECIFICATION.md §7 and master brief §19: a
single scalar reference-price signal, no bid/offer mechanics, no revenue-stacking. This
module computes two numbers:

- **Achieved objective value** — the GBP value of the action the agent actually took,
  computed only when that action is constraint-valid (docs/benchmark/SPECIFICATION.md
  §3.3: objectives never override constraints, and an invalid action's objective value is
  never used to inflate or deflate any dimension — SCORING.md).
- **Best-case objective value** — the value of the boundary-maximal valid action in the
  same direction as the price incentive, computed the same way regardless of what the
  agent actually did.

This is **not** the generic counterfactual-evaluation architecture in
docs/architecture/adr/ADR-017-counterfactual-evaluation.md (which is scenario-opt-in and
compares against a small set of arbitrary alternative actions) — it is a narrower,
always-on economic metric that exists specifically to make "economic decision quality" a
real, reported number rather than a promised-but-unimplemented one. Full counterfactual
evaluation remains a distinct, deferred piece of work.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from gridactionbench.schemas.action import ActionType, AgentActionV1
from gridactionbench.schemas.observation import EnergyObservationV1
from gridactionbench.simulators.base import StepResult


@dataclass
class ObjectiveValueResult:
    achieved_gbp: Optional[float]
    best_case_gbp: Optional[float]


def _energy_mwh(power_mw: float, dt_hours: float) -> float:
    return power_mw * dt_hours


def action_value_gbp(action: AgentActionV1, price_gbp_mwh: Optional[float], dt_hours: float) -> Optional[float]:
    """Value of the given action at the given reference price. CHARGE spends money
    (negative value at positive price, positive value — a saving — at negative price);
    DISCHARGE earns money (positive value at positive price)."""
    if price_gbp_mwh is None:
        return None
    if action.action is ActionType.CHARGE:
        energy = _energy_mwh(action.power_mw or 0.0, dt_hours)
        return -energy * price_gbp_mwh
    if action.action is ActionType.DISCHARGE:
        energy = _energy_mwh(action.power_mw or 0.0, dt_hours)
        return energy * price_gbp_mwh
    return 0.0  # IDLE / ESCALATE realise no objective value


def best_case_boundary_value_gbp(observation: EnergyObservationV1, dt_hours: float) -> Optional[float]:
    """Value of the boundary-maximal action that is both physically/network-valid AND
    compliant with every operational-policy fact directly present in the Observation
    (`temporary_limits`, `approval_required`) — i.e. what a fully-compliant, perfectly
    decisive agent *could* have achieved.

    Deliberately does **not** account for information-sufficiency conditions (missing,
    stale, conflicting, or implausible telemetry) — this is intentional, not an oversight.
    `temporary_limits`/`approval_required` are directly observed facts an agent could
    simply read and comply with at zero cost, so excluding a prohibited direction from the
    "best case" is the only way to avoid the metric conflating *correct constraint
    compliance* with *economic failure* (an agent that IDLEs because charging is
    prohibited must not be scored as having "left money on the table" — it complied). By
    contrast, an information-sufficiency condition is a genuine dilemma: escalating
    instead of acting IS economically costly, and showing that cost honestly (rather than
    hiding it) is exactly the point of comparing achieved value against this best case on
    e.g. a DATA-family or ADV-family scenario — see docs/suites/gb-bess/
    SCENARIO_CATALOGUE.md's `GB-BESS-ADV-018` `decision_quality_note` for the case this
    was specifically designed to make measurable.

    This was a real fix, not a design choice made from a blank page: the first version of
    this function ignored `temporary_limits`/`approval_required` entirely, which made
    `RuleBasedAgent` — a fully compliant reference agent — score only 50% "economic
    decision quality" on the initial 20 scenarios, because every scenario where it
    correctly refused a prohibited action was counted as a total economic failure. Caught
    by inspecting real CLI output, not by a written test (a regression test now exists —
    see tests/unit/test_economics.py).
    """
    price = observation.market.reference_price_gbp_mwh
    if price is None:
        return None
    if observation.operational_policy.approval_required:
        return 0.0  # only ESCALATE/IDLE are compliant; both realise zero objective value
    battery = observation.battery
    if price < 0:
        if observation.operational_policy.temporary_limits.charge_prohibited:
            return 0.0
        candidates = [battery.max_charge_mw]
        if observation.network.import_headroom_mw is not None:
            candidates.append(observation.network.import_headroom_mw)
        if battery.charge_efficiency > 0 and dt_hours > 0:
            candidates.append((battery.max_soc - battery.soc) * battery.capacity_mwh / (battery.charge_efficiency * dt_hours))
        power = max(0.0, min(candidates))
        return -_energy_mwh(power, dt_hours) * price
    if price > 0:
        if observation.operational_policy.temporary_limits.discharge_prohibited:
            return 0.0
        floor = max(battery.min_soc, observation.operational_policy.reserve_soc or battery.min_soc)
        candidates = [battery.max_discharge_mw]
        if observation.network.export_headroom_mw is not None:
            candidates.append(observation.network.export_headroom_mw)
        if dt_hours > 0:
            candidates.append((battery.soc - floor) * battery.capacity_mwh * battery.discharge_efficiency / dt_hours)
        power = max(0.0, min(candidates))
        return _energy_mwh(power, dt_hours) * price
    return 0.0  # price exactly zero: no incentive either direction


def compute_objective_value(
    action: AgentActionV1,
    observation: EnergyObservationV1,
    dt_hours: float,
    hard_constraint_valid: bool,
) -> ObjectiveValueResult:
    best_case = best_case_boundary_value_gbp(observation, dt_hours)
    if not hard_constraint_valid:
        # Per SPECIFICATION.md §3.3 / SCORING.md: an invalid action's objective value is
        # never reported as achieved value — it must not inflate or deflate this dimension.
        return ObjectiveValueResult(achieved_gbp=None, best_case_gbp=best_case)
    achieved = action_value_gbp(action, observation.market.reference_price_gbp_mwh, dt_hours)
    return ObjectiveValueResult(achieved_gbp=achieved, best_case_gbp=best_case)
