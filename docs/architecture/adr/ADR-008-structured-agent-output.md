# ADR-008: Structured Agent Output

**Status:** Proposed

## Context
Master brief §12 requires that free-form agent reasoning never determine deterministic constraint evaluation, and that malformed outputs, schema repairs, and raw output all be recorded.

## Decision
`AgentActionV1` is a strictly validated structured schema (`docs/suites/gb-bess/SPECIFICATION.md` §3). For LLM-backed agents, the runner requests structured output (via provider-native structured/tool-output modes where available) and, on parse failure, applies a bounded, logged repair attempt (e.g. re-prompting once with the validation error) before falling back to recording the response as `schema_valid: false` with the action treated as an implicit ESCALATE-equivalent failure for evaluation purposes — never silently coerced into a best-guess valid action. Raw model output is always retained in the Decision Record regardless of parse outcome.

## Alternatives considered
- **Free-text output with a downstream NLP/regex extraction step** — rejected: reintroduces exactly the ambiguity master brief §12 warns against, and makes "did the agent really mean CHARGE 2MW" a matter of extraction-heuristic quality rather than an unambiguous structured field.
- **Silently defaulting malformed output to IDLE** — rejected: would hide real agent failures (schema non-compliance) behind an artificially safe-looking outcome, undermining both the malformed-output metrics master brief §12 requires and the honest-reporting principle running through the whole methodology (`docs/benchmark/METHODOLOGY.md`).

## Consequences
- Positive: schema-validity and repair-attempt rates become first-class, comparable metrics across agent architectures (an LLM agent that frequently needs schema repair is a real, reportable finding, not noise to be cleaned away).
- Negative: treating unparseable output as an evaluation failure (rather than silently retrying indefinitely) may understate a capable agent's "true" decision quality if its structured-output plumbing is merely unreliable rather than its judgment — mitigated by capping and logging retry attempts distinctly from judgment failures, so the two are reportable separately.
