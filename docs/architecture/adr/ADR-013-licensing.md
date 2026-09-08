# ADR-013: Code Licensing

**Status:** Proposed

## Context
Master brief §58 requires an ADR comparing Apache-2.0 and MIT, with a starting recommendation of Apache-2.0, considering commercial reuse, contribution, patent grant, and ecosystem compatibility.

## Decision
**Apache License 2.0** for all GridActionBench code (`gridactionbench/`, `baselines/`, `suites/`, `scripts/`, `tests/`, `examples/`). Dataset licensing is tracked entirely separately (`DATA_LICENSES.md`, `docs/data/DATA_SOURCES.md`) and is never assumed to inherit the code licence.

## Rationale
- **Patent grant.** Apache-2.0 includes an explicit patent grant and defensive termination clause, which matters for a benchmark that may be used by commercial entities (energy operators, AI vendors) evaluating their own systems — reduces patent-litigation risk for contributors and users in a way MIT's shorter text does not address.
- **Commercial reuse.** Both licences permit commercial reuse; no material difference here.
- **Contribution.** Apache-2.0 is widely recognized and accepted by corporate contributor policies (many companies' OSS-contribution approval processes specifically favor Apache-2.0 for its patent clause), which matters for master brief §59's goal of enabling independent, potentially corporate-affiliated contributors (e.g. DNOs, BESS operators, other AI labs).
- **Ecosystem compatibility.** MIT-licensed sibling prior-art repositories (PowerMCP, PowerFM, PowerWF — `docs/research/PRIOR_ART.md` §7) are compatible with Apache-2.0 consumption (MIT code can be incorporated into an Apache-2.0 project); the reverse is not guaranteed, so choosing Apache-2.0 preserves more future interoperability optionality than choosing MIT would.

## Alternatives considered
- **MIT** — simpler, marginally more permissive text, but no explicit patent grant; rejected given the commercial-and-research dual audience this project expects.
- **GPL family (copyleft)** — rejected: would restrict commercial adoption by energy-sector and AI-vendor users in ways contrary to the project's stated goal of broad, low-friction adoption (master brief §59, §84 non-goals notwithstanding — the code itself should still be maximally reusable).

## Consequences
- Positive: aligns with the broader ecosystem's licensing norms (MLCommons' MLPerf reference implementations and most modern AI-benchmark tooling use permissive licences); reduces friction for corporate contribution and adoption.
- Negative: none material — Apache-2.0 is a well-understood, low-risk choice for this project's profile.

## Attribution requirement if reusing licensed code
If any future code is incorporated from another project, its licence must be verified and required notices/attributions preserved before merge (master brief §58) — no code has been copied from any reviewed prior-art repository to date (`docs/research/PRIOR_ART.md` §7, `docs/research/POWERAGENTBENCH_REVIEW.md` §14).
