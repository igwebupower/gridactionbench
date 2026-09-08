# Project Initiation Document (PID)

**Project:** GridActionBench, first suite GB-BESS v0.1
**Status:** Phase 0 — Foundation (target window per master brief: 9-11 September 2026)
**Document status:** Draft

## 1. Purpose

Build a transparent, reproducible experimental framework for discovering how AI agents (and non-AI controllers) behave when making operational decisions for a simulated grid-connected BESS, in a Great Britain electricity-system context, and to publish the resulting evidence openly. See `docs/benchmark/BENCHMARK_CARD.md` for the full scope statement.

## 2. Gate 0 — required answers before technical implementation

### 2.1 "Why should GridActionBench exist if PowerAgentBench already exists?"

This question was taken seriously, not rhetorically — see the full research in `docs/research/PRIOR_ART.md` and `docs/research/POWERAGENTBENCH_REVIEW.md`. The honest answer has three parts:

**First, PowerAgentBench and GridActionBench evaluate structurally different questions.** PowerAgentBench (Power-Agent org: Zhang, Pomarico, Mylonas, Foti, Berizzi, Xie et al.) evaluates whether an LLM agent can execute a **grid-wide engineering workflow** — inspect a network case, select tools, call a real power-flow/dynamic simulator (PyPSA/PandaPower/MATPOWER/PSS-E), screen contingencies across a multi-bus network, and propose mitigations, evaluated on the IEEE 39-bus case and a WECC dynamics case. GridActionBench: GB-BESS evaluates whether an agent selects a valid **single-asset operational action** (CHARGE/DISCHARGE/IDLE/ESCALATE for one battery) given physical, network-headroom, operational-policy, and information constraints, with an explicit and equally-weighted focus on recognizing *insufficient information* and escalating appropriately — an axis that has no direct analogue in the reviewed PowerAgentBench material. These are complementary research questions (engineering-workflow competence vs. operational-action validity under constraint and uncertainty), not competing answers to the same question.

**Second, GridActionBench is deliberately friction-light where PowerAgentBench is not.** PowerAgentBench's dynamic benchmark depends on licensed, proprietary tooling (PSS/E 36.2, DMView 3.4). GridActionBench: GB-BESS v0.1 has zero external licensed dependencies by design (`docs/architecture/adr/ADR-003-simulator-abstraction.md`), trading physical fidelity for installability and a much lower barrier to independent contribution and reproduction — a deliberate, stated trade-off, not an oversight.

**Third, GridActionBench formalizes several concepts this research found under-specified in the closest prior art**: independent, documented versioning of scenario/evaluator/simulator artifacts (PowerAgentBench's repository showed no formal versioning scheme — `docs/research/POWERAGENTBENCH_REVIEW.md` §8); a first-class Unrecognised Critical Violation (UCV) metric, gated on an explicit `ucv_eligible` classification per evaluator rather than applied to every "critical" finding uniformly (`docs/suites/gb-bess/EVALUATION_SPEC.md`); and an explicit escalation-quality axis (Appropriate vs. Unnecessary Escalation Rate) that treats "always escalate" as a documented failure mode requiring its own control scenario (`GB-BESS-HUM-020`).

**Fourth (added Phase 0.5, per explicit review feedback that this comparison was missing): GridActionBench and Grid2Op/RL2Grid are not competing answers to the same question either.** Grid2Op (RTE France) and RL2Grid are Gymnasium-compatible reinforcement-learning environments and training/evaluation benchmarks for sequential, reward-maximizing grid-topology control (switching, redispatch, curtailment) across a simulated network. GridActionBench does not train policies, does not define a reward function, and evaluates any decision-making system — RL policy, rule-based controller, or LLM agent — against fixed, versioned scenarios on constraint adherence, information sufficiency, and escalation, not cumulative reward. Grid2Op/RL2Grid have no analogue to GridActionBench's ESCALATE action, its information-sufficiency (DATA) or adversarial (ADV) scenario families, or its ucv_eligible-gated violation metric. See `docs/research/PRIOR_ART.md` §2 for the full comparison, including where the two projects' territory *does* genuinely overlap (episode-mode sequential evaluation, constrained-optimization framing) rather than pretending there is none.

**Self-assessment:** this differentiation is real but should not be overstated. If GB-BESS v0.1's calibration phase (Phase 4) or external domain review (Phase 7) finds the single-asset scope too narrow to produce interesting findings, that would weaken this answer materially, and should be treated as a legitimate reason to reconsider scope — not explained away.

### 2.2 "What specifically makes GB-BESS a Great Britain benchmark rather than a generic battery benchmark using GBP?"

**Revised Phase 0.5** — the Phase 0 answer overstated this. Answered in full, with sourced evidence and an explicit benchmark-affecting test, in `docs/suites/gb-bess/GB_SPECIFICITY.md`. Corrected summary: applying the test "if removing a claimed GB-specific feature changes no scenario, evaluator, observation, rule, or parameter distribution, it is probably contextual rather than benchmark-specific" leaves **two** genuinely benchmark-affecting features — network headroom modeled as dynamically curtailable (grounded in DNO/NESO Active Network Management and Technical Limits, not a generic fixed "grid capacity" abstraction) and negative/volatile reference price treated as a core, not exotic, scenario condition (grounded in Elexon's real half-hourly settlement structure) — both currently instantiated as scenario-design and terminology choices, not yet as GB-calibrated parameter distributions. The DESNZ/Ofgem battery-connections-queue policy narrative and the GBP-currency/half-hourly-timestep convention, both presented in the Phase 0 draft as GB-specific "features," did **not** survive the test and have been moved to `docs/suites/gb-bess/GB_CONTEXT.md` as contextual/motivational material — removing either changes no evaluator, scenario, or schema field in GB-BESS v0.1. This is a narrower, more defensible claim than the Phase 0 draft made, and is explicitly labeled **contextual and structural GB specificity, not yet data-grounded** (no real, licence-confirmed GB dataset is frozen into v0.1 yet) — see `GB_SPECIFICITY.md`'s "Honest self-assessment" for the precise claim boundary.

## 3. Relationship to other initiatives

- **Enprompta** — GridActionBench runs entirely independently; no component requires Enprompta. See master brief §61. Optional future integration (experiment management, trace visualization) is explicitly out of scope for the open-source MVP.
- **PowerAgentBench** — treated as important prior art and a differentiation reference point (§2.1, above), not a target for forking. No code, scenario, or evaluator logic has been copied from it; its own licence is unconfirmed (`docs/research/POWERAGENTBENCH_REVIEW.md` §14) and must remain so treated until independently verified.
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
| PowerAgentBench review | `docs/research/POWERAGENTBENCH_REVIEW.md` | Done |
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
