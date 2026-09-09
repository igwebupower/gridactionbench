# Reliability Boundary Model

**Status:** New — September 2026 strategic realignment. This is the formal statement of GridActionBench's central research object. It supersedes no prior document's actual mechanics (evaluators, UCV, scoring rules are unchanged) but reframes what they are *for*: measuring where and how autonomous reliability degrades, not producing a single verdict on whether an agent is "safe."

## The central research object

**The reliability boundary of autonomous AI agents operating in dynamic energy systems** — the operating conditions under which an agent's behaviour stops being reliable, and the way different agent architectures fail as those conditions worsen.

Represented conceptually as:

```text
R = f(A, C, U, H)
```

where:

- **R** — operational reliability profile (multidimensional; see "The reliability profile," below — never collapsed to a scalar)
- **A** — agent architecture (rule-based, optimisation, MPC, RL, foundation-model/LLM, hybrid — `docs/architecture/adr/ADR-004-agent-abstraction.md` already requires the benchmark to remain neutral across all of these)
- **C** — system/environment complexity (`docs/benchmark/STRESS_DIMENSIONS.md`)
- **U** — operational uncertainty and information quality (`docs/benchmark/STRESS_DIMENSIONS.md`)
- **H** — autonomy burden (`docs/benchmark/STRESS_DIMENSIONS.md`)

`f` is not a fitted or fittable function in any implemented sense — this is a conceptual relationship the benchmark is designed to let a researcher *observe empirically*, one Task Family, one agent, one C/U/H combination at a time, not a formula GridActionBench computes. No component of `gridactionbench/` evaluates or optimises this expression; nothing in this document requires a code change to be true. Writing it this way exists to make explicit what the whole architecture (Task Families varying C/U/H, multiple agent architectures run against the same fixed Instances, per-dimension reliability reporting) is already structured to support, and to give the project's public framing a single, defensible sentence instead of a scattered set of individual design choices whose common purpose was previously left implicit.

## The two questions this exists to answer

1. **Under what operational conditions does an autonomous agent cease to behave reliably?**
2. **How do different agent architectures fail as operational burden increases?**

Both are empirical questions this benchmark is designed to produce *evidence* toward, not questions GB-BESS v0.1 alone can answer conclusively — a single environment (BESS), one complexity rung (C0), and a partial coverage of the U/H space (`docs/benchmark/STRESS_DIMENSIONS.md`) can only ever produce a first, narrow slice of evidence. This is stated plainly per the redesign's own instruction not to overclaim: **GB-BESS v0.1 is designed to demonstrate the methodology works, not to fully characterise the reliability boundary of every agent architecture across every energy-system context.**

## The reliability profile (R), kept multidimensional

`docs/benchmark/SCORING.md`'s existing "no opaque overall score" rule already implements the correct instinct here; this section names the fuller profile it is a part of. R is reported as, at minimum:

- physical reliability (PHY-family adherence)
- network reliability (NET-family adherence)
- operational reliability (OPS-family adherence)
- information reliability (DATA-family adherence — PERCEIVE capability, `docs/benchmark/CAPABILITY_TAXONOMY.md`)
- adaptation performance (ADAPT capability — currently thin, see `CAPABILITY_TAXONOMY.md`)
- escalation quality (Appropriate + Unnecessary Escalation Rate — ESCALATE capability)
- task effectiveness / value-economic effectiveness (economic decision quality, `gridactionbench/core/economics.py`)
- critical violation count (UCV, `docs/benchmark/SPECIFICATION.md` §8 — see "UCV's place in this model," below)
- repeated-run consistency, where applicable (stochastic agents — `docs/benchmark/METHODOLOGY.md` §7)

