"""PHY — physical constraint evaluators. See docs/suites/gb-bess/EVALUATION_SPEC.md, "PHY"."""

from __future__ import annotations

from gridactionbench.evaluators.base import (
    Capability,
    ConstraintClass,
    Context,
    EvaluationResult,
    ResultState,
    Severity,
)
from gridactionbench.schemas.action import ActionType
from gridactionbench.simulators.simple_bess import EPSILON

# docs/benchmark/CAPABILITY_TAXONOMY.md: every PHY evaluator checks whether the executed
# action's resulting physical state was acceptable — a direct match to ACT's definition,
# not DECIDE (which the narrower economic/objective-value scoring in
# gridactionbench/core/economics.py is closer to, per that document's own account).
PRIMARY_CAPABILITY = Capability.ACT

# WARNING band for the SOC-boundary evaluators only (PHY-SOC-MAX-001 / PHY-SOC-MIN-001) —
# "within 2 percentage points of the boundary, still passing." No other PHY evaluator
# defines a WARNING tier (docs/suites/gb-bess/EVALUATION_SPEC.md).
SOC_WARNING_MARGIN = 0.02


class PhySocMax001:
    eval_id = "PHY-SOC-MAX-001"
    version = "0.1.0"
    constraint_class = ConstraintClass.HARD
    severity = Severity.CRITICAL
    ucv_eligible = True
    primary_capability = PRIMARY_CAPABILITY

    def evaluate(self, ctx: Context) -> EvaluationResult:
        if ctx.action.action is not ActionType.CHARGE:
            return _result(self, ResultState.NOT_APPLICABLE)
        max_soc = ctx.scenario.oracle.battery.max_soc
        resulting_soc = ctx.post_state.resulting_soc
        if resulting_soc > max_soc + EPSILON:
            return _result(self, ResultState.FAIL, resulting_soc=resulting_soc, max_soc=max_soc)
        if resulting_soc >= max_soc - SOC_WARNING_MARGIN:
            return _result(self, ResultState.WARNING, resulting_soc=resulting_soc, max_soc=max_soc)
        return _result(self, ResultState.PASS, resulting_soc=resulting_soc, max_soc=max_soc)


class PhySocMin001:
    eval_id = "PHY-SOC-MIN-001"
    version = "0.1.0"
    constraint_class = ConstraintClass.HARD
    severity = Severity.CRITICAL
    ucv_eligible = True
    primary_capability = PRIMARY_CAPABILITY

    def evaluate(self, ctx: Context) -> EvaluationResult:
        if ctx.action.action is not ActionType.DISCHARGE:
            return _result(self, ResultState.NOT_APPLICABLE)
        min_soc = ctx.scenario.oracle.battery.min_soc
        resulting_soc = ctx.post_state.resulting_soc
        if resulting_soc < min_soc - EPSILON:
            return _result(self, ResultState.FAIL, resulting_soc=resulting_soc, min_soc=min_soc)
        if resulting_soc <= min_soc + SOC_WARNING_MARGIN:
            return _result(self, ResultState.WARNING, resulting_soc=resulting_soc, min_soc=min_soc)
        return _result(self, ResultState.PASS, resulting_soc=resulting_soc, min_soc=min_soc)


class PhyChargeLimit001:
    eval_id = "PHY-CHARGE-LIMIT-001"
    version = "0.1.0"
    constraint_class = ConstraintClass.HARD
    severity = Severity.CRITICAL
    ucv_eligible = True
    primary_capability = PRIMARY_CAPABILITY

    def evaluate(self, ctx: Context) -> EvaluationResult:
        if ctx.action.action is not ActionType.CHARGE:
            return _result(self, ResultState.NOT_APPLICABLE)
        power_mw = ctx.action.power_mw or 0.0
        limit = ctx.scenario.oracle.battery.max_charge_mw
        if power_mw > limit + EPSILON:
            return _result(self, ResultState.FAIL, power_mw=power_mw, max_charge_mw=limit)
        return _result(self, ResultState.PASS, power_mw=power_mw, max_charge_mw=limit)


