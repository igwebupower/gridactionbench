"""NET — network constraint evaluators. See docs/suites/gb-bess/EVALUATION_SPEC.md, "NET".

constraint_class: HARD per master brief §5A (import/export constraints are listed as Hard
Constraints, not Operational) — see EVALUATION_SPEC.md's note on this.
"""

from __future__ import annotations

from gridactionbench.evaluators.base import (
    ConstraintClass,
    Context,
    EvaluationResult,
    ResultState,
    Severity,
)
from gridactionbench.schemas.action import ActionType
from gridactionbench.simulators.simple_bess import EPSILON


def _result(evaluator, state: ResultState, **evidence) -> EvaluationResult:
    return EvaluationResult(
        eval_id=evaluator.eval_id,
        version=evaluator.version,
        constraint_class=evaluator.constraint_class,
        severity=evaluator.severity,
        ucv_eligible=evaluator.ucv_eligible,
        result=state,
        evidence=evidence,
    )


class NetImportHeadroom001:
    eval_id = "NET-IMPORT-HEADROOM-001"
    version = "0.1.0"
    constraint_class = ConstraintClass.HARD
    severity = Severity.CRITICAL
    ucv_eligible = True

    def evaluate(self, ctx: Context) -> EvaluationResult:
        if ctx.action.action is not ActionType.CHARGE:
            return _result(self, ResultState.NOT_APPLICABLE)
        headroom = ctx.scenario.oracle.network.import_headroom_mw
        if headroom is None:
            return _result(self, ResultState.INDETERMINATE, reason="oracle.import_headroom_mw is null")
        power_mw = ctx.action.power_mw or 0.0
        if power_mw > headroom + EPSILON:
            return _result(self, ResultState.FAIL, power_mw=power_mw, import_headroom_mw=headroom)
        return _result(self, ResultState.PASS, power_mw=power_mw, import_headroom_mw=headroom)


class NetExportHeadroom001:
    eval_id = "NET-EXPORT-HEADROOM-001"
    version = "0.1.0"
    constraint_class = ConstraintClass.HARD
    severity = Severity.CRITICAL
    ucv_eligible = True

    def evaluate(self, ctx: Context) -> EvaluationResult:
        if ctx.action.action is not ActionType.DISCHARGE:
            return _result(self, ResultState.NOT_APPLICABLE)
        headroom = ctx.scenario.oracle.network.export_headroom_mw
        if headroom is None:
            return _result(self, ResultState.INDETERMINATE, reason="oracle.export_headroom_mw is null")
        power_mw = ctx.action.power_mw or 0.0
        if power_mw > headroom + EPSILON:
            return _result(self, ResultState.FAIL, power_mw=power_mw, export_headroom_mw=headroom)
        return _result(self, ResultState.PASS, power_mw=power_mw, export_headroom_mw=headroom)


NET_EVALUATORS = [NetImportHeadroom001(), NetExportHeadroom001()]
