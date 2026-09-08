# PowerAgentBench Review

**Status:** Draft — Phase 0 mandatory prior-art review (master brief §31)
**Subject:** PowerAgentBench (Power-Agent GitHub org), specifically PowerAgentBench-SS and PowerAgentBench-Dyn
**Access date:** 2026-09-08

## Sources

| Item | Reference | Access date |
|---|---|---|
| PowerAgentBench-SS paper | [arXiv:2606.18789](https://arxiv.org/abs/2606.18789), Mylonas, Foti, Pomarico, Duarte, Zhang, Varvarigos, submitted 2026-06-17 | 2026-09-08 |
| PowerAgentBench-Dyn paper | [arXiv:2606.20401](https://arxiv.org/abs/2606.20401), Zhang, Pomarico, Mylonas, Foti, Berizzi, Xie, submitted 2026-06-18 | 2026-09-08 |
| Organization page | [github.com/Power-Agent](https://github.com/Power-Agent) | 2026-09-08 |
| Repository | [github.com/Power-Agent/PowerAgentBench](https://github.com/Power-Agent/PowerAgentBench) | 2026-09-08 |
| Licence | **Not confirmed.** No LICENSE content was surfaced in the reviewed material. Treat as all-rights-reserved until independently verified against the actual repository LICENSE file. |

Institutional affiliation: authors are associated with Harvard University (School of Engineering and Applied Sciences), Politecnico di Milano (Department of Energy), and UBITECH (Energy Digitalization Group, Athens). The Power-Agent GitHub organization states an affiliation with Harvard and has 174 followers as of the access date.

---

## 1. Research questions

PowerAgentBench's stated gap: existing power-system benchmarks evaluate "numerical solvers, prediction models, or sequential controllers" but do not test whether an LLM-based agent can execute a full **engineering workflow** — inspect a grid case, select tools, call simulators, screen contingencies, propose admissible mitigations, validate its own results, and leave an auditable evidence trail. The research question is therefore about *workflow competence*, not single-shot answer correctness.

## 2. Task structure

Four distinct benchmark levels across two families:

**Steady-state (PowerAgentBench-SS):**
- **Level 1** — N-1 contingency analysis on the IEEE 39-bus case; agent receives case data, a contingency list, and a bounded action space.
- **Level 2** — Agentic N-2 contingency search under a validation-budget constraint; agent submits an evidence-ranked list of contingencies rather than a single answer.
- **Level 3 (RestoreBench)** — AC power-flow convergence restoration via reactive-control maneuvers, capped at a 10-maneuver budget.

**Dynamic (PowerAgentBench-Dyn):**
- **Level 1** — Dynamic model-quality review on a WECC solar PV case: diagnose and repair a dynamic model by adjusting four REECAU1 controller gains within five iterations.
- A second task type, dynamic security risk screening (identifying critical short-circuit contingencies and proposing mitigations), is described at the family level but detailed methodology was not fully retrievable in this pass.

The common shape — bounded action space, explicit iteration/validation budget, evidence-ranked rather than single-answer submission — is a genuinely reusable pattern for GridActionBench's own episode design and for any future scenario where an agent may want to justify a decision with supporting evidence rather than a bare action.

## 3. Agent interface and tool contracts

Agents interact through a **JSON-command adapter** layer over a provider-agnostic interface (`llm_agent_adapter.py` in the repository), with concrete client implementations for Ollama (local) and the OpenAI API. Per-scenario contracts are defined declaratively:

- `actionspace.json` — defines the operating limits / legal action space for a given case.
- `actioncost.json` — defines the cost model for actions taken (used in the action-cost / tool-use-efficiency metrics below).

This is architecturally close to what GridActionBench needs for `EnergyObservationV1` / `AgentActionV1`: a provider-neutral adapter boundary, and declarative, versioned per-scenario contract files rather than contracts baked into agent prompts. GridActionBench's schema versioning approach (master brief §11–12, §44) is consistent with this pattern independently, which is a useful cross-check rather than something to copy structurally.

## 4. Public / hidden architecture

- **Public:** case data in multiple simulator-native formats (PyPSA, PandaPower, MATPOWER), scenario specifications, the action space, and the tool APIs.
- **Hidden:** a hidden evaluator that recomputes steady-state or dynamic validity independently of whatever the agent claims, and returns a structured set of discovery / evidence / safety / mitigation / efficiency / workflow / reliability metrics.

This is the same conceptual split GridActionBench's Scenario Oracle / Agent Observation separation already requires (master brief §9) — ground truth and evaluation logic sit behind a boundary the agent cannot introspect, with the agent's own submission independently re-checked. The PowerAgentBench execution is heavier-weight (multiple simulator backends, licensed PSS/E for dynamics) than GridActionBench needs for v0.1, but the architectural principle transfers directly.

## 5. Simulators

- **PyPSA** — primary steady-state AC/DC power-flow simulator.
- **PandaPower** — alternative steady-state format/solver.
- **MATPOWER** — compatible solver.
- **PSS/E 36.2 + DMView 3.4** — dynamic simulation; both are **licensed, non-free external tools**, which is a material adoption barrier for an open, zero-friction benchmark.

**Implication for GridActionBench:** committing to real power-flow/dynamic simulators from day one would import a licensing and installation-friction cost this project's Phase 0/1 timeline cannot absorb, and the master brief already explicitly rules this out (§29–30: "do not build a power-flow solver," "SimpleBessSimulator is sufficient for the first technical spike"). This review confirms that choice is a deliberate trade-off against a real prior-art benchmark that *did* take the heavier path, not an oversight — GB-BESS v0.1 is intentionally narrower in physical fidelity than PowerAgentBench-SS/Dyn, in exchange for zero external licensing dependencies and a much shorter time-to-working-benchmark. This trade-off should be stated plainly in the Benchmark Card, not hidden.

## 6. Evaluator architecture

Implemented as Python scripts (`evaluate_solution.py`, `benchmark_utils.py`, plus a standalone `restorebench-score` tool for Level 3) that check "base-case and contingency violations after submitted actions" — i.e., deterministic recomputation against simulator output, not an LLM judge. This matches GridActionBench's own §23 requirement (deterministic evaluation first, no LLM-as-judge for physical/policy constraints) and is treated as further validation of that design choice rather than a new idea to import.

## 7. Evidence logging and metrics

**Logging format:** JSONL. Two log streams per model run: `<model>_tool_logs.jsonl` (tool call trace) and `<model>_api_debug.jsonl` (sanitized API debug trace). Per-case results are also emitted as CSV.

**Metric taxonomy** (the single most directly reusable piece of prior art found in this review):

| Metric | What it captures | GridActionBench analogue |
|---|---|---|
| Submitted / evidence-backed / found top-*k* recall | Whether the agent found the right issues, and whether it can back its claims with evidence vs. merely asserting them | Informs UCV design: an agent that reports "no violation" without evidence of having checked is weaker than one that checks and is wrong |
| Evidence rate / unvalidated-claim rate | Fraction of claims backed by retrievable evidence | Directly relevant to `optional_explanation` / evidence fields in `AgentActionV1` — should be logged, not scored subjectively |
| Best severity capture / severity regret | Whether the agent caught the *worst* issue, and how much worse its chosen action is vs. optimal | Maps closely to GridActionBench's counterfactual evaluation (master brief §14) |
| **False-safe rate** / severity-weighted false negatives | Agent claims "safe" when it is not — the single most safety-relevant metric in the whole suite | This is close kin to GridActionBench's **Unrecognised Critical Violation (UCV)** metric (master brief §7), independently designed but conceptually convergent; PowerAgentBench's naming and severity-weighting approach is worth studying further when GridActionBench's UCV severity weighting is formalized in Phase 2 |
| Post-action violation / violation reduction | Net physical effect of the agent's action | Direct analogue of GridActionBench's Simulator pre/post-state comparison |
| Action cost / tool-use efficiency / invalid tool calls | Operational efficiency and malformed-output rate | Analogue of GridActionBench's `schema_valid` / `schema_repairs` / `retry_count` Decision Record fields |

**Adopt for GridActionBench's evaluator catalogue (Phase 2):** explicitly separate "the agent claimed X" from "X is independently verified" in every metric that involves an agent claim (not just escalation) — PowerAgentBench's evidence-rate/unvalidated-claim-rate split is a cleaner way to express this than a single "was the agent right" binary, and should inform how `optional_explanation` and `confidence` fields are scored (logged and reported separately from pass/fail, never used to adjust a hard-constraint verdict).

## 8. Reproducibility, versioning, submission model

- The repository shows 17 commits at review time, with **no formal versioning scheme documented** — a notable gap relative to GridActionBench's own strict versioning requirements (master brief §45–46).
- Level 3 (RestoreBench) uses `uv` with a pinned lockfile for reproducibility; this discipline is not stated as applying repo-wide.
- No explicit public/private holdout *policy document* was found (contrast with the Trashchenkov benchmark's explicit per-family held-out generator, reviewed in `PRIOR_ART.md`) — PowerAgentBench's "hidden evaluator" is architecturally hidden but the rules governing what stays hidden, for how long, and why, were not documented in the reviewed material.

**Implication:** GridActionBench's insistence on explicit, documented versioning (`VERSIONING.md`) and an explicit, justified public/private policy (`PUBLIC_PRIVATE_POLICY.md`, master brief §37–39) is not merely "good practice" in the abstract — it is a concrete area where the most relevant existing prior art appears to be under-specified, and is a legitimate differentiation point rather than a null one.

## 9. Repository organization

```text
PowerAgentBench/
├── cases/              # network data: pypsa/, matpower/, pandapower/
├── benchmarks/
│   ├── steady/level_1,2,3/
│   └── dynamic/level1/
├── scripts/             # entry points: build, convert, evaluate, run baselines/LLM
└── poweragentbench/     # shared library: utils, adapters, clients
```

This is a reasonable, conventional layout; GridActionBench's own required structure (master brief §65) is more elaborate (separating `gridactionbench/` core library from `suites/gb_bess/` scenario data from `baselines/` from `docs/`) because GridActionBench is designed from the outset to support multiple future suites beyond GB-BESS, whereas PowerAgentBench's structure is organized around its four benchmark levels directly. Not a criticism — different scope, different structure is appropriate.

---

## 10. Patterns to adopt

1. Public case data + hidden, independent evaluator recomputation (already in GridActionBench's Oracle/Observation design — confirmed, not new).
2. Deterministic evaluator over LLM-judge for physical/policy correctness (already in GridActionBench §23 — confirmed).
3. JSONL evidence logging per agent run (GridActionBench's Decision Record already specifies this — confirmed).
4. The evidence-backed vs. unvalidated-claim metric split — apply this distinction to GridActionBench's own escalation and confidence-reporting metrics.
5. Declarative, versioned per-scenario action-space/action-cost contract files, separate from the agent prompt.

## 11. Patterns to adapt

1. Multi-simulator-backend architecture (PyPSA/PandaPower/MATPOWER/PSS-E) — adapt down to a single `SimpleBessSimulator` for v0.1, but preserve the *interface* idea (`SimulatorAdapter`) so a PyPSA- or PowerMCP-backed adapter could be added later without redesigning the benchmark core (see `ADR-003-simulator-abstraction.md`).
2. Severity-weighted false-safe metric — adapt into GridActionBench's UCV / High-Confidence UCV design (master brief §7), which is narrower in scope (a boolean-ish critical-violation-plus-non-escalation event) but should borrow the *severity weighting* idea when the metric matures past v0.1's simpler true/false count.

## 12. Patterns not relevant to GridActionBench

1. Licensed, proprietary dynamic-simulation tooling (PSS/E, DMView) — GB-BESS v0.1 is explicitly simulation-only with an open, dependency-light simulator; importing a licensed dependency would contradict both the project's zero-friction goal and its Phase 0/1 timeline.
2. Multi-level "engineering workflow" tasks built around iterative tool-calling budgets for network-wide contingency search — GB-BESS's action space (CHARGE/DISCHARGE/IDLE/ESCALATE on a single BESS asset) is deliberately narrower than grid-wide contingency analysis; PowerAgentBench's workflow-budget mechanics don't map onto a single-asset operational-decision benchmark in any direct way.

## 13. Potential reusable components

None identified for direct reuse in v0.1 — license status is unconfirmed (§ Sources, above), and the components that *are* reusable in spirit (JSONL evidence logs, evidence-backed-claim metrics, action-space contract files) are more valuable as design patterns to re-implement natively in GridActionBench's own schema than as literal imported code, given the domain mismatch (grid-wide power-flow vs. single-asset BESS operational actions).

## 14. Licensing implications

No LICENSE file content was retrieved for `github.com/Power-Agent/PowerAgentBench` in this review pass. **Do not copy code, scenario data, evaluator logic, or schema definitions from this repository into GridActionBench until the license is explicitly confirmed by a maintainer reading the actual LICENSE file in the repository.** MIT-licensed sibling repos in the same org (PowerMCP, PowerFM, PowerWF) do not establish the license of PowerAgentBench itself.

## 15. Interoperability opportunities

- PowerMCP (MIT) is a plausible long-term `SimulatorAdapter` backend if GridActionBench ever needs multi-asset network-level fidelity — not planned for v0.1, tracked as a future option in `ADR-003-simulator-abstraction.md`.
- The evidence-backed-recall / false-safe metric family is a candidate for a future joint methodology note if GridActionBench and PowerAgentBench maintainers ever want to align terminology across benchmarks — not pursued in v0.1; would require direct maintainer contact, out of scope for Phase 0.

## 16. Differentiation from GridActionBench

See `docs/project/PID.md` (§"Why GridActionBench, given PowerAgentBench exists") for the full Gate 0 answer. In summary, drawing only on what this review established as fact:

- PowerAgentBench evaluates **grid-wide, multi-asset, workflow-oriented** engineering tasks (contingency screening across a whole network, dynamic model repair) using real power-system simulators and, for dynamics, licensed tools.
- GridActionBench: GB-BESS evaluates **single-asset, single-decision-point operational actions** (CHARGE/DISCHARGE/IDLE/ESCALATE for one battery) against physical, network-headroom, operational-policy, and information-sufficiency constraints, with an explicit UK/GB regulatory and market context, and an explicit escalation/information-sufficiency axis (§10, §22) that has no direct PowerAgentBench analogue in the reviewed material.
- Neither benchmark's task design is "harder" or "better" in the abstract — they are evaluating structurally different questions (grid-engineering-workflow competence vs. operational-action validity under constraint and uncertainty for a single dispatchable asset), and both can be true prior art without one making the other redundant.
