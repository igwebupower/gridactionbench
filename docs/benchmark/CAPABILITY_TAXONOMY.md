# Capability Taxonomy — Perceive / Decide / Act / Adapt / Escalate

**Status:** New — September 2026 strategic realignment. Formalises five capabilities the benchmark evaluates and states, honestly, which ones GB-BESS v0.1 currently exercises well, exercises thinly, or does not yet exercise at all. See `docs/benchmark/RELIABILITY_BOUNDARY_MODEL.md` for how these capabilities relate to the reliability profile, and `docs/project/GAP_ANALYSIS.md` for the resulting backlog items.

## Why five capabilities, not one "correctness" axis

`docs/benchmark/SPECIFICATION.md` already separates action validity from decision quality (§9.1) and escalation from ordinary action (§6, §9). This taxonomy generalises that existing separation into a named model that also covers perception and adaptation — two things the existing architecture supports evidence for for (Oracle/Observation separation; episode state changes) but had not previously been named as a distinct capability with its own tagging convention. Naming them does not change how any evaluator computes a result; it changes how existing and future evaluators are tagged and reported so a reader can ask "how reliable is this agent architecture at *escalating*, specifically, as distinct from *deciding*" rather than only "how reliable is this agent architecture, overall."

## The five capabilities

### PERCEIVE

Can the agent establish the relevant state of the energy system, including recognising when it cannot?

**What this maps to today:** the Oracle ≠ Observation separation (`docs/benchmark/SPECIFICATION.md` §1, §5) is the architectural foundation this capability is evaluated against. Concretely: `telemetry.field_status`/`age_seconds`/`missing_fields`/`quality_flags` (`docs/suites/gb-bess/SPECIFICATION.md` §2) model missing information, stale information, and conflicting observations; `DATA-IMPLAUSIBLE-HEADROOM-001` models anomaly recognition (a value outside a scenario-declared plausible range); the DATA/HUM evaluator families (`docs/suites/gb-bess/EVALUATION_SPEC.md`) are what actually score this capability today, under the name "information sufficiency."

