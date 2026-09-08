# ADR-003: Simulator Abstraction

**Status:** Proposed

## Context
Master brief §29-30 mandates `SimpleBessSimulator` for v0.1 and explicitly forbids building a power-flow solver, while also asking for a generic simulator interface anticipating future adapters (pandapower, OpenDSS, PowerFactory, GridLAB-D). Prior art review (`docs/research/PRIOR_ART.md` §1.1, item 2) found that the most methodologically aligned prior work (the Trashchenkov "Power Systems Agent Benchmark") explicitly uses deterministic surrogate evaluators rather than real simulators, with a documented "maturity ladder" for upgrading fidelity later without changing task/solution schemas — direct external validation for this approach.

## Decision
Define a `SimulatorAdapter` interface (`docs/architecture/ARCHITECTURE.md`) with exactly two methods (`step`, `validate_action`), and ship exactly one implementation, `SimpleBessSimulator`, in v0.1: SOC transition, charge/discharge efficiency, min/max SOC, max charge/discharge power, import/export headroom, deterministic given `(pre_state, action, seed)`. No power-flow solver, no multi-asset network topology.

## Alternatives considered
- **Wrap an existing power-flow library (pandapower) even for a single-asset SOC model** — rejected: adds a heavy dependency and installation friction for no benchmark-relevant fidelity gain at the single-BESS-asset scope of v0.1; directly contradicts master brief §30's explicit instruction.
- **No abstraction at all — hard-code `SimpleBessSimulator` calls throughout the core** — rejected: would require a breaking rewrite of the runner/evaluator code to ever add a second simulator backend, and provides no near-term benefit large enough to justify skipping a two-method interface.

## Consequences
- Positive: matches validated prior-art practice; keeps v0.1 dependency-light and installable in minutes, supporting the Phase 1 timeline; leaves a clean seam for a future PyPSA/PandaPower/PowerMCP/Grid2Op-backed adapter (`docs/research/PRIOR_ART.md` §7) without redesign.
- Negative: `SimpleBessSimulator`'s physical fidelity is materially lower than PowerAgentBench's real-simulator-backed approach (`docs/research/POWERAGENTBENCH_REVIEW.md` §5) — this must be stated plainly in the Benchmark Card as a scope limitation, not hidden.
