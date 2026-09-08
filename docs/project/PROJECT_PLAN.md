# Project Plan

**Status:** Draft — Phase 0. This reproduces the master brief's phase structure (§67-81) as the project's tracking artifact; see the master brief for full phase content, and `docs/project/BACKLOG.md` for the granular Phase 1 task list.

## Phase summary

| Phase | Window (indicative, per master brief) | Focus | Status |
|---|---|---|---|
| 0 — Foundation | 9-11 Sep 2026 | Specification, research, governance docs | In progress (this plan reflects work completed in this pass) |
| 1 — Technical spike | 12-18 Sep 2026 | Minimal working pipeline: Scenario→Oracle→Observation→Agent→Action→Validator→Simulator→Evaluation→Decision Record, 10 golden scenarios, CLI | **Complete** — 57/57 tests passing, 18/18 evaluators implemented (ahead of Phase 2's own target), all 20 scenarios implemented; see `docs/project/BACKLOG.md` |
| Gate 1 | 18 Sep 2026 | Technical feasibility demonstration | **Passed** — all seven acceptance criteria satisfied (`docs/project/BACKLOG.md`); one real evaluator bug and one scenario-documentation error found and fixed via end-to-end reference-agent runs, which is itself evidence the architecture surfaces its own defects as intended |
| 2 — Evaluation core | 19-27 Sep 2026 | ~15-25 evaluators implemented across all 7 families | Not started |
| 3 — Scenario engine | 22-30 Sep 2026 | Parameterised templates, generator, ≥100 templates, ≥1,000 executions | **Started** — 20 templates, 300-scenario generated set, `docs/suites/gb-bess/SCENARIO_TEMPLATES.md`; real gap to ≥100/≥1,000 remains and is documented, not hidden |
| 4 — Benchmark calibration | after Phase 3 | Run reference/seeded-failure agents, confirm expected failures detected | Not started |
| 5 — GB data | ~1-7 Oct 2026 | Research, licence-confirm, freeze real GB data where justified | Not started (Phase 0 research surfaced Elexon BMRS as the leading candidate, licence unconfirmed) |
| 6 — Resilience/adversarial testing | ~5-11 Oct 2026 | Expand DATA/ADV coverage | Not started |
| 7 — External validation | ~8-16 Oct 2026 | Domain-expert review | Not started |
| 8 — LLM/agent comparison | after Phase 4 + initial Phase 7 | ≥2 LLM configurations evaluated | Not started — explicitly gated on calibration |
| 9 — Benchmark freeze | ~16-19 Oct 2026 | Freeze v0.1 artifacts | Not started |
| 10 — Official experiment | ~19-23 Oct 2026 | Run and analyze the frozen benchmark | Not started |
| 11 — Public release | ~23-27 Oct 2026 | Publish repository, tag, results | Not started |
| 12 — DESNZ evidence | 24 Oct-5 Nov 2026 | Prepare evidence report | Not started |

## Phase 0 exit criteria (this phase)

Per master brief §67's Gate 0 requirement: convincing answers to "why GridActionBench given PowerAgentBench exists" and "what makes GB-BESS genuinely GB-specific" — both delivered in `docs/project/PID.md` §2. Remaining Phase 0 gaps: `docs/research/BENCHMARK_DESIGN_REVIEW.md` and `docs/research/EXPERT_REVIEW_CHECKLIST.md` (tracked in `docs/project/BACKLOG.md`), and the root governance/community files (README, LICENSE, CITATION.cff, CONTRIBUTING, CODE_OF_CONDUCT, GOVERNANCE, SECURITY, CHANGELOG).

## Critical path dependencies

- Phase 2 (evaluators) and Phase 3 (scenario engine) both depend on Phase 1's core pipeline existing — cannot parallelize ahead of Phase 1 completion.
- Phase 4 (calibration) depends on Phase 2 evaluators and Phase 3's rule-based/seeded-failure agents both existing.
- Phase 8 (LLM comparison) is strictly gated on Phase 4 calibration being judged satisfactory — this is a hard phase-ordering rule (master brief §28), not a scheduling suggestion, and this plan will not be amended to relax it under schedule pressure without an explicit, documented decision.
- Phase 9 (freeze) depends on Phase 5 (GB data), Phase 6 (resilience), and at least initial Phase 7 (external validation) feedback being incorporated.

## Change control

Any change to phase ordering or scope requires updating this document and `docs/project/RISK_REGISTER.md` together — a scope or schedule change that isn't reflected in the risk register is treated as incomplete change management.
