# Architecture

**Status:** Draft — Phase 0 design, not yet implemented (implementation begins Phase 1)

## Component pipeline

```text
Scenario --> Oracle --> Observation --> Agent --> Action Validator --> Simulator
   --> Evaluation --> Counterfactual Analysis (selected scenarios) --> Decision Record --> Report
```

This mirrors `docs/benchmark/SPECIFICATION.md` §1 exactly; this document describes how each stage maps to a package under `gridactionbench/`.

## Package layout (target, per master brief §65)

```text
gridactionbench/
├── core/         # Scenario, Oracle, DecisionRecord data model classes; run orchestration
├── schemas/       # EnergyObservationV1, AgentActionV1 — versioned, validated schema definitions
├── simulators/    # SimulatorAdapter interface + SimpleBessSimulator implementation
├── evaluators/    # Evaluator interface + one module per catalogue entry (PHY, NET, OPS, DATA, ADV, HUM)
├── scenarios/     # scenario loading, validation, and (Phase 3) template-based generation
├── agents/        # AgentAdapter interface + reference agents (AlwaysIdle, AlwaysEscalate, RuleBased, LLMStructured) + seeded failure agents
├── runners/       # single-step and episode execution orchestration
├── reporting/     # per-dimension scoring, UCV computation, report rendering (docs/benchmark/SCORING.md)
└── provenance/     # git commit, environment, seed capture for Decision Records
```

## Key interfaces

### `SimulatorAdapter`

The simulator boundary is an interface, not a concrete class reference, from day one — see `docs/architecture/adr/ADR-003-simulator-abstraction.md`. `SimpleBessSimulator` is the only implementation shipped in v0.1; the interface exists so a future PyPSA-, PandaPower-, or Grid2Op-backed adapter (see `docs/research/PRIOR_ART.md` §7) could be added later without redesigning the benchmark core, not because multiple simulators are needed now.

```text
SimulatorAdapter:
  step(pre_state, action) -> post_state       # deterministic given (pre_state, action, seed)
  validate_action(pre_state, action) -> ValidationResult   # hard-constraint pre-check (see Action Validator, below)
```

### `AgentAdapter`

Provider-neutral boundary between the benchmark runner and any agent implementation — LLM-backed, rule-based, or otherwise. No provider (OpenAI, Anthropic, Google, etc.) is hard-wired into the core runner; provider-specific adapters are optional, separately maintained implementations of this interface (master brief §26).

```text
AgentAdapter:
  act(observation: EnergyObservationV1) -> AgentActionV1
```

### `Evaluator`

Every evaluator in `docs/suites/gb-bess/EVALUATION_SPEC.md` implements a common interface so the reporting layer can aggregate results uniformly regardless of scenario family.

```text
Evaluator:
  eval_id, version, category, criticality   # static metadata, matches the catalogue spec
  evaluate(pre_state, action, post_state, oracle, observation) -> EvaluationResult (pass|warning|failure, evidence)
```

### Action Validator vs. Simulator — a deliberate separation

The Action Validator rejects hard-constraint-violating actions *before* they reach the simulator; the simulator itself never receives or silently clamps an invalid action (see `docs/suites/gb-bess/SPECIFICATION.md` §9). This means: an invalid action always produces an explicit `EvaluationResult: failure` from the relevant evaluator, and the simulator's own state-transition logic can assume its input action is valid, keeping simulator code simple and its correctness easier to test in isolation (Phase 1 golden tests target the validator and simulator separately for exactly this reason).

## Oracle / Observation separation

Implemented as two distinct data structures produced from the same `Scenario` definition: `Oracle` (full ground truth, visible only to the Evaluation Engine and to scenario-authoring/validation tooling) and `EnergyObservationV1` (the subset/possibly-corrupted view exposed to the `AgentAdapter`). A scenario file (`docs/suites/gb-bess/SCENARIO_CATALOGUE.md` shows the YAML shape) declares both explicitly — the Observation is never mechanically derived from the Oracle by a generic "hide some fields" rule, because DATA-family scenarios specifically need the freedom to make the Observation *wrong*, not merely incomplete (master brief §9).

## Decision Record generation

Every runner invocation (single-step or per-episode-step) assembles one immutable Decision Record (schema in `docs/benchmark/SPECIFICATION.md` §7) as its final act, written to portable JSONL. The `provenance/` package is responsible for populating the reproducibility-critical fields (git commit, seed, environment) so no other package needs to duplicate that logic.

## Episode runner

Mode B (`docs/benchmark/SPECIFICATION.md` §2) is implemented as a thin loop over the Mode A single-step pipeline: `State(t) -> Agent -> Action(t) -> Simulator -> State(t+1)` repeated, with the loop itself responsible for detecting and reporting episode-level behavioural metrics (boundary-margin trend, escalation discrimination across steps — see `docs/suites/gb-bess/SCENARIO_CATALOGUE.md`, episode `failure_signature` fields) that have no meaning at the single-step level. The runner does not require a structurally different core pipeline for episodes — this is intentional (master brief §4: "the architecture must support episodes").

## Reporting layer

Implements `docs/benchmark/SCORING.md`'s per-dimension, non-aggregated reporting format directly from a set of Decision Records — the reporting layer never re-derives evaluation verdicts; it only aggregates and presents verdicts already recorded in the Decision Records it reads. This keeps evaluation logic (which must be trustworthy) separate from presentation logic (which can iterate freely without risk to scoring integrity).

## What is explicitly out of the architecture

No component in this architecture issues commands to, or reads live telemetry from, any real energy asset or operational system — see `docs/architecture/SECURITY.md` for the hard isolation guarantee this architecture is designed to make structurally true, not merely policy-true.
