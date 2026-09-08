# ADR-017: Counterfactual Evaluation

**Status:** Proposed

## Context
Master brief §14 requires counterfactual evaluation for selected scenarios, to distinguish "the agent merely failed" from "the agent chose an invalid action when a valid alternative would have achieved most of the objective" — and explicitly warns against generating unnecessary counterfactuals for every scenario.

## Decision
Counterfactual evaluation is an opt-in, per-scenario flag (not a universal runner behaviour): a scenario's specification explicitly lists whether it carries counterfactual evaluation, and if so, a small deterministic set of alternative permitted actions to evaluate (typically IDLE plus the boundary-maximal valid CHARGE/DISCHARGE, per `docs/benchmark/METHODOLOGY.md` §5). When enabled, the Evaluation Engine runs the same Simulator and Evaluators against each alternative action from the same pre-state, and records the comparison in the Decision Record's `counterfactual_results_if_generated` field (`docs/benchmark/SPECIFICATION.md` §7) — never as a separate, disconnected artifact.

## Alternatives considered
- **Always compute counterfactuals for every scenario** — rejected: master brief §14 explicitly forbids this; most PHY/NET golden-boundary scenarios have an obvious, uninteresting counterfactual (IDLE) whose computation would add cost and reporting noise without research value.
- **Compute counterfactuals only post-hoc, in an offline analysis script separate from the benchmark run itself** — rejected: would make counterfactual results non-reproducible as part of the same versioned Run (a later analysis run using a different simulator/evaluator version could silently produce inconsistent counterfactual comparisons) — keeping it inside the same Evaluation Engine call, using the same versioned Simulator/Evaluators as the actual-action evaluation, preserves version consistency.

## Consequences
- Positive: counterfactual results are always evaluated under the identical simulator/evaluator version as the actual action they are compared against, preserving the versioning integrity `docs/benchmark/VERSIONING.md` requires.
- Negative: scenario authors must explicitly decide and justify which scenarios warrant counterfactual evaluation (an added authoring burden), which is accepted as the correct trade-off against master brief §14's explicit "do not generate unnecessary counterfactuals" instruction.
