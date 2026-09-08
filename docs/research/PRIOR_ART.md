# Prior Art Review

**Status:** Draft — Phase 0 foundation research
**Access date for all sources below:** 2026-09-08
**Author:** GridActionBench Lead Benchmark Architect (AI-assisted research; all claims sourced to primary documents, see citations)

This document surveys benchmark methodology directly relevant to GridActionBench: GB-BESS v0.1, so that the project's design choices can be justified against, rather than invented independently of, existing work. The most detailed review — PowerAgentBench — is in a separate document: [`POWERAGENTBENCH_REVIEW.md`](POWERAGENTBENCH_REVIEW.md). This document covers the wider landscape and cross-cutting methodology lessons.

---

## 1. The "PowerAgent" / "Power systems agent" landscape

A important finding of this research: **there are at least two distinct, unaffiliated projects with confusingly similar names**, both directly relevant, neither of which should be conflated with the other:

| Project | Org / Author | Repo | Scope |
|---|---|---|---|
| **PowerAgentBench** (-SS, -Dyn) | Power-Agent GitHub org; Zhang, Pomarico, Mylonas, Foti, Berizzi, Xie et al. (Harvard-affiliated, with Politecnico di Milano and UBITECH co-authors) | `github.com/Power-Agent/PowerAgentBench` | Agentic workflow benchmark: contingency screening, restoration, dynamic model review, using real power-system simulators (PyPSA, PandaPower, MATPOWER, PSS/E) |
| **Power Systems Agent Benchmark** | Sergei Trashchenkov (independent, no institutional affiliation stated) | `github.com/trashchenkov/power-systems-agent-benchmark` | Executable evaluation across 41 task families in 8 domains, using deterministic closed-form/simplified-model evaluators rather than full simulators |

Both are treated as prior art below. The master project brief's "PowerAgentBench" reference is understood to mean the Power-Agent org's benchmark (highest star count under that exact name, and the name the brief uses), reviewed in depth separately. The Trashchenkov project is reviewed here because its executable-evaluation philosophy and public/held-out generator architecture are unusually well-aligned with GridActionBench's own needs, arguably more so on evaluator methodology than PowerAgentBench-SS itself.

