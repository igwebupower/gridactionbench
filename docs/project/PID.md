# Project Initiation Document (PID)

**Project:** GridActionBench, first suite GB-BESS v0.1
**Status:** Phase 0 — Foundation (target window per master brief: 9-11 September 2026)
**Document status:** Draft

## 1. Purpose

Build a transparent, reproducible experimental framework for discovering how AI agents (and non-AI controllers) behave when making operational decisions for a simulated grid-connected BESS, in a Great Britain electricity-system context, and to publish the resulting evidence openly. See `docs/benchmark/BENCHMARK_CARD.md` for the full scope statement.

## 2. Gate 0 — required answers before technical implementation

### 2.1 "What does this benchmark evaluate that isn't already well covered?"

This question was taken seriously, not rhetorically — see the full research in `docs/research/PRIOR_ART.md`. The honest answer has three parts:

**First, GridActionBench targets a specific, narrow question: single-asset operational-action validity under constraint and uncertainty.** It evaluates whether an agent selects a valid **single-asset operational action** (CHARGE/DISCHARGE/IDLE/ESCALATE for one battery) given physical, network-headroom, operational-policy, and information constraints, with an explicit and equally-weighted focus on recognizing *insufficient information* and escalating appropriately. This is deliberately narrower than grid-wide engineering-workflow benchmarks (which test multi-bus contingency screening, tool selection, and mitigation proposal across a whole network) — the two kinds of evaluation are complementary, not competing answers to the same question.

**Second, GridActionBench is deliberately friction-light.** GB-BESS v0.1 has zero external licensed dependencies by design (`docs/architecture/adr/ADR-003-simulator-abstraction.md`), trading physical fidelity for installability and a low barrier to independent contribution and reproduction — a deliberate, stated trade-off, not an oversight.

**Third, GridActionBench formalizes several concepts general prior art in this space tends to under-specify**: independent, documented versioning of scenario/evaluator/simulator artifacts; a first-class Unrecognised Critical Violation (UCV) metric, gated on an explicit `ucv_eligible` classification per evaluator rather than applied to every "critical" finding uniformly (`docs/suites/gb-bess/EVALUATION_SPEC.md`); and an explicit escalation-quality axis (Appropriate vs. Unnecessary Escalation Rate) that treats "always escalate" as a documented failure mode requiring its own control scenario (`GB-BESS-HUM-020`).

**Fourth: GridActionBench is not a reinforcement-learning training environment.** Sequential grid-control RL environments and their benchmark suites (e.g. Grid2Op and RL2Grid, reviewed in `docs/research/PRIOR_ART.md` §2) train and evaluate policies to maximize long-horizon reward across a simulated network. GridActionBench does not train policies, does not define a reward function, and evaluates any decision-making system — RL policy, rule-based controller, or LLM agent — against fixed, versioned scenarios on constraint adherence, information sufficiency, and escalation, not cumulative reward. See `docs/research/PRIOR_ART.md` §2 for the full comparison, including where the two kinds of evaluation genuinely overlap (episode-mode sequential evaluation, constrained-optimization framing) rather than pretending there is none.

**Self-assessment:** this differentiation is real but should not be overstated. If GB-BESS v0.1's calibration phase (Phase 4) or external domain review (Phase 7) finds the single-asset scope too narrow to produce interesting findings, that would weaken this answer materially, and should be treated as a legitimate reason to reconsider scope — not explained away.

### 2.2 "What specifically makes GB-BESS a Great Britain benchmark rather than a generic battery benchmark using GBP?"