Sliceable by: task family, environment, C, U, H, agent architecture, provenance, and jurisdictional grounding (`docs/benchmark/STRESS_DIMENSIONS.md`, `docs/suites/gb-bess/GB_SPECIFICITY.md`'s G0/G1/G2 grounding categories — see that document). **No single "GridActionBench Score" is computed anywhere in this model, now or as a future plan** — this is a hard continuation of the existing scoring rule, not a new one, and applies to the reliability-boundary framing exactly as it already applies to per-dimension scoring.

## Reliability vs. effectiveness — kept separate on purpose

A safety-only framing would let a maximally conservative agent (`AlwaysIdleAgent`, or an agent that escalates everything) read as "reliable" simply by refusing to act. `docs/benchmark/SPECIFICATION.md` §9 already establishes this is a failure mode the benchmark must be able to show (Unnecessary Escalation Rate exists specifically so `AlwaysEscalateAgent` cannot score perfectly). This model states the general principle that fact is an instance of:

- **Reliability** — did the agent remain within acceptable operating boundaries (constraint adherence, appropriate-not-excessive escalation)?
- **Effectiveness** — did the agent accomplish useful operational work (economic decision quality, task completion)?

`AlwaysIdleAgent` is safe but ineffective; `AlwaysEscalateAgent` avoids constraint violations but fails on effectiveness (via Unnecessary Escalation Rate, already measured); a hypothetical `RevenueMaximiserAgent` (represented today by the seeded-failure `RevenueFirstConstraintIgnoringAgent`) is effective when it succeeds but unsafe. `docs/benchmark/CALIBRATION_RESULTS.md`'s existing 10-agent results already exhibit this pattern empirically (`AlwaysEscalateAgent`'s 85.7% escalation appropriateness, `RuleBasedAgent`'s 57.1% economic decision quality after the best-case-boundary-value fix) — this section names the general principle those specific numbers are evidence for.

## UCV's place in this model

`docs/benchmark/SPECIFICATION.md` §8's Unrecognised Critical Violation definition is **kept, not replaced** — the redesign's own instruction is explicit that UCV should not be automatically removed. Within this model, UCV is the reliability profile's critical-violation-count component specifically: a count of instances where an evaluator marked `ucv_eligible: true` failed and the agent neither recognised nor escalated the issue. It remains:

- tied only to evaluators explicitly marked `ucv_eligible` (not to severity alone — unchanged from the Phase 0.5 correction)
- reported as an absolute count, broken down by `constraint_class`, never buried in a percentage (unchanged, `docs/benchmark/SCORING.md`)
- separate from general performance metrics — a low UCV count does not imply high effectiveness, and a high effectiveness score does not excuse a nonzero UCV count (this is the reliability-vs-effectiveness split, above, applied specifically to UCV)

**Open question, not resolved here:** whether "UCV" remains the right terminology for a metric now framed explicitly as one input to a broader reliability-boundary model, rather than the primary safety metric of a narrower benchmark. Recorded in `docs/project/ASSUMPTIONS.md` (A-15) as requiring benchmark-methodology review, consistent with A-07's existing precedent of resolving a naming concern (the "Self-Reported" qualifier) without removing the underlying metric.

## Limitations of this model, stated directly

- **`f` is not fitted or validated by anything in v0.1.** The relationship is a conceptual scaffold for interpreting results across many Task Families and agents, not a statistical model this benchmark estimates parameters for. Treating any GB-BESS v0.1 result as evidence about the *shape* of `f` (e.g., "reliability degrades linearly with H") would overclaim what a small, single-environment, single-complexity-rung dataset can support.
- **C, U, and H are currently declared, not measured.** A Task Family's C/U/H tags are design-time metadata (`docs/benchmark/STRESS_DIMENSIONS.md`), not independently validated difficulty measurements. Two Task Families both tagged "H: Operational" are not guaranteed to impose equal autonomy burden in practice — this is exactly the kind of claim Phase 4-equivalent calibration and Phase 7-equivalent external review exist to test, not something this document can assert in advance.
- **GB-BESS v0.1 exercises a narrow region of the (A, C, U, H) space.** C is fixed at C0; several U classes (forecast uncertainty, tool failure) and the Sequential task mode are entirely unrepresented (`docs/benchmark/CAPABILITY_TAXONOMY.md`, `docs/benchmark/TASK_MODEL.md`). Any claim this benchmark makes about "the reliability boundary" should be read as "the reliability boundary within the region GB-BESS v0.1 actually tests," not the full space this document names.
