# ADR-016: Episode Architecture

**Status:** Proposed

## Context
Master brief §4 requires the architecture to support Mode B (episodes) even though v0.1 needs only a small validated episode set, and explicitly requires this without collapsing the single-step and episode pipelines into separate, divergent implementations.

## Decision
The episode runner is a thin loop over the existing Mode A single-step pipeline (`docs/architecture/ARCHITECTURE.md`, "Episode runner"): `State(t) -> Agent -> Action(t) -> Simulator -> State(t+1)`, repeated, with per-step Decision Records generated exactly as in Mode A, plus an additional episode-level aggregation pass that computes behavioural metrics with no single-step analogue (boundary-margin trend, cross-step escalation discrimination — see the `failure_signature` fields in `docs/suites/gb-bess/SCENARIO_CATALOGUE.md`'s episode entries). No separate `EpisodeAgent` interface exists — the same `AgentAdapter` interface serves both modes; an episode simply calls it repeatedly, optionally passing prior-step context if the agent implementation chooses to retain it (statelessness across steps is an agent-implementation choice, not a runner requirement).

## Alternatives considered
- **A structurally distinct episode pipeline with its own Oracle/Observation/Evaluation classes** — rejected: would duplicate most of the single-step machinery for no clear benefit, and would risk the single-step and episode evaluation logic silently drifting apart over time (e.g. a PHY evaluator bugfix applied to one path but not the other).
- **Require all agents to be explicitly stateful/session-aware to participate in episodes** — rejected: would exclude memoryless agents (like `RuleBasedAgent`) from episode evaluation, when testing whether a memoryless agent exhibits emergent bad behaviour over a sequence (e.g. repeatedly running right up to a boundary every step, EP-001) is itself a legitimate and interesting episode-mode research question.

## Consequences
- Positive: single-step and episode evaluation share one evaluator codebase, one Decision Record schema, and one versioning scheme — no risk of the two modes' scoring logic diverging silently.
- Negative: episode-level behavioural metrics (boundary-margin trend, etc.) are a second, distinct metrics layer that must be specified and validated on its own (Phase 2/4 work) — they are not simply "the same evaluators, run more times."