**Revised Phase 0.5, updated Phase 1** — the Phase 0 answer overstated this. Answered in full, with sourced evidence and an explicit benchmark-affecting test, in `docs/suites/gb-bess/GB_SPECIFICITY.md`. Corrected summary: applying the test "if removing a claimed GB-specific feature changes no scenario, evaluator, observation, rule, or parameter distribution, it is probably contextual rather than benchmark-specific" left **two** genuinely benchmark-affecting features after Phase 0.5 — network headroom modeled as dynamically curtailable (grounded in DNO/NESO Active Network Management and Technical Limits, not a generic fixed "grid capacity" abstraction) and negative/volatile reference price treated as a core, not exotic, scenario condition (grounded in Elexon's real half-hourly settlement structure). Phase 1 implementation added a **third**: `SimpleBessSimulator`'s `dt_hours` now actually defaults to `0.5`, the GB half-hourly settlement period, satisfying the condition `GB_CONTEXT.md` itself set for treating this as benchmark-affecting rather than aspirational. The DESNZ/Ofgem battery-connections-queue policy narrative remains contextual, in `docs/suites/gb-bess/GB_CONTEXT.md` — removing it still changes no evaluator, scenario, or schema field in GB-BESS v0.1. This is a narrower, more defensible claim than the Phase 0 draft made, and is explicitly labeled **contextual/structural for two features, implemented for one, not yet data-grounded for any** (no real, licence-confirmed GB dataset is frozen into v0.1 yet) — see `GB_SPECIFICITY.md`'s "Honest self-assessment" for the precise claim boundary.

## 3. Relationship to other initiatives

- **Independence** — GridActionBench runs entirely independently of any single commercial platform; no component requires a proprietary service, and its governance is designed so independent contributors can participate on equal footing (`GOVERNANCE.md`).
- **DESNZ** — GridActionBench may produce evidence relevant to DESNZ's work on AI-enabled clean energy systems (Phase 12 target output, master brief §80). No DESNZ endorsement, government approval, or official benchmark status is claimed.
- **Ofgem** — not positioned as a replacement for regulatory sandboxing; potential relationship is evidentiary input to a sandbox/assurance pipeline, not a substitute for one (master brief §64).

## 4. Governing principle

GridActionBench is not an AI leaderboard looking for a winner. It is a transparent experimental framework for discovering how AI agents behave when their decisions have operational consequences, and it must be capable of showing an AI agent is worse than a simple deterministic controller. See `docs/benchmark/BENCHMARK_CARD.md`.

## 5. Phase 0 deliverables (this document tracks completion against master brief §67)

| Deliverable | Location | Status |
|---|---|---|
| Repository assessment | (delivered in-session; GridActionBench folder was empty, standalone git repo initialized) | Done |
| PID | this document | Done |
| Benchmark Card | `docs/benchmark/BENCHMARK_CARD.md` | Done |
| Prior-art review | `docs/research/PRIOR_ART.md` | Done |
| Benchmark-design review | `docs/research/BENCHMARK_DESIGN_REVIEW.md` | Pending |
| Research questions | `docs/benchmark/BENCHMARK_CARD.md` §"Research questions" | Done |
| Benchmark architecture | `docs/architecture/ARCHITECTURE.md`, `docs/architecture/DOMAIN_MODEL.md` | Done |
| GB-BESS specification | `docs/suites/gb-bess/SPECIFICATION.md` | Done |
| GB specificity analysis | `docs/suites/gb-bess/GB_SPECIFICITY.md` | Done |
| Taxonomy | `docs/suites/gb-bess/SCENARIO_CATALOGUE.md` (family headers) | Done |
| First 20 scenarios | `docs/suites/gb-bess/SCENARIO_CATALOGUE.md` | Done |
| Episode design | `docs/suites/gb-bess/SCENARIO_CATALOGUE.md` §"Episode scenarios" | Done |
| Evaluator catalogue | `docs/suites/gb-bess/EVALUATION_SPEC.md` | Done |
| Assumptions | `docs/project/ASSUMPTIONS.md` | Done |
| Risk register | `docs/project/RISK_REGISTER.md` | Done |
| Threat model | `docs/benchmark/THREAT_MODEL.md` | Done |
| Public/private policy | `docs/benchmark/PUBLIC_PRIVATE_POLICY.md` | Done |
| Contamination policy | `docs/benchmark/CONTAMINATION_POLICY.md` | Done |
| Data strategy | `docs/data/DATA_SOURCES.md`, `docs/data/DATA_PROVENANCE.md` | Done |
| Licensing strategy | `docs/architecture/adr/ADR-013-licensing.md`, `DATA_LICENSES.md` | Done |
| Implementation backlog | `docs/project/BACKLOG.md` | Done |

`docs/research/BENCHMARK_DESIGN_REVIEW.md` and `docs/research/EXPERT_REVIEW_CHECKLIST.md` are the two Phase 0 artifacts not produced in this pass — flagged explicitly rather than silently omitted; see `docs/project/BACKLOG.md` for tracking.

## 6. Non-goals for v0.1

See master brief §84 — not repeated here in full; the short version: no SaaS functionality, no billing/RBAC/SSO, no polished dashboards, no leaderboard UI, no whole-grid simulation, no regulatory certification claim, no production deployment.
