# Security Policy

## Physical-system isolation (the most important thing in this file)

**GridActionBench GB-BESS v0.1 is simulation-only.** No component in this repository may issue commands to, or maintain credentials for, a physical energy asset or operational energy-system interface (SCADA, EMS, inverter control, DNO control, DERMS, market bidding execution). This is an architectural guarantee, enforced by design — see `docs/architecture/SECURITY.md` and `docs/architecture/adr/ADR-015-physical-system-isolation.md` for the full statement and enforcement mechanism.

If you believe you have found a code path, dependency, or schema field that could plausibly reach a real operational endpoint, **report it immediately** as described below — this is treated as the highest-severity class of issue this project can have.

## Reporting a vulnerability or isolation concern

Please report security concerns, including any suspected physical-system isolation violation, privately to the project maintainer (see `GOVERNANCE.md` for current contact information) rather than as a public issue, until a fix is available. Include:

- A description of the concern.
- Steps to reproduce, if applicable.
- The affected file(s) or component(s).

## Scope

This policy covers the GridActionBench codebase, its documented dependencies, and its evaluation infrastructure (public and, once built, private — `docs/benchmark/PUBLIC_PRIVATE_POLICY.md`). It does not cover any real energy asset, network, or market system — none are integrated with this project, by design.

## Other integrity concerns

For benchmark-integrity concerns that are not security vulnerabilities in the traditional sense (e.g., suspected evaluator gaming, contamination, or holdout leakage), see `docs/benchmark/THREAT_MODEL.md` and report through the same channel — these are taken seriously as threats to the project's research validity even when they carry no traditional "CVE" framing.
