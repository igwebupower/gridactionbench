# Versioning

**Status:** Draft — Phase 0

## Versioned artifacts

Six independently versioned artifacts exist, and every published result must cite all six (master brief §46):

| Artifact | Versioning scheme | Owner |
|---|---|---|
| GridActionBench framework | SemVer (`MAJOR.MINOR.PATCH`) | `gridactionbench/` core library |
| Suite (e.g. GB-BESS) | SemVer, independent of framework version | `suites/gb_bess/` |
| Scenario set | SemVer, independent of suite version | scenario files under `suites/gb_bess/v0_1/` |
| Evaluator set | SemVer, independent of all the above | `gridactionbench/evaluators/` |
| Simulator | SemVer | `gridactionbench/simulators/` |
| Agent configuration | Free-text/structured description, not SemVer — captures model id, prompt hash, temperature, tools, etc. | run-specific, recorded in the Decision Record |

## Why independent versioning, not one project-wide version number

A framework release that only touches the CLI or reporting layer should not force every existing scenario and evaluator result to be treated as non-comparable to prior runs. Conversely, a single evaluator bugfix (e.g. correcting `OPS-RESERVE-SOC-001`'s boundary comparison from `>` to `>=`) must invalidate comparability of *that evaluator's* historical results without requiring every other evaluator's results to be re-run. Independent versioning is what makes this possible; a single monolithic version number would force an unjustifiably conservative choice between never bumping it (hiding real changes) or bumping it for everything (destroying historical comparability unnecessarily).

## Rules

1. **No published result omits a version tuple.** The required citation form is: *"Agent configuration X achieved 97% network-constraint adherence on GridActionBench GB-BESS v0.1 (evaluator set v0.1.0, scenario set v0.1.0, simulator v0.1.0)."* An unqualified "Model X scored 97%" is not a valid GridActionBench claim (master brief §46).
2. **Released public scenarios are immutable.** A correction to a published scenario requires a new `scenario_version`, never an in-place edit of a released scenario file (master brief §44). The old version remains available for reproducibility of prior results.
3. **Evaluator logic changes require a version bump plus documentation.** Any change to an evaluator's `logic_or_formula`, thresholds, or pass/warning/failure boundaries requires: rationale, tests, impact analysis (which prior results does this affect?), documentation update in `docs/suites/gb-bess/EVALUATION_SPEC.md`, and a version increment (master brief §45). Scoring logic is never silently altered.
4. **Simulator changes require a version bump.** Any change to `SimpleBessSimulator`'s state-transition logic (efficiency application, boundary handling, timestep semantics) requires a version increment; results from different simulator versions are not directly comparable and must be labeled accordingly.
5. **Benchmark freeze (Phase 9) is a hard version boundary.** Once GB-BESS v0.1 is frozen (schemas, simulator, scenario suite, evaluator versions, methodology, Reference Track protocol, baseline configurations, official holdout configuration — master brief §77), any subsequent change requires a new suite version (v0.1.1 patch for non-breaking fixes, v0.2.0 for anything that changes comparability), never a silent edit to the frozen v0.1 artifacts.

## SemVer interpretation for this project

- **MAJOR** — breaking change to schema, required-field structure, or evaluator pass/fail semantics that would invalidate direct comparison with prior results.
- **MINOR** — additive, backward-compatible change (new optional schema field, new evaluator, new scenario added to an existing family) that does not alter existing scenarios' or evaluators' behaviour.
- **PATCH** — bugfix that does not change intended pass/fail semantics (e.g., a typo fix in a scenario description, a logging fix) — anything that *does* change intended semantics is MINOR or MAJOR even if the code diff is small.

## Where version metadata lives

Every Decision Record (`docs/benchmark/SPECIFICATION.md` §7) carries all six version fields plus `git_commit` and `runtime_version`, making every individual run independently reproducible-in-principle without cross-referencing external release notes.