**What is not yet modelled:** forecast uncertainty (no scenario carries a forecast that can be right or wrong — prices and headroom are presented as point values, not distributions or forecasts with a stated horizon); tool selection (the `AgentAdapter.act()` interface, `ADR-004`, receives one observation and returns one action — an agent cannot choose *which* of several information sources to query, because the interface does not expose a choice); source authority (no scenario currently presents two sources with different declared authority levels — `GB-BESS-DATA-016`'s two conflicting readings are undifferentiated by authority, only by which arrived).

### DECIDE

Can the agent select an appropriate course of action given physical constraints, network constraints, objectives, reserve requirements, operational policy, authority, uncertainty, competing objectives, and future-state consequences?

**What this maps to today:** this is the capability GB-BESS v0.1 is deepest on. The PHY/NET/OPS evaluator families plus economic objective-value scoring (`gridactionbench/core/economics.py`) together score whether a proposed action is constraint-valid and, separately, how good a valid action was relative to the scenario's objective (`docs/benchmark/SPECIFICATION.md` §9.1). Future-state consequences are scored only within a single decision point in Atomic tasks (the immediate resulting SOC/headroom state); across Operational tasks, "future-state consequences" starts to shade into ADAPT, below.

**What is not yet modelled:** genuinely competing objectives within one decision (every current scenario has at most one live economic incentive; no scenario asks an agent to trade off, say, revenue against a stated efficiency objective simultaneously) — tracked as a gap, not fabricated as implemented.

### ACT

Can the agent execute actions that produce acceptable physical, network, operational, and economic consequences? Where possible, the resulting world state is evaluated rather than the persuasiveness of the agent's explanation.

**What this maps to today:** already a first-class design principle, not a new addition — `docs/benchmark/METHODOLOGY.md` §4 and `docs/benchmark/SPECIFICATION.md` §3.4 already state that `optional_explanation` and self-reported `confidence` never determine a pass/fail verdict; verdicts come from `SimpleBessSimulator`'s deterministic state transition and the evaluator suite applied to it. This capability is named here mainly to make explicit what was previously only a scattered set of individual rules: ACT is the capability the whole PHY/NET/OPS/economic-scoring machinery exists to measure.

### ADAPT

Can the agent revise its plan when forecasts change, constraints change, telemetry becomes unavailable, tools fail, previous actions alter future feasible states, asset state deviates from expectation, or an unexpected event occurs?

**What this maps to today, honestly:** thin. Three of the six existing episodes touch this — `GB-BESS-EP-003` (network headroom drops then recovers mid-episode; the `failure_signature` explicitly checks both "used stale headroom" and "stayed overly conservative after recovery"), `GB-BESS-EP-004` (telemetry degrades partway through), and `GB-BESS-EP-005` (a temporary restriction appears then clears). No Atomic task tests ADAPT at all by construction (a single decision point cannot test revision of a prior plan), and none of the existing episodes involve a genuine forecast that turns out wrong, a tool failure, or an asset deviating from its expected physical response — the "changing conditions" tested so far are all *policy or telemetry* changes, not *forecast-was-wrong* or *tool-failed* changes.

**Per the redesign's own framing, this is deliberately named as the primary future task-design focus**, not something to backfill immediately. Tracked in `docs/project/GAP_ANALYSIS.md` and `docs/project/BACKLOG.md` at priority P1/P2, not claimed as already adequately covered.

### ESCALATE

Can the agent recognise when autonomous action is inappropriate — insufficient information, conflicting authoritative sources, insufficient authority, human approval required, uncertainty beyond permitted tolerance, or anomalous system conditions?

**What this maps to today:** the most mature of the five outside DECIDE. `ESCALATE` is a first-class action (`docs/benchmark/SPECIFICATION.md` §6); Appropriate and Unnecessary Escalation Rate are both measured (§9); `GB-BESS-HUM-020` and the generator's `HUM-UNNECESSARY` template exist specifically so an agent that escalates everything does not read as reliable (`docs/benchmark/SPECIFICATION.md` §9's "an agent that always escalates must not achieve a perfect result"). `GB-BESS-EP-006` already tests cross-step escalation *discrimination* (escalating on the steps that need it, not on the ones that don't), which is closer to an Operational-task version of this capability than a purely Atomic one.

**What is not yet modelled:** "insufficient authority" as a condition distinct from "approval required" (`OPS-APPROVAL-REQUIRED-001` models the latter; no scenario models an agent that has full information and physical/policy permission but is operating outside its own declared authority scope — a distinction the redesign's own agent definition treats as separate from missing information).

## Tagging rule

Every evaluator and every Task Family should carry a `primary_capability` tag from `{PERCEIVE, DECIDE, ACT, ADAPT, ESCALATE}`, and may carry secondary tags where a single evaluator genuinely measures more than one (e.g. `HUM-ESCALATE-CRITICAL-DATA-001`'s required-escalation component is primarily ESCALATE but depends on PERCEIVE having correctly identified the triggering condition). **This tagging has not yet been applied to the 18 existing evaluators or 20 existing scenarios** — it is a documentation/metadata addition, tracked as a P1 backlog item (`docs/project/GAP_ANALYSIS.md`), not retrofitted in this pass. The mapping given in each capability section above is a narrative description of where existing evaluators land, not a claim that the formal tag field exists in code yet.

## Relationship to constraint_class

`constraint_class` (HARD/OPERATIONAL/INFORMATION, `docs/suites/gb-bess/EVALUATION_SPEC.md`) and `primary_capability` are independent classifications, like `severity` and `ucv_eligible` already are (`docs/suites/gb-bess/EVALUATION_SPEC.md`'s classification model). A HARD-class evaluator is not automatically a DECIDE-capability evaluator, and an INFORMATION-class evaluator is not automatically a PERCEIVE-capability one — `DATA-IMPLAUSIBLE-HEADROOM-001` is INFORMATION-class but arguably tests PERCEIVE (did the agent recognise an implausible value) more than it tests the DECIDE capability a NET-class evaluator would. Each evaluator's capability tag should be assigned on its own merits when the tagging work above is done, not derived mechanically from `constraint_class`.
