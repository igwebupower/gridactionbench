# ADR-004: Agent Abstraction

**Status:** Proposed

## Context
Master brief §26 explicitly forbids hard-wiring the benchmark to any specific model provider, and requires that the benchmark evaluate deterministic controllers, optimizers, RL policies, and tool-using agents on equal footing with LLM agents.

## Decision
Define a minimal `AgentAdapter` interface: `act(observation: EnergyObservationV1) -> AgentActionV1`. Reference implementations (`AlwaysIdleAgent`, `AlwaysEscalateAgent`, `RuleBasedAgent`, `LLMStructuredAgent`, and the seeded failure agents — master brief §26-27) all implement this same interface with no privileged access to internals. Provider-specific LLM client logic (OpenAI, Anthropic, etc.) lives in optional adapter modules that implement `LLMStructuredAgent`'s provider-neutral interface, never imported by core runner code directly.

## Alternatives considered
- **Provider-specific runner branches (e.g. `if provider == "openai"` in the core runner)** — rejected: directly contradicts master brief §26 and would make adding/removing provider support a core-code change rather than an isolated adapter addition.
- **Require all agents to be LLMs with a prompt-only interface** — rejected: would make it structurally impossible to evaluate `RuleBasedAgent` or an RL policy on identical footing, defeating master brief §2's explicit multi-architecture requirement.

## Consequences
- Positive: `RuleBasedAgent` and seeded failure agents can be implemented and tested in Phase 1 without any external API dependency, supporting the "calibration before LLM comparison" phase ordering (master brief §28).
- Negative: a maximally thin interface (single `act` call) cannot natively express multi-turn tool-calling agents' internal tool-use loop — such agents must flatten their internal process into a single `AgentActionV1` per observation, with intermediate tool calls logged via the Decision Record's `tool_calls` field rather than being visible to the interface itself. Acceptable for v0.1's single-step/episode-step granularity; revisit if a future suite needs finer-grained multi-turn evaluation within a single decision point.
