# Definition of Done — GB-BESS v0.1

**Status:** Draft — Phase 0. This is the master brief §83 checklist, reproduced here as the project's live tracking artifact (not restated narrative — see the master brief itself for full context on each item).

## Core
- [ ] Clean installation
- [ ] CLI execution
- [ ] Deterministic simulator (`SimpleBessSimulator`)
- [ ] Versioned schemas (`EnergyObservationV1`, `AgentActionV1`)
- [ ] Scenario Oracle implemented
- [ ] Observation/Oracle separation implemented (not just specified — `docs/architecture/adr/ADR-005`)
- [ ] Immutable Decision Records

## Evaluation
- [ ] ≥15 meaningful evaluators implemented (18 specified in `docs/suites/gb-bess/EVALUATION_SPEC.md`, 0 implemented as of Phase 0)
- [ ] Hard/operational/objective/information separation implemented in code, not just in documentation
- [ ] UCV detection implemented
- [ ] Escalation evaluation implemented
- [ ] Counterfactual support for selected scenarios implemented

## Scenarios
- [ ] ≥100 meaningful templates/definitions (20 fully specified as of Phase 0; templates are Phase 3 work)
- [ ] ≥1,000 executions
- [ ] Single-step suite implemented
- [ ] Small episode suite implemented (6 designed as of Phase 0, 0 implemented)
- [ ] Provenance tracked per scenario
- [ ] Versioning enforced per scenario

## Calibration
- [ ] AlwaysIdleAgent implemented and run
- [ ] AlwaysEscalateAgent implemented and run
- [ ] RuleBasedAgent implemented and run
- [ ] Seeded failure agents implemented and run
- [ ] Known failures correctly detected (documented calibration report produced)

## Agent research
- [ ] ≥2 LLM configurations evaluated, after calibration is satisfactory (not before — master brief §28)
- [ ] Repeated trials where appropriate for stochastic agents
- [ ] Reproducibility metadata captured for every run

## Benchmark science
- [x] Benchmark Card (`docs/benchmark/BENCHMARK_CARD.md`)
- [x] Methodology (`docs/benchmark/METHODOLOGY.md`)
- [x] Threat model (`docs/benchmark/THREAT_MODEL.md`)
- [x] Contamination policy (`docs/benchmark/CONTAMINATION_POLICY.md`)
- [x] Holdout policy (`docs/benchmark/PUBLIC_PRIVATE_POLICY.md`)
- [x] Reference Track specification (`docs/benchmark/SUBMISSION_RULES.md`)
- [x] Limitations stated (distributed across `BENCHMARK_CARD.md`, `GB_SPECIFICITY.md`, and per-evaluator/per-ADR limitations sections)
- [ ] Construct-validation review completed (register exists — `docs/project/ASSUMPTIONS.md` — but no item has completed external review yet)

## GB context
- [x] GB specificity documented (`docs/suites/gb-bess/GB_SPECIFICITY.md`)
- [x] Data provenance process documented (`docs/data/DATA_PROVENANCE.md`)
- [x] Dataset licences checked before use (none committed yet; Elexon BMRS explicitly flagged unconfirmed)
- [x] No fake GB specificity claimed (explicit "honest self-assessment" in `GB_SPECIFICITY.md` distinguishes contextual from data-grounded specificity)

## External validation
- [ ] At least one credible external energy-domain review completed
- [ ] Review issues documented (Feedback → Issue → Assessment → Accepted/Rejected → Rationale → Change, per `docs/benchmark/METHODOLOGY.md` §8)

## Release
- [ ] Public repository (standalone repo initialized Phase 0; not yet pushed to a public remote)
- [ ] Release tag
- [ ] Citation metadata (`CITATION.cff`)
- [ ] Reproducible results
- [x] No physical energy-system interaction (architecturally enforced from Phase 0 — `docs/architecture/SECURITY.md`, `ADR-015`)

## Current overall status

Phase 0 (specification/research) substantially complete as of this document's writing. Zero implementation work has begun — every unchecked item above is Phase 1+ work. This checklist should be updated at the end of every phase, not only at the end of the project.
