# Methodology

**Status:** Revised — Phase 0.5. §4 rewritten to document confidence's limitations explicitly and to reflect the Self-Reported High-Confidence UCV rename (`docs/benchmark/SPECIFICATION.md` §8); §9.1 cross-reference added for decision-quality orthogonality.

## 1. What GridActionBench measures

Action validity, information sufficiency, constraint adherence, and consequence — not answer quality, not fluency, not stated reasoning. See `docs/benchmark/SPECIFICATION.md` for the architecture this methodology operationalises.

## 2. Deterministic evaluation is the default and the norm

Every PHY, NET, and OPS evaluator in `docs/suites/gb-bess/EVALUATION_SPEC.md` is a closed-form mathematical check against simulator state, computed the same way every time given the same inputs. No evaluator in this catalogue asks a language model whether an action "looks safe." This is a methodological commitment, not an implementation convenience: LLM-as-judge introduces non-determinism and potential bias precisely where the benchmark most needs a stable, auditable ground truth.

**Where an LLM judge may eventually be used:** only for narrowly scoped, explicitly labeled subjective dimensions (e.g., qualitative rating of an `optional_explanation`'s clarity) that are reported separately and never feed into a pass/fail constraint verdict. None are implemented in v0.1.

## 3. Terminology discipline

See `docs/benchmark/SPECIFICATION.md` §12. In practice this means: a report says "network constraint violation," not "unsafe action," unless the specific failure has been independently validated (domain review + repeated reproduction) to justify that stronger term. This document exists partly to prevent methodology drift under publication pressure — a benchmark that inflates its own findings to sound more alarming is exactly as dishonest as one that downplays them.

## 4. Why the agent's own confidence and reasoning are logged but never authoritative

**Revised this pass — confidence's limitations are now stated explicitly, not implied.** `AgentActionV1.confidence` is a **self-reported, uncalibrated number**: nothing in this benchmark verifies that an agent's stated confidence corresponds to its actual reliability, and no evidence has been collected (as of Phase 0.5) establishing that any evaluated agent's confidence is calibrated at all. This limitation is why the corresponding metric is named **Self-Reported High-Confidence UCV**, not "High-Confidence UCV" — the qualifier is load-bearing, not decorative, and must be preserved in every report, chart, and narrative that cites the metric. It would be a methodological error to write or imply "the agent was 96% likely to be correct" from this field; the only defensible claim is "the agent emitted a confidence value of 0.96 alongside an action that turned out to violate a critical constraint."

`AgentActionV1.confidence` and `optional_explanation` are recorded in every Decision Record and used in exactly two ways: (1) to compute the **Self-Reported High-Confidence UCV** flag (an agent that stated high confidence while wrong is a more actionable finding than one that stated low confidence while wrong — actionable as a *reported pattern*, not as evidence of calibration), and (2) as qualitative evidence for human review. They are never parsed to determine whether a hard or operational constraint passed — that determination is made entirely from the parsed `action` + `power_mw` against simulator/oracle state (master brief §12, §23). Confidence is retained as metadata on every Decision Record, including passing ones, specifically so a future, separate calibration study (comparing stated confidence against actual outcome across many decisions) remains possible without this benchmark itself asserting a calibration claim it has not verified.

See `docs/benchmark/SPECIFICATION.md` §8 for the full UCV/Self-Reported High-Confidence UCV definition, and §9.1 for the related, independent point that a constraint-valid decision's *quality* (including whether an agent's caution level was appropriate) is evaluated separately from constraint validity itself.

## 5. Counterfactual methodology

Where a scenario carries counterfactual evaluation (flagged per-scenario, not universal — see `docs/benchmark/SPECIFICATION.md` §10), the benchmark computes objective value and constraint verdicts for a small, deterministic set of alternative permitted actions (typically: IDLE, and the boundary-maximal valid CHARGE or DISCHARGE) using the same simulator and evaluators applied to the agent's actual action. This produces three distinguishable outcomes for a failed action: (a) no valid action existed that achieved meaningful objective value (the scenario was genuinely hard), (b) a valid alternative existed achieving comparable objective value to the agent's invalid choice (the agent's failure cost little in practice but was still a failure), or (c) a valid alternative existed achieving *most* of the objective value the agent was chasing (the agent's failure was avoidable at near-zero cost). These are reported distinctly, not collapsed into "failed."

## 6. Reference vs. Extended track methodology

See `docs/benchmark/SPECIFICATION.md` §13 and `docs/benchmark/SUBMISSION_RULES.md`. Only Reference Track results are eligible for direct cross-agent comparison in official reporting; Extended Track results are reported with explicit configuration deltas and are never plotted on the same axis as Reference Track results without that distinction being visually and textually unmistakable.

## 7. Stochastic agents require repeated trials

Any agent with non-deterministic output (temperature > 0, sampling-based tool selection, etc.) must be run multiple trials per scenario, with the full distribution (not just the best run) reported. Selecting a single favorable run and presenting it as "the" result is explicitly prohibited (master brief §54, §86).

## 8. Human-review methodology (Phase 7)

External domain reviewers are asked to identify what is *wrong, ambiguous, or misleading* in the benchmark's assumptions, scenarios, thresholds, or metrics — not whether they generally like the project. Every piece of feedback is tracked through Feedback → Issue → Assessment → Accepted/Rejected → Rationale → Change, with rejected feedback's rationale documented, not silently dropped. See `docs/research/EXPERT_REVIEW_CHECKLIST.md` (to be created ahead of Phase 7).

## 9. Construct validity discipline

Every metric name is checked against what it actually measures before publication. If a metric's construct validity is narrow (e.g., `HUM-ESCALATE-CRITICAL-DATA-001` currently has statistical power on only one scenario for the unnecessary-escalation case, per its own documented limitation), the metric name and any accompanying narrative must reflect that narrowness rather than implying broader coverage than exists. See `docs/project/DEFINITION_OF_DONE.md` for the three-level validation requirement (software / domain / construct).
