# Changelog

All notable changes to GridActionBench are documented here. Versioning follows `docs/benchmark/VERSIONING.md` — framework, suite, scenario set, evaluator set, and simulator are versioned independently; this changelog notes which artifact(s) each entry affects.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased] — Phase 0

### Added
- Initial repository structure per `docs/architecture/ARCHITECTURE.md` and the master project specification.
- Phase 0 foundation documentation: Benchmark Card, core and GB-BESS suite specifications, prior-art review (`docs/research/PRIOR_ART.md`), PowerAgentBench review (`docs/research/POWERAGENTBENCH_REVIEW.md`), benchmark design self-review (`docs/research/BENCHMARK_DESIGN_REVIEW.md`), GB specificity analysis (`docs/suites/gb-bess/GB_SPECIFICITY.md`), initial 20-scenario catalogue plus 6 episode designs (`docs/suites/gb-bess/SCENARIO_CATALOGUE.md`), 18-evaluator catalogue specification (`docs/suites/gb-bess/EVALUATION_SPEC.md`), governance and policy documents (public/private, contamination, threat model, submission rules, versioning, scoring, methodology), 17 architecture decision records, project management documents (PID, project plan, risk register, assumptions register, backlog, definition of done), and community/governance files (this changelog, README, LICENSE, CITATION.cff, CONTRIBUTING, CODE_OF_CONDUCT, GOVERNANCE, SECURITY).
- No implementation code yet — this release is documentation and specification only.

### Notes
- No public GitHub remote has been configured as of this entry; the repository is a standalone local git repository.
- No LLM comparison, calibration run, or scenario execution has occurred — all metrics, thresholds, and scenario parameter values in the Phase 0 documentation are design targets, not validated results.
