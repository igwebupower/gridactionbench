# Contamination Policy

**Status:** Draft — Phase 0

## Starting premise

Public benchmark data will, over time, plausibly appear in model-training corpora. GridActionBench does not claim its public scenarios remain contamination-free indefinitely, and no report produced by this project should imply otherwise (master brief §43, §86).

## What contamination would look like here

Unlike a text-QA benchmark, contamination for GridActionBench is not "the model memorized the answer string." It would instead look like: a model having seen the published `SCENARIO_CATALOGUE.md` (or its parameter ranges/templates) during training and having learned to pattern-match "this looks like a GridActionBench PHY-boundary scenario" well enough to produce the locally-correct action without the underlying capability generalizing to a structurally similar but numerically different held-out instance. This is a subtler failure than string memorization and is one reason `docs/research/PRIOR_ART.md` flags the Power Systems Agent Benchmark's "unanimous agent disagreement with the evaluator" quality-control pattern as worth adopting — a model performing well on public scenarios but poorly, or suspiciously *too* well, on generated variants is itself diagnostic.

## Mitigations adopted for GB-BESS v0.1

1. **Private holdouts drawn from published generators, not hand-authored secret scenarios** — see `docs/benchmark/PUBLIC_PRIVATE_POLICY.md`. A generator-based approach is inherently harder to contaminate via memorization of specific instances, since the instances an evaluator actually sees are not the ones a model could have trained on.
2. **Parameterised scenarios (Phase 3) over a fixed scenario bank.** Once ≥100 templates exist, official evaluation draws fresh parameter combinations rather than reusing the exact same numeric values release after release.
3. **Rotating official sets across benchmark versions.** GB-BESS v0.2 and later versions are expected to draw from regenerated or expanded holdout pools, not the same frozen v0.1 holdout indefinitely.
4. **Novel combinations across scenario dimensions** (SOC regime × network regime × price regime × policy state × information quality — see master brief §53 coverage tracking) as a further defense: even if individual dimension values leak, novel *combinations* remain harder to have specifically memorized.
5. **Contamination disclosure.** If evidence of contamination is found (e.g., suspiciously perfect performance on public scenarios that does not replicate on structurally equivalent generated variants), it will be documented in the relevant results report, not suppressed.
6. **Scenario retirement.** A public scenario that is confirmed contaminated (e.g., appears verbatim or near-verbatim in a model's training-adjacent outputs) is retired from official evaluation use and replaced, with the retirement itself documented in `CHANGELOG.md`.

## What this policy does not do

It does not claim to detect contamination reliably — GridActionBench has no training-data-access mechanism to confirm contamination directly (no benchmark does, in general, without model-provider cooperation). The mitigations above reduce contamination's *practical impact* on result validity; they do not eliminate the possibility of it, and this document does not claim otherwise.

## Relationship to the public/private policy

This document assumes and depends on `docs/benchmark/PUBLIC_PRIVATE_POLICY.md`'s generator-based holdout design; the two documents should be read together and kept in sync — a change to the holdout generation strategy in one requires reviewing the contamination-mitigation claims in this one.
