"""Action Validator.

Per docs/suites/gb-bess/SPECIFICATION.md §9.9 and docs/architecture/ARCHITECTURE.md: the
Action Validator determines whether an action is HARD-constraint-valid, which is what
would gate simulator execution in an episode/live context (the simulator itself never
receives or clamps an invalid action). In Mode A (single-step, the only mode this Phase 1
spike implements), this distinction has no forward-state consequence — there is no next
step to gate — but the validity determination itself is still made and recorded, both for
correctness of the Decision Record and so the episode runner (not yet implemented) can
reuse this exact logic unchanged in a future phase.

This module does not duplicate evaluator logic: it derives validity from the HARD-class
results the Evaluation Engine already computed, rather than recomputing constraint checks
independently — a second, divergent implementation of the same checks would be a bug
waiting to happen.
"""

from __future__ import annotations

from gridactionbench.evaluators.base import ConstraintClass, EvaluationResult, ResultState


def is_hard_constraint_valid(results: list[EvaluationResult]) -> bool:
    """True iff no HARD-class evaluator returned FAIL."""
    return not any(r.constraint_class is ConstraintClass.HARD and r.result is ResultState.FAIL for r in results)
