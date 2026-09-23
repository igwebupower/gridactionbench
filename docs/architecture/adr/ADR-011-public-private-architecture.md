# ADR-011: Public/Private Architecture

**Status:** Proposed

## Context
Master brief §37-39 requires a public/private split that is justified, not arbitrary, and holdouts that test only documented capabilities.

## Decision
Generator-based private holdouts (published generator code and acceptance criteria; private seeds and drawn instances) rather than a fixed hand-authored private scenario bank or a fixed percentage split. Full rationale in `docs/benchmark/PUBLIC_PRIVATE_POLICY.md`, informed directly by the Power Systems Agent Benchmark's per-family deterministic generator design (`docs/research/PRIOR_ART.md` §1.1 item 3). Private evaluation infrastructure lives in a separate private repository (`gridactionbench-evaluation-private`) — created 2026-09-23 but still empty (no holdouts, seed, or protocol populated yet) — with `.gitignore`d local fixtures used for any interim private-development needs.

## Alternatives considered
- **Fixed 80/20 (or any fixed percentage) hand-authored split** — rejected: master brief §38 explicitly forbids choosing a percentage by convention alone; a generator-based approach answers the underlying contamination/statistical-power/maintenance-burden questions more directly than any fixed ratio would (see `PUBLIC_PRIVATE_POLICY.md` for the full argument).
- **Everything public, no holdouts at all** — rejected: would leave the benchmark with no defense against prompt-overfitting or scenario memorization (`docs/benchmark/THREAT_MODEL.md`), undermining its research value for exactly the claims (constraint adherence, escalation reliability) it exists to measure credibly.

## Consequences
- Positive: holdout generation logic is itself auditable by the public even though specific instances are not, directly supporting transparency (master brief priority list, §87) without sacrificing anti-gaming protection.
- Negative: requires building generator infrastructure (Phase 3) before any holdout evaluation is credible — GB-BESS v0.1 has no "GridActionBench Verified" results at Phase 0/1, only Local/Reproducible Submission tiers, until that infrastructure exists.