Sources:
- [PowerAgentBench-SS (arXiv:2606.18789)](https://arxiv.org/abs/2606.18789) — Mylonas, Foti, Pomarico, Duarte, Zhang, Varvarigos. Submitted 2026-06-17.
- [PowerAgentBench-Dyn (arXiv:2606.20401)](https://arxiv.org/abs/2606.20401) — Zhang, Pomarico, Mylonas, Foti, Berizzi, Xie. Submitted 2026-06-18.
- [Power-Agent GitHub organization](https://github.com/Power-Agent) — 174 followers, Harvard-affiliated; repos: PowerAgentBench (28★), PowerMCP (211★, MIT), PowerSkills (65★), PowerFM (53★, MIT), PowerWF (41★, MIT), power-agent.github.io.
- [Power Systems Agent Benchmark (arXiv:2606.20950v2)](https://arxiv.org/html/2606.20950) — Sergei Trashchenkov. Submitted/revised 2026-07-02. Repo: `github.com/trashchenkov/power-systems-agent-benchmark`. Artifact: Zenodo DOI [10.5281/zenodo.20753046](https://doi.org/10.5281/zenodo.20753046).

### 1.1 Cross-cutting lessons for GridActionBench

**From the Trashchenkov benchmark ("Power Systems Agent Benchmark"):**

1. **"Executable evaluation" is the load-bearing idea** — checking the *consequences* of an action with a program rather than grading the agent's prose account of it. This is precisely GridActionBench's own governing principle ("do not just evaluate what an AI says — evaluate what happens if you let it act"), independently arrived at by both projects, which is reassuring convergent validation rather than something to copy verbatim.
2. **Deterministic surrogates over full simulators, deliberately.** The paper explicitly states *"we do not use these simulators at all"* (referring to pandapower/MATPOWER/OpenDSS/PyPSA/ANDES/PGLib), using compact closed-form/linearized evaluators instead, with an explicit **maturity ladder** (closed-form → engineering model → full simulator → stochastic suite) that lets evaluator fidelity improve without changing the task/solution schema. This directly supports GridActionBench's own choice (master brief §29–30) to start with `SimpleBessSimulator` rather than a power-flow solver, and suggests documenting our own maturity ladder explicitly.
3. **Per-family deterministic held-out generators**, drawn from a private seed, with published acceptance criteria (reference solver solves it; evaluator confirms feasibility; no small perturbation of the reference scores higher). This is a stronger, more falsifiable design than a simple "20% holdout split" and is directly relevant to GridActionBench's own public/private policy (see `docs/benchmark/PUBLIC_PRIVATE_POLICY.md`).
4. **Quality-control via agent disagreement, not just accuracy.** Section 8 of the paper describes finding an evaluator bug (an off-by-one fault-current-indicator error) because *all three* tested agents unanimously and correctly disagreed with the evaluator. This is a genuinely useful pattern GridActionBench should adopt during evaluator validation (master brief §48, Phase 4 calibration): unanimous, high-confidence agent disagreement with an evaluator is itself a signal to re-review the evaluator, not just the agents.
5. **No opaque aggregate score; per-case feasibility flag + normalized score + explicit violation list.** Consistent with the master brief's own §25 prohibition on an opaque overall score.
6. **Explicit reproducibility infrastructure claim** ("every number in this paper can be regenerated from the repository," CI validates evaluators/solvers/runner/generator on every change) — a concrete bar GridActionBench should match or exceed for its own golden/regression test suite.
7. **Acknowledged limitations are stated plainly** — compact, non-industrial-scale cases; unproven reference optimality; a 41-family sample the authors themselves call "statistically fragile." This transparency about limitations is a norm GridActionBench should follow explicitly in its own Benchmark Card, not something to imitate only when convenient.

**From PowerAgentBench (Power-Agent org) — reviewed in full detail separately**, the headline lessons are: real-simulator grounding (PyPSA/PandaPower/MATPOWER/PSS-E) is achievable and valuable, but at the cost of heavier infrastructure and licensed-tool dependencies (PSS/E, DMView); a public-case/hidden-evaluator split works well as an architecture; and its metric taxonomy (evidence-backed recall, false-safe rate, severity regret, action cost, tool-use efficiency) is one of the most directly transferable pieces of prior art for GridActionBench's own UCV and counterfactual metrics. See `POWERAGENTBENCH_REVIEW.md` for the full breakdown and the adopt/adapt/reject analysis.

---

## 2. Grid2Op and RL2Grid

**Status:** Added Phase 0.5 (2026-09-08) — this section was missing from the Phase 0 draft and is added per explicit review feedback that sequential grid-control RL environments are directly relevant prior art this project had not yet examined.

**Sources:**
- [Grid2Op (github.com/rte-france/Grid2Op)](https://github.com/rte-france/Grid2Op) — RTE France (Réseau de Transport d'Électricité). License: Mozilla Public License 2.0. Access date 2026-09-08.
- [Grid2Op project page, LF Energy](https://lfenergy.org/projects/grid2op/) — hosted under the Linux Foundation Energy umbrella. Access date 2026-09-08 (page metadata only retrievable in this pass; substantive content not confirmed beyond the GitHub repository).
- [RL2Grid: Benchmarking Reinforcement Learning in Power Grid Operations (arXiv:2503.23101)](https://arxiv.org/abs/2503.23101) — Marchesini, Donnot, et al. Submitted 2025-03-29, revised 2025-06-20. License: CC BY 4.0. Repository: [github.com/emarche/RL2Grid](https://github.com/emarche/RL2Grid).

**What they are:** Grid2Op is a Gymnasium-compatible reinforcement-learning environment framework, built by RTE France, for sequential power-grid operation — topology switching, redispatching, curtailment, and load-shedding, under full or approximated AC power-flow dynamics, stochastic renewable generation, and contingency events (line disconnections, maintenance, weather-driven overloads). It underpins RTE's "Learning to Run a Power Network" (L2RPN) competition series. RL2Grid is a benchmark suite built on top of Grid2Op that standardizes tasks, state/action spaces, and reward structures across that environment, adds expert-informed heuristics and constrained-MDP safety formulations (load-shedding and thermal-overload constraints), and reports baselines across DQN, PPO, SAC, TD3, and Lagrangian PPO.

**How this differs from GridActionBench, and why the difference is not manufactured:**

Grid2Op/RL2Grid and GridActionBench solve genuinely different problems, not merely differently-branded versions of the same one:

1. **Optimization target.** Grid2Op/RL2Grid train and evaluate policies to *maximize long-horizon operational reward* (survival time, cost, overload avoidance) via reinforcement learning over many episodes of interaction — the environment is a training and evaluation substrate for policy *learning*. GridActionBench does not train anything; it evaluates whatever decision-making system (already trained, hand-coded, or prompted) is handed to it against fixed, versioned scenarios, scored on constraint adherence, information sufficiency, and escalation — not reward maximization. An agent that never touches Grid2Op's reward signal (e.g. a rule-based controller, or an LLM given a single scenario) is a first-class, expected GridActionBench participant; it would be an unusual fit for an RL benchmark built around a Gym `reward()` signal.
2. **Action space and asset scope.** Grid2Op's action space is grid-topology-centric (switch lines, redispatch generators, curtail renewables) across a whole synthetic network; GridActionBench: GB-BESS's action space is four actions (CHARGE/DISCHARGE/IDLE/ESCALATE) for one battery asset. This is a strict subset in ambition, not a competing full-grid model.
3. **What "escalation" and "information sufficiency" mean.** Grid2Op/RL2Grid have no analogue to GridActionBench's ESCALATE action or its DATA/HUM scenario families (stale/missing/conflicting telemetry, appropriate vs. unnecessary escalation) — an RL policy in Grid2Op always acts on whatever observation the environment hands it; there is no first-class "the agent should recognise it doesn't have enough information and refuse to act" concept built into the environment or its reward structure. This is the single clearest non-overlapping area between the two projects and is central to GridActionBench's own research questions (master brief §22).
4. **Adversarial and instruction-following behaviour.** GridActionBench's ADV family (prompt injection, instruction override) has no Grid2Op/RL2Grid analogue — these are RL environments, not natural-language-instructable agents, so "does an adversarial instruction cause an inappropriate action" is not a question their action interface can even pose.
5. **Where the overlap is real, and should not be understated.** Both projects test sequential decision-making under physical/network constraints, both use a versioned, reproducible environment/task structure, and both explicitly measure constraint violation (Grid2Op/RL2Grid via the constrained-MDP safety formulation; GridActionBench via deterministic evaluators). GridActionBench's Mode B (episode evaluation, master brief §4) is a structurally similar idea to a Grid2Op episode, at much smaller scale (5-10 steps vs. RL2Grid's long-horizon episodes) and without a reward-maximization objective. If GridActionBench's episode suite grows substantially in a future version, the overlap with Grid2Op/RL2Grid's territory would grow too, and this document's differentiation claim should be re-examined at that point rather than assumed to hold indefinitely.

**Patterns to adopt or adapt:**
- Grid2Op's Gymnasium-interface convention (`Environment` class with a standard `step`/`reset` API) is a reasonable reference point for GridActionBench's own `SimulatorAdapter`/runner interface (`docs/architecture/ARCHITECTURE.md`) if a future episode-heavy suite wants interoperability with the broader Gym ecosystem — not adopted in v0.1, since GridActionBench's evaluation loop is not itself an RL training loop and does not need Gym-style `reward()` semantics, but worth tracking as a compatibility option.
- RL2Grid's constrained-MDP framing (safety as an explicit constraint on the optimization, not just a post-hoc check) is conceptually adjacent to GridActionBench's "objectives never override constraints" rule (`docs/benchmark/SPECIFICATION.md` §3.3) — independently arrived at, not adopted from RL2Grid, but worth noting as convergent validation.

**Licensing implications:** Grid2Op is MPL 2.0 — compatible with Apache-2.0 consumption in the same way the MIT-licensed PowerMCP/PowerFM/PowerWF repositories are (`docs/architecture/adr/ADR-013-licensing.md`), should a future `SimulatorAdapter` ever wrap it. RL2Grid's paper is CC BY 4.0 (a content licence, not directly applicable to its code, which should be checked separately in its own repository if ever reused). No code from either project has been copied into GridActionBench.

**Interoperability opportunity, not a v0.1 commitment:** a future `SimulatorAdapter` wrapping Grid2Op could, in principle, let GridActionBench evaluate BESS-specific operational actions within a larger simulated network context (e.g., a BESS asset embedded in a Grid2Op environment, with GridActionBench's evaluators applied to just that asset's actions) — this would be a significant undertaking, is not planned for v0.1, and is noted here only as a long-term option alongside the PowerMCP option already tracked in `docs/architecture/adr/ADR-003-simulator-abstraction.md`.

---

## 3. HELM (Holistic Evaluation of Language Models)

**Source:** [Stanford CRFM, HELM (arXiv:2211.09110)](https://arxiv.org/abs/2211.09110); [github.com/stanford-crfm/helm](https://github.com/stanford-crfm/helm); [crfm.stanford.edu/helm](https://crfm.stanford.edu/helm/). Access date 2026-09-08.

HELM's relevance to GridActionBench is architectural, not domain-specific — GridActionBench is not a general-purpose LM benchmark. Two ideas transfer directly:

- **Multi-metric reporting over a single scenario, not a single leaderboard number.** HELM reports up to 7 metrics (accuracy, calibration, robustness, fairness, bias, toxicity, efficiency) per scenario rather than collapsing to one score. This directly validates the master brief's §25 instruction not to create an opaque overall "GridAction Safety Score," and is one of the clearest pieces of external methodological support for that design choice.
- **Explicit, stated incompleteness.** HELM's own framing acknowledges evaluation coverage is partial by design (not every scenario × metric combination is measured — the source notes ~87.5% coverage) rather than claiming universal coverage. GridActionBench's Benchmark Card should adopt the same posture (master brief §47: "explicitly state that GridActionBench is incomplete by design").

**Not adopted:** HELM's scenario taxonomy and model-provider abstraction layer are built for general-purpose LM capability comparison (QA, summarization, toxicity, etc.) and are not meaningfully reusable for an action-validity/consequence benchmark — GridActionBench's taxonomy (PHY/NET/OPS/MKT/DATA/ADV/HUM) is domain-native and should not be forced into HELM's scenario categories.

---

## 4. SWE-bench Verified

**Source:** [OpenAI, "Introducing SWE-bench Verified"](https://openai.com/index/introducing-swe-bench-verified/); [swebench.com/verified.html](https://www.swebench.com/verified.html). Access date 2026-09-08.

SWE-bench Verified is a 500-instance, **human-annotator-filtered** subset of SWE-bench, produced with 93 professional software developers screening the full set for well-scoped unit tests and well-specified issue descriptions, explicitly to fix known problems in the original benchmark: incorrect grading of correct solutions, under-specified problem statements, and overly narrow unit tests.

**Directly relevant lesson:** a benchmark's *first* deliverable is not maximum scenario count — it is a smaller, human-reviewed set proven to be well-posed (unambiguous ground truth, no false negatives against genuinely correct solutions). This is precisely the master brief's own required scenario review ladder (§48: DRAFT → ENGINEERING_REVIEWED → BENCHMARK_REVIEWED → VERIFIED) and its Phase-ordering instruction (§28) to calibrate the benchmark *before* running expensive LLM comparisons. GridActionBench should treat "Verified" scenario status with the same rigor SWE-bench Verified treats instance curation — construct validity work, not volume work.

**Not directly transferable:** SWE-bench's evaluation mechanism (running a held-out unit test suite against a code patch) has no structural analogue in GridActionBench, where correctness is evaluated via deterministic physical/policy constraint checks against a simulator state, not test-pass/fail on code.

---

## 5. MLPerf (MLCommons)

**Source:** [MLCommons, MLPerf Inference Submission Guidelines](https://github.com/mlcommons/inference/blob/master/Submission_Guidelines.md); [MLPerf Training (arXiv:1910.01500)](https://arxiv.org/pdf/1910.01500). Access date 2026-09-08.

MLPerf's relevance is governance and comparability methodology, not task content:

- **Closed vs. Open division.** Closed division submissions must use an equivalent implementation to a published reference implementation, enabling strict apples-to-apples hardware/software comparison; Open division permits different models/approaches, explicitly *not* claimed as comparable to Closed results. This maps directly onto GridActionBench's own **Reference Track vs. Extended Track** design (master brief §41) — the same closed/open distinction, renamed for an agent-evaluation context, with an explicit non-equivalence rule between tracks.
- **A published reference implementation is mandatory**, not optional documentation. GridActionBench's `SimpleBessSimulator`, `RuleBasedAgent`, and baseline evaluators occupy this role and must be maintained with the same seriousness as a scoring artifact, not treated as throwaway example code.
- **Versioned submission rules tied to a frozen benchmark version.** MLPerf ties every published result to a specific benchmark version/ruleset. This directly supports the master brief's §46 requirement that every published GridActionBench result cite benchmark/suite/scenario-set/evaluator-set/simulator versions explicitly rather than an unqualified "Model X scored 97%."

**Not adopted:** MLPerf's hardware-performance submission machinery (latency/throughput scenarios, ECC RAM requirements, etc.) has no analogue here — GridActionBench evaluates decision correctness and consequence, not throughput.

---

## 6. Summary table — patterns adopted / adapted / rejected

| Pattern | Source | Disposition | Where it lands in GridActionBench |
|---|---|---|---|
| Executable/consequence-based evaluation over prose grading | Trashchenkov PSAB; also independently, master brief | **Adopt** | Core architecture (§3, master brief) |
| Deterministic evaluator maturity ladder (closed-form → simulator) | Trashchenkov PSAB | **Adopt** | `docs/architecture/adr/ADR-003-simulator-abstraction.md` |
| Per-family deterministic held-out generator with published acceptance criteria | Trashchenkov PSAB | **Adapt** | `PUBLIC_PRIVATE_POLICY.md` |
| Public case data + hidden evaluator recomputation split | PowerAgentBench-SS | **Adopt** | Core architecture; `PUBLIC_PRIVATE_POLICY.md` |
| Evidence-backed recall / false-safe rate / severity regret metric family | PowerAgentBench (full suite) | **Adapt** | UCV metric design, `EVALUATION_SPEC.md` |
| Real power-system simulator grounding (PyPSA/PandaPower/PSS-E) | PowerAgentBench | **Reject for v0.1** | Explicitly deferred — `SimpleBessSimulator` only (master brief §29–30); noted as a future `SimulatorAdapter` target |
| Gymnasium-style environment interface convention | Grid2Op | **Not adopted for v0.1** | GridActionBench's evaluation loop is not a reward-maximizing RL training loop; tracked as a future compatibility option only |
| Constrained-MDP safety-as-explicit-constraint framing | RL2Grid | **Convergent, not adopted from** | Independently present in `docs/benchmark/SPECIFICATION.md` §3.3 ("objectives never override constraints") |
| Multi-metric, non-aggregated reporting | HELM | **Adopt** | `SCORING.md` (§25 prohibition on opaque score) |
| Explicit, stated benchmark incompleteness | HELM | **Adopt** | `BENCHMARK_CARD.md` |
| Human-reviewed "Verified" subset before scale | SWE-bench Verified | **Adopt** | Scenario review ladder (§48) |
| Calibrate before comparing | SWE-bench Verified (implicitly); master brief §28 explicitly | **Adopt** | Phase ordering (§28, §72) |
| Closed/Open (Reference/Extended) track separation with reference implementation | MLPerf | **Adopt** | `SUBMISSION_RULES.md`, Reference/Extended tracks |
| Versioned rulesets tied to every published number | MLPerf | **Adopt** | `VERSIONING.md` |
| Agent-disagreement-as-evaluator-QC signal | Trashchenkov PSAB | **Adopt** | Phase 4 calibration methodology |
| Hardware/throughput submission machinery | MLPerf | **Reject** | Not applicable |
| General-purpose LM scenario taxonomy | HELM | **Reject** | Domain-native taxonomy (PHY/NET/OPS/MKT/DATA/ADV/HUM) used instead |
| Reward-maximization RL training/evaluation loop | Grid2Op/RL2Grid | **Reject** | GridActionBench evaluates given decision-makers against fixed scenarios; it does not train policies or define a reward function |

### 6.1 Six-way differentiation, stated plainly

- **PowerAgentBench** → agentic power-system engineering/workflow competence (grid-wide contingency screening, dynamic model repair), using real power-flow/dynamic simulators.
- **Grid2Op / RL2Grid** → sequential grid-control reinforcement-learning environments and training/evaluation benchmarks, reward-maximization-oriented, grid-topology-centric action space.
- **HELM** → general-purpose language-model capability evaluation methodology (multi-metric, non-aggregated reporting), not energy-domain.
- **SWE-bench Verified** → human-curated code-fix correctness benchmark; contributes a calibration/curation methodology lesson, not domain content.
- **MLPerf** → hardware/software performance benchmarking governance (Closed/Open division, versioned rulesets); contributes a submission-track methodology lesson, not domain content.
- **GridActionBench** → architecture-neutral evaluation of *operational actions* — constraint adherence, information sufficiency, escalation, adversarial behaviour, and consequence — for any decision-making system (not just RL policies, not just LLM agents), initially instantiated in a GB-BESS single-asset context. No overlap with PowerAgentBench (workflow scope), Grid2Op/RL2Grid (reward-maximization/training scope), HELM (general LM capability), SWE-bench Verified (code-fix domain), or MLPerf (hardware performance) is claimed beyond genuine methodological convergence, documented above and in `docs/research/POWERAGENTBENCH_REVIEW.md` §16, where material overlap exists (episode-mode vs. Grid2Op episodes; deterministic-evaluation vs. Trashchenkov PSAB; track separation vs. MLPerf).

## 7. Interoperability opportunities (not commitments for v0.1)

- **PowerMCP** (MIT-licensed MCP servers for PowerWorld/PSSE/OpenDSS) is a plausible future `SimulatorAdapter` target if GridActionBench ever needs power-flow fidelity beyond `SimpleBessSimulator` — noted in `docs/architecture/adr/ADR-003-simulator-abstraction.md` as a candidate, not built in v0.1.
- **Grid2Op** (MPL 2.0) is a plausible future `SimulatorAdapter` target if GridActionBench ever wants to evaluate a BESS asset embedded within a larger simulated network context — see §2, above. Not built in v0.1.
- Both PowerAgentBench and the Trashchenkov benchmark publish JSON task/solution/result schemas; GridActionBench's own `EnergyObservationV1`/`AgentActionV1`/Decision Record schemas are independently designed for the BESS operational-action domain but should remain loosely translatable to/from these where a future cross-benchmark harness might want to run all three side by side. No shared-schema commitment is made for v0.1.

## 8. Licensing implications

- PowerMCP, PowerFM, PowerWF are MIT-licensed, and Grid2Op is MPL 2.0 — both compatible with GridActionBench's own Apache-2.0 direction (see `docs/architecture/adr/ADR-013-licensing.md`); no code has been copied from any of these repositories into GridActionBench.
- PowerAgentBench's own license was not stated in the reviewed material (`Not stated in provided content`, per the repository fetch) — treat as **all rights reserved / unknown** until explicitly verified; do not copy code or scenario data from it under any circumstance until a license is confirmed.
- The Trashchenkov benchmark's arXiv paper carries an arXiv perpetual non-exclusive distribution license (paper text only); no explicit repository code license was found in the reviewed excerpt — same caution applies.
- RL2Grid's paper is CC BY 4.0; its repository's code licence was not independently checked in this pass and should be verified separately before any reuse.
- No code, scenario data, or evaluator logic from any reviewed project has been reused in GridActionBench. All GridActionBench implementation work is original.

## 9. Research gaps / TODOs

```text
RESEARCH TODO — NETWORK ACCESS REQUIRED (if revisited offline)
- Confirm PowerAgentBench's actual repository LICENSE file (not found in reviewed excerpt).
- Confirm whether PowerMCP's simulator adapters could satisfy a future GridActionBench SimulatorAdapter interface without modification, or would require a wrapper.
- PowerAgent (singular, without "Bench") and PowerSkills were named in the master brief; reviewed here only via the Power-Agent org page summary, not fetched in full — revisit if PowerSkills' agent-instruction design becomes relevant to AgentActionV1 design.
- Confirm RL2Grid's repository code licence directly (only the paper's CC BY 4.0 licence was confirmed in this pass).
- The LF Energy project page for Grid2Op (lfenergy.org/projects/grid2op/) could not be substantively fetched in this pass (metadata only) — the GitHub repository was used as the primary source instead; revisit if LF Energy governance details become relevant.
```
