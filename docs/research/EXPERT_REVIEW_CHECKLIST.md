# Expert Review Checklist

**Status:** Draft — Phase 0, prepared ahead of Phase 7 (External Validation, ~8-16 Oct 2026). This is the question set to be put to external domain reviewers; per `docs/benchmark/METHODOLOGY.md` §8, reviewers are asked what is wrong, ambiguous, or misleading — not whether they generally approve of the project.

## Reviewer profiles sought

- BESS engineering / battery systems (physical constraint realism — `docs/project/ASSUMPTIONS.md` A-01, A-06, A-08)
- GB power-network operations (DNO/DSO curtailment, ANM realism — A-03; NET family scenario design)
- BESS optimisation / trading (MKT family scope and the "narrow economic modeling" claim in `docs/suites/gb-bess/SPECIFICATION.md` §7)
- AI evaluation / benchmark methodology (construct validity, UCV design, public/private holdout design)
- AI agent architecture (agent interface realism — `docs/research/BENCHMARK_DESIGN_REVIEW.md`, "Agent interface / tool contracts" finding)
- Energy-system modeling more broadly (simulator fidelity trade-off — `ADR-003`)

## Question set

### Physical / battery engineering
1. Are the illustrative SOC/power-limit/efficiency values in `SCENARIO_CATALOGUE.md` (§PHY) plausible for a real grid-connected BESS, or do they suggest an asset class/size that doesn't exist in practice?
2. Is a constant (non-power-dependent, non-SOC-dependent) efficiency coefficient (`ASSUMPTIONS.md` A-06) a defensible simplification for this benchmark's purpose, or does it hide behaviour that actually matters for the failure modes being tested?
3. Is the staleness threshold placeholder (`ASSUMPTIONS.md` A-04) in a sane range for real BESS telemetry, or off by an order of magnitude in either direction?

### Network / DNO operations
4. Does the benchmark's network-headroom model (`GB_SPECIFICITY.md` Feature 1) fairly represent how ANM/Technical Limits curtailment actually behaves, or does it oversimplify in a way that would mislead a reader about real DNO operational practice?
5. Is treating headroom as a single scalar (rather than a curve, or multi-signal DERMS instruction) a reasonable v0.1 simplification, or does it eliminate exactly the behaviour (e.g. rapid signal changes) that matters most for testing agent adaptation?

### Market / economics
6. Is the single-scalar reference-price mechanic (`SPECIFICATION.md` §7) sufficient to test "does economic incentive cause constraint violation," or does its narrowness undermine even that limited claim?
7. Does the benchmark's explicit refusal to model Balancing Mechanism bid/offer mechanics or revenue-stacking (`GB_CONTEXT.md`, "What GB-BESS v0.1 explicitly does not model") leave a gap serious enough that the MKT family's findings would be misleading to a BESS-trading audience?

### GB specificity
8. Having read `GB_SPECIFICITY.md` in full: is the "contextual/structural but not yet data-grounded" self-assessment accurate, or does it understate/overstate the benchmark's genuine GB-specificity either way?
9. Are there other GB-specific mechanisms (beyond ANM/Technical Limits, BMRS settlement structure, and the connections-queue policy context) that a credible GB-BESS benchmark should incorporate and currently does not?

### Benchmark methodology
10. Is the UCV definition (`SPECIFICATION.md` §8) — binary, not severity-weighted — a reasonable v0.1 starting point, or does it need severity weighting before any published result should be taken seriously?
11. Does the escalation-quality design (Appropriate vs. Unnecessary Escalation Rate, `SPECIFICATION.md` §9, `EVALUATION_SPEC.md` HUM-ESCALATE-CRITICAL-DATA-001) actually distinguish a genuinely useful autonomous system from a merely cautious one, or does it have blind spots?
12. Is the generator-based public/private holdout design (`PUBLIC_PRIVATE_POLICY.md`) sound, or does its acceptance-criteria logic have exploitable gaps?
13. Having read `docs/research/BENCHMARK_DESIGN_REVIEW.md`'s self-identified weaknesses: which of those five findings is most urgent to fix before any public release, and which (if any) is overstated?

### Agent architecture
14. Is the single-call `AgentAdapter.act()` interface (`ADR-004`) a reasonable constraint for the kinds of agents this benchmark should be evaluating, or does it structurally exclude an important class of agent design?

## Process

Each reviewer's response is logged as: Feedback → Issue (filed) → Assessment → Accepted/Rejected → Rationale → Change (or explicit no-change decision with rationale). No feedback is silently dropped; rejected feedback's rationale is documented alongside the accepted changes, per `docs/benchmark/METHODOLOGY.md` §8.
