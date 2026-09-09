# Stress Dimensions — Complexity, Operational Uncertainty, Autonomy Burden

**Status:** New — September 2026 strategic realignment. Formalises three experimental dimensions used to describe *why* a task is hard, as a complement to (not a replacement for) `docs/suites/gb-bess/SCENARIO_TEMPLATES.md`'s existing coverage-dimension tags (`soc_regime`, `network_regime`, `price_regime`, `policy_state`, `information_quality`, `expected_escalation`, `boundary_condition`). See `docs/benchmark/RELIABILITY_BOUNDARY_MODEL.md` for how these dimensions relate to the central research object.

## Why three dimensions, and why not a single difficulty score

A single "difficulty" number would hide exactly the thing this benchmark exists to surface: *which kind* of pressure caused an agent to fail. An agent that fails only as system complexity rises, but is fine under uncertainty, has a different problem than one that fails only under degraded information. Collapsing C, U, and H into one score would repeat the mistake `docs/benchmark/SCORING.md` already refuses to make for evaluation dimensions ("no opaque overall score") — this section applies the same discipline to task difficulty, not only to agent scoring.

**These are task-metadata dimensions, not scoring dimensions.** They describe properties of a Task Family or Instance (`docs/benchmark/TASK_MODEL.md`); they are not themselves evaluators and do not produce a pass/fail verdict. A Run report can slice reliability results *by* C/U/H level (`docs/benchmark/SCORING.md`'s "sliceable by" requirement), which is the entire point of naming them.

## C — System Complexity

Complexity is not asset count alone. It may include: number of assets, number of constraints, dependency structure, interacting objectives, coupled state variables, network/market interaction, and temporal dependence.

**Conceptual progression (not yet a frozen numeric scale — see "What is not yet decided," below):**

```text
C0   single BESS                                  <- GB-BESS v0.1 (current, only implemented level)
C1   PV + BESS
C2   PV + BESS + load
C3   DER + grid/network/market interaction
C4+  portfolio, network, multi-agent environments (future, unscoped)
```

**Where GB-BESS v0.1 sits today:** C0 only, and even within C0 the complexity that exists (network headroom interaction, price interaction, temporary policy restrictions) is represented as independent overlays on one asset, not as interacting sub-systems. `docs/project/PID.md` §2.1's answer to "is single-asset scope too narrow" is directly about this: the honest position is that C0 is a deliberately minimal starting rung of a ladder that this document now names, not a permanent ceiling — see `docs/project/PID.md`, "Scope as a ladder, not a ceiling."

**What is not yet decided:** the exact boundary between C0 and C1 (does adding a single, non-interacting PV forecast count as C1, or only once PV output competes with the battery for the same network headroom?), and whether complexity should eventually be a composite numeric index or remain a categorical rung label. **Do not freeze a numeric complexity score before Phase 4-equivalent calibration evidence exists to justify one** — this mirrors the redesign's own explicit instruction and `docs/project/ASSUMPTIONS.md`'s existing discipline of not inventing thresholds ahead of evidence.

**What must exist regardless of where the numeric question lands:** every Task Family should carry measurable complexity metadata (asset count, constraint count, and a `complexity_rung` tag from the progression above) even before that metadata is used to compute anything. **`complexity_rung` applied — 2026-09-09**, closing that part of this P1 backlog item (`docs/project/GAP_ANALYSIS.md`): every `ScenarioTemplate` and `EpisodeSpec` now carries `complexity_rung: str = "C0"` (a dataclass field distinct from, and additive to, `ScenarioTemplate.coverage`) — uniformly `"C0"`, since GB-BESS v0.1 has no other rung implemented. Asset count and constraint count remain unimplemented — GB-BESS v0.1's asset count is trivially 1 throughout, but a precise per-template constraint-count metric requires a definitional decision (does a policy field set to its inert default, e.g. `approval_required: false`, count as "a constraint" for that template?) not yet made, so it is left as still-open rather than guessed at.

## U — Operational Uncertainty

Operational uncertainty is broader than random noise. Categorical classes, not (yet) an ordered scale:

```text
U0   clean / known state
U1   forecast uncertainty
U2   missing information
U3   stale information
U4   conflicting information
U5   tool or source failure
U6   unexpected event
U7   adversarial or untrusted information
```

**Where GB-BESS v0.1 sits today:** U0, U2, U3, U4, U7 are represented (clean scenarios; `DATA-MISSING-SOC-001`; `DATA-STALE-SOC-001`; `DATA-CONFLICT-SOC-001`; the ADV family). **U1 (forecast uncertainty) and U5 (tool or source failure) are not represented at all** — no scenario currently gives the agent a forecast that can later be checked against what actually happened, and no scenario models a tool call failing (the `AgentAdapter` interface has no tool-call surface to fail in the first place, per `docs/benchmark/CAPABILITY_TAXONOMY.md`'s PERCEIVE section). U6 (unexpected event) is partially represented by the episode family's mid-episode condition changes but is not named as its own category anywhere in the existing scenario catalogue.

**`u_classes` applied — 2026-09-09**, closing this dimension's tagging gap (`docs/project/GAP_ANALYSIS.md` P1): every `ScenarioTemplate` and `EpisodeSpec` carries a `u_classes` tuple (one or more of `U0`-`U7`); `tests/unit/test_capability_tags.py` checks every declared class is a real, spelled member of this set. `DATA-IMPLAUSIBLE-HEADROOM-001`'s template is tagged `U7`, not a new class of its own — an implausible-but-not-necessarily-malicious sensor reading falls under this class's "or untrusted information" half, alongside the ADV family's adversarial half.

**Explicitly not assumed to be ordered by severity.** `U3 is necessarily harder than U2` is not asserted anywhere in this document and must not be assumed by future scenario design — a scenario with stale-but-plausible data (U3) can be easier for an agent to handle correctly than one with missing data that creates strong pressure to fabricate a value (U2), depending on what else is going on in the scenario. Any claim that one U class is harder than another for a given agent architecture is an empirical finding to be measured, not a design assumption to bake in.

## H — Autonomy Burden

**Deliberately named "Autonomy Burden," not "Autonomy Horizon."** Elapsed time or step count alone does not describe autonomous responsibility — a single decision with irreversible, high-value consequences can carry more autonomy burden than ten trivial, easily-reversible ones. Potential components: number of consequential decisions, dependency depth, duration, delayed consequences, reversibility/irreversibility, opportunity for human intervention, number of state transitions, and accumulated exposure to uncertainty.

**Task modes as an H proxy, not a definition:** `docs/benchmark/TASK_MODEL.md`'s Atomic/Sequential/Operational ladder is a coarse, currently-used proxy for increasing H — Atomic tasks have the lowest autonomy burden (one decision, immediately checkable), Operational tasks the highest (many decisions, some effects only visible several steps later, per-episode escalation-discrimination scoring). This proxy is explicitly not the same claim as "more steps = harder" — `docs/benchmark/SPECIFICATION.md`'s existing instruction that episode difficulty is not defined by duration is preserved and generalised here to all of H, not just episode length.

**What is not yet decided:** whether H should eventually become a composite index (weighting reversibility against duration against decision count) or remain a set of separately-reported components. **Not decided in this pass** — recorded as an open question in `docs/project/ASSUMPTIONS.md` (A-14) rather than resolved by assertion.

**`autonomy_burden` applied — 2026-09-09**, as a coarse proxy consistent with the above: every `ScenarioTemplate` carries `autonomy_burden: str = "low"` (Atomic) and every `EpisodeSpec` carries `autonomy_burden: str = "high"` (Operational) — a categorical label, not the composite index the open question above is about.

## How C/U/H metadata should be used once tagged

1. **Slicing, not scoring.** A Run report should be able to show "physical constraint adherence, broken out by C0/C1/... and by U-class," the same way it already breaks UCV out by `constraint_class` (`docs/benchmark/SCORING.md`). This is additive reporting-layer work, not a change to any evaluator's pass/fail logic. **Implemented — 2026-09-09**: `gridactionbench/reporting/report.py`'s `Report.by_capability` slices every existing dimension by `primary_capability`; `ucv_by_u_class`/`ucv_by_complexity_rung`/`ucv_by_autonomy_burden` slice UCV counts by stress dimension for scenarios carrying `Scenario.task_family_tags` (the 20 hand-authored v0.1 scenarios do not, and correctly contribute nothing to these three — see `tests/unit/test_report.py`).
2. **Calibration input, not calibration output.** C/U/H tags on a Task Family are declared by whoever designs it (the same way `ScenarioTemplate.coverage` tags are declared today), not measured empirically from agent results — an agent's *observed* degradation as C/U/H rise is the research finding this metadata makes visible, not a property the metadata itself asserts.
3. **No scenario is retroactively re-tagged to make a result look better.** Any change to a Task Family's declared C/U/H metadata after results exist against it is a scoring-adjacent change requiring the same change-control discipline `docs/project/RISK_REGISTER.md` R-17 already requires for `ucv_eligible` changes.
