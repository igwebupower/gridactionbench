# Governance

**Status:** Draft. This governance structure predates the project's implementation work and has not needed to change as it progressed — GridActionBench's implementation is currently Phase 1-3 (`docs/project/PROJECT_PLAN.md`), but there is still one identified maintainer and no confirmed external contributors or reviewers (tracked in a maintainer-controlled internal record). This document defines the intended structure so independent participation is possible from the outset, not merely once the project happens to attract contributors.

## Roles

### Maintainer
Responsible for repository and release management: merging changes, cutting versioned releases (`docs/benchmark/VERSIONING.md`), and final decisions when review roles disagree. The maintainer does not have unilateral authority to change scoring logic, evaluator behaviour, or released scenario content without following the change-control process below (§ "Changes affecting official benchmark behaviour").

### Domain Reviewer
Energy-engineering review: battery physics, GB network operations, market mechanics. Assesses whether scenario parameters, physical/network/operational constraints, and GB-specificity claims are defensible (feeds a maintainer-controlled internal assumptions record and the Phase 7 external validation process in `docs/research/EXPERT_REVIEW_CHECKLIST.md`).

### Benchmark Reviewer
Evaluation-methodology review: construct validity, statistical power, contamination resistance, scoring design. Assesses whether a metric measures what its name claims (`docs/benchmark/METHODOLOGY.md` §9) and whether proposed evaluator or scenario changes preserve or degrade benchmark integrity.

### Contributor
Anyone submitting code, scenarios, data, documentation, or research to the project. No special status is required to contribute — see `CONTRIBUTING.md`.

## Independence from commercial interests

GridActionBench operates independently of any proprietary platform (`docs/project/PID.md` §3). No governance role is contingent on affiliation with any specific company, and no design decision may be made to favor a commercial product's roadmap over the benchmark's own research integrity. This is a standing constraint on the Maintainer role specifically, since that role has the most day-to-day influence over the project's direction.

## Changes affecting official benchmark behaviour

Per master brief §60, any change to scenarios, evaluators, schemas, or scoring logic that affects official benchmark results requires, in order:

1. A public issue or recorded proposal describing the change.
2. A stated rationale.
3. An impact assessment (which prior results does this affect? does it require a version bump, and at what level — `docs/benchmark/VERSIONING.md`?).
4. Tests (unit/golden/regression as applicable — `docs/testing/TEST_STRATEGY.md`).
5. Review (Benchmark Reviewer at minimum; Domain Reviewer if the change touches energy-domain assumptions).
6. Documentation update.
7. An explicit versioning decision.

A change skipping any of these steps is not eligible for merge into a path that affects official benchmark behaviour, regardless of who proposes it, including the Maintainer.

## Decision-making

Where Domain Reviewer and Benchmark Reviewer assessments conflict (e.g., a physically realistic scenario that the Benchmark Reviewer judges to have poor construct validity, or vice versa), the Maintainer makes the final call, with the disagreement and rationale recorded in the relevant issue — disagreements are not silently resolved by the Maintainer overriding without explanation.

## Current role holders

To be populated as the project gains contributors. As of this writing, the Maintainer role is held by the project's original author; no Domain Reviewer or Benchmark Reviewer role has been formally filled.
