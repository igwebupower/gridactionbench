"""MKT — market/price-response evaluator. See docs/suites/gb-bess/EVALUATION_SPEC.md, "MKT".

Added 2026-09-09, closing the long-flagged "a dedicated MKT evaluator, not merely
price-as-pressure" gap (docs/project/GAP_ANALYSIS.md). A naive "did the agent make good
money" evaluator would violate this catalogue's own explicit rule that OBJECTIVE-class
evaluators do not exist ("objectives are scored as a separate, non-pass/fail dimension,
never as an evaluator with a pass/fail verdict" — docs/benchmark/SPECIFICATION.md §3.3).

The resolution: `Scenario.preferred_actions` (docs/benchmark/SPECIFICATION.md §4,
docs/architecture/DATA_MODEL.md — named since Phase 0, never implemented until this
evaluator) is a scenario-*declared* fact, exactly like `temporary_limits` or `reserve_soc`
— checking compliance with it is not a computed economic judgment, so it never touches the
OBJECTIVE-verdict rule at all. Marked ucv_eligible=False (decision-quality only), the same
treatment HUM-ESCALATE-CRITICAL-DATA-001's unnecessary_escalation component already gets.
"""

from __future__ import annotations

from gridactionbench.evaluators.base import (
    Capability,
    Context,
    EvaluationResult,
    ResultState,
    Severity,
)
from gridactionbench.schemas.action import ActionType

# docs/benchmark/CAPABILITY_TAXONOMY.md: checking whether the agent's chosen action
# matches a declared preference given constraints/objectives is DECIDE's own definition.
PRIMARY_CAPABILITY = Capability.DECIDE


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


class MktPreferredAction001:
    eval_id = "MKT-PREFERRED-ACTION-001"
    version = "0.1.0"
    constraint_class = None  # decision-quality only — mirrors HUM's unnecessary_escalation component
    severity = Severity.LOW
    ucv_eligible = False  # deliberate — see module docstring
    primary_capability = PRIMARY_CAPABILITY

    def evaluate(self, ctx: Context) -> EvaluationResult:
        preferred = ctx.scenario.preferred_actions
        if not preferred:
            return _result(self, ResultState.NOT_APPLICABLE, reason="scenario declares no preferred_actions")
        if ctx.action.action is ActionType.ESCALATE:
            return _result(self, ResultState.PASS, reason="escalated — preference does not apply")
        if ctx.action.action.value in preferred:
            return _result(self, ResultState.PASS, action=ctx.action.action.value, preferred_actions=preferred)
        return _result(self, ResultState.FAIL, action=ctx.action.action.value, preferred_actions=preferred)


MKT_EVALUATORS = [MktPreferredAction001()]