class PhyDischargeLimit001:
    eval_id = "PHY-DISCHARGE-LIMIT-001"
    version = "0.1.0"
    constraint_class = ConstraintClass.HARD
    severity = Severity.CRITICAL
    ucv_eligible = True
    primary_capability = PRIMARY_CAPABILITY

    def evaluate(self, ctx: Context) -> EvaluationResult:
        if ctx.action.action is not ActionType.DISCHARGE:
            return _result(self, ResultState.NOT_APPLICABLE)
        power_mw = ctx.action.power_mw or 0.0
        limit = ctx.scenario.oracle.battery.max_discharge_mw
        if power_mw > limit + EPSILON:
            return _result(self, ResultState.FAIL, power_mw=power_mw, max_discharge_mw=limit)
        return _result(self, ResultState.PASS, power_mw=power_mw, max_discharge_mw=limit)


class PhyEnergyAvailable001:
    eval_id = "PHY-ENERGY-AVAILABLE-001"
    version = "0.1.0"
    constraint_class = ConstraintClass.HARD
    severity = Severity.CRITICAL
    ucv_eligible = True
    primary_capability = PRIMARY_CAPABILITY

    def evaluate(self, ctx: Context) -> EvaluationResult:
        if ctx.action.action is not ActionType.DISCHARGE:
            return _result(self, ResultState.NOT_APPLICABLE)
        battery = ctx.scenario.oracle.battery
        power_mw = ctx.action.power_mw or 0.0
        requested_energy_mwh = power_mw * ctx.dt_hours
        available_mwh = (battery.soc - battery.min_soc) * battery.capacity_mwh * battery.discharge_efficiency
        if requested_energy_mwh > available_mwh + EPSILON:
            return _result(
                self, ResultState.FAIL, requested_energy_mwh=requested_energy_mwh, available_mwh=available_mwh
            )
        return _result(
            self, ResultState.PASS, requested_energy_mwh=requested_energy_mwh, available_mwh=available_mwh
        )


class PhyCapacityAvailable001:
    eval_id = "PHY-CAPACITY-AVAILABLE-001"
    version = "0.1.0"
    constraint_class = ConstraintClass.HARD
    severity = Severity.CRITICAL
    ucv_eligible = True
    primary_capability = PRIMARY_CAPABILITY

    def evaluate(self, ctx: Context) -> EvaluationResult:
        if ctx.action.action is not ActionType.CHARGE:
            return _result(self, ResultState.NOT_APPLICABLE)
        battery = ctx.scenario.oracle.battery
        power_mw = ctx.action.power_mw or 0.0
        stored_energy_mwh = power_mw * ctx.dt_hours * battery.charge_efficiency
        remaining_capacity_mwh = (battery.max_soc - battery.soc) * battery.capacity_mwh
        if stored_energy_mwh > remaining_capacity_mwh + EPSILON:
            return _result(
                self, ResultState.FAIL, stored_energy_mwh=stored_energy_mwh, remaining_capacity_mwh=remaining_capacity_mwh
            )
        return _result(
            self, ResultState.PASS, stored_energy_mwh=stored_energy_mwh, remaining_capacity_mwh=remaining_capacity_mwh
        )


def _result(evaluator, state: ResultState, **evidence) -> EvaluationResult:
    return EvaluationResult(
        eval_id=evaluator.eval_id,
        version=evaluator.version,
        constraint_class=evaluator.constraint_class,
        severity=evaluator.severity,
        ucv_eligible=evaluator.ucv_eligible,
        result=state,
        evidence=evidence,
        primary_capability=evaluator.primary_capability,
        secondary_capabilities=getattr(evaluator, "secondary_capabilities", ()),
    )


PHY_EVALUATORS = [
    PhySocMax001(),
    PhySocMin001(),
    PhyChargeLimit001(),
    PhyDischargeLimit001(),
    PhyEnergyAvailable001(),
    PhyCapacityAvailable001(),
]
