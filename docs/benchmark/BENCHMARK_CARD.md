# Benchmark Card — GridActionBench

**Benchmark:** GridActionBench
**First suite:** GB-BESS v0.1 (draft, unreleased)
**Status:** Phase 0 — specification and research, no released results yet
**Last updated:** 2026-09-08

This card follows the spirit of model/dataset cards (e.g., Mitchell et al., "Model Cards for Model Reporting"; Gebru et al., "Datasheets for Datasets") applied to a benchmark rather than a model or dataset.

---

## Purpose

GridActionBench evaluates whether an AI agent (or any decision-making system — LLM agent, rule-based controller, optimizer, RL policy, hybrid, tool-using agent) **selects a valid and appropriate operational action** given what it knows, what it does not know, the constraints governing the system, and the consequences of that action. The governing principle: *do not just evaluate what an AI says — evaluate what happens if you let it act.*

The first benchmark suite, **GB-BESS v0.1**, applies this to operational decisions for a simulated grid-connected Battery Energy Storage System (BESS) in a Great Britain electricity-system context.

## Intended users

- Researchers studying AI agent reliability in consequential, constrained decision domains.
- Teams building AI-assisted or autonomous energy operations tooling, who want independent evidence of failure modes before deployment.
- Policy and assurance researchers (e.g., studying staged autonomy or assurance frameworks) who need empirical behavioural evidence rather than capability-only benchmarks.
- Benchmark methodology researchers interested in action-validity, information-sufficiency, and consequence-based evaluation as a category distinct from answer-quality evaluation.

## Intended use

- Comparing how different agent architectures behave under identical, versioned physical, network, operational-policy, market, information-quality, and adversarial conditions.
- Discovering constraint violations, escalation failures, and information-sufficiency failures in a controlled, reproducible, simulation-only environment.
- Producing evidence for research and policy discussion about AI agent reliability in energy operations (see `docs/project/PID.md` for the intended DESNZ evidence output).

## Out-of-scope use

- **Certification of any real AI system as safe for real-world energy operations.** GridActionBench is a behavioural research benchmark, not a certification, conformance, or regulatory-approval system.
- **Any live or physical control of a real energy asset.** GB-BESS v0.1 is simulation-only by hard architectural constraint (see `docs/architecture/SECURITY.md`).
- **Claiming government or regulatory endorsement.** GridActionBench is not an official UK government benchmark, is not endorsed by DESNZ, Ofgem, NESO, or Elexon, and does not claim to be.
- **Ranking foundation models as a leaderboard exercise.** GridActionBench does not assume an LLM is the correct architecture for this task; a deterministic controller outperforming an LLM agent is a valid, expected, and reportable research outcome, not a benchmark failure.
- **Complete Grid Code / Distribution Code compliance assessment.** GB-BESS v0.1 models a deliberately narrow subset of physical and operational constraints; it does not implement full regulatory compliance testing.

## Subject

Individual operational decisions (CHARGE / DISCHARGE / IDLE / ESCALATE) for a single simulated grid-connected BESS asset, evaluated at a single decision point (Mode A, primary in v0.1) or across a short sequence of decision points (Mode B, small validated subset in v0.1).

## Geography

Great Britain electricity-system context. See `docs/suites/gb-bess/GB_SPECIFICITY.md` for an evidenced breakdown of exactly which design elements are genuinely GB-specific versus generic, and `docs/suites/gb-bess/GB_CONTEXT.md` for institutional background.

## Research questions

Primary: *How reliably do different AI-agent architectures make BESS operational decisions under physical constraints, network constraints, operational policies, market signals, degraded information, and adversarial conditions relevant to Great Britain?*

Secondary questions this benchmark is designed to surface evidence for (not exhaustive — see `docs/project/PID.md`):
- Which constraint categories (physical / network / operational-policy) are violated most often, and by which agent architectures?
- Do agents recognize insufficient information, or act on stale/missing/contradictory data as if it were reliable?
- Do agents escalate appropriately — neither over-escalating into operational uselessness nor under-escalating into unrecognised critical violations?
- Do economic incentives (price signals) cause agents to violate constraints they would otherwise respect?
- How do agents respond to adversarial inputs attempting to override stated constraints?
- Do failure patterns persist or worsen over a sequence of decisions (episode mode)?

## Benchmark modes

- **Mode A — Single-Step Evaluation** (primary for v0.1): one observation, one action, one evaluation.
- **Mode B — Episode Evaluation** (small validated subset for v0.1): a short sequence of decision points, used to detect behaviour that only emerges over time (progressive SOC depletion, repeated unnecessary escalation, oscillation, etc.).

## Scenario taxonomy

Seven families: **PHY** (physical constraints), **NET** (network constraints), **OPS** (operational policy), **MKT** (economic objectives), **DATA** (information quality), **ADV** (adversarial conditions), **HUM** (human escalation). See `docs/suites/gb-bess/SCENARIO_CATALOGUE.md`.

## Data

Synthetic scenarios calibrated to plausible GB parameter ranges, informed by (but not currently built from) real GB institutional mechanisms and, where licence-confirmed, real GB market data in later phases. See `docs/data/DATA_SOURCES.md` and `docs/data/DATA_PROVENANCE.md`. No scenario is represented as a historical GB event unless explicitly and verifiably sourced as such.

## Simulator

`SimpleBessSimulator` — a deliberately simple, deterministic battery state-transition model (SOC, charge/discharge efficiency, min/max SOC, max charge/discharge power, import/export headroom). Not a power-flow solver. See `docs/architecture/adr/ADR-003-simulator-abstraction.md`.

## Metrics

Reported as independent dimensions, never collapsed into a single opaque score (see `docs/benchmark/SCORING.md`): physical constraint adherence, network constraint adherence, operational-policy adherence, data-quality handling, adversarial resilience, appropriate escalation rate, unnecessary escalation rate, economic decision quality, and Unrecognised Critical Violation (UCV) counts (absolute, always reported alongside any percentage).

## Validation status (as of this card's last-updated date)

**Pre-calibration.** No golden tests, evaluator validation, scenario validation, or domain-expert review have yet been completed — this Benchmark Card is being published as part of Phase 0 specification work, ahead of any implementation. It will be revised substantially once Phase 1 (technical spike) and Phase 4 (calibration) are complete. Treat all metric names and scenario counts in this document as *design targets*, not validated capabilities, until `docs/project/DEFINITION_OF_DONE.md` is satisfied.

## Known limitations (stated plainly, per HELM's precedent — see `docs/research/PRIOR_ART.md`)

- GB-BESS v0.1 models a single BESS asset in isolation, not a multi-asset or whole-grid system.
- The simulator is a simplified state-transition model, not a physics-grade power-flow or dynamic simulator.
- Economic modeling is a narrow scalar reference-price signal, not a full revenue-stacking model.
- GB specificity is currently contextual/structural, not yet data-grounded in licence-confirmed real GB market data (see `docs/suites/gb-bess/GB_SPECIFICITY.md`, "Honest self-assessment").
- The benchmark cannot and does not certify real-world safety; see `docs/benchmark/METHODOLOGY.md` for the project's terminology discipline around "unsafe" vs. "constraint violation."
- Public benchmark data will, over time, likely appear in model-training corpora; see `docs/benchmark/CONTAMINATION_POLICY.md`.
- This benchmark is incomplete by design and cannot represent every real-world BESS operating condition.

## Misuse risks

- Treating a high GB-BESS score as evidence of real-world operational safety or regulatory readiness.
- Treating GB-BESS as a general AI capability leaderboard rather than a behavioural-reliability research tool.
- Assuming public benchmark scenarios remain a valid contamination-free test indefinitely (see `docs/benchmark/CONTAMINATION_POLICY.md`).

## Contamination risks

Public scenarios, once published, may enter model-training data over time. Mitigations include private holdouts, parameterized/generated scenario variants, and scenario retirement; see `docs/benchmark/CONTAMINATION_POLICY.md`. This benchmark does not claim its public test data remains uncontaminated forever.

## Version

GridActionBench framework: unreleased (Phase 0). GB-BESS suite: v0.1 (draft, unreleased). This card will be re-issued at each frozen benchmark version per `docs/benchmark/VERSIONING.md`.

## Governance

See `GOVERNANCE.md` (repository root, once populated) for maintainer, domain reviewer, benchmark reviewer, and contributor roles. GridActionBench operates independently of Enprompta or any proprietary platform; see `docs/project/PID.md`, "Relationship with Enprompta."

## Maintainers

See `GOVERNANCE.md`.

## Citation

See `CITATION.cff` (repository root, once populated).
