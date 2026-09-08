# ADR-012: Data Provenance

**Status:** Proposed

## Context
Master brief §34-36 requires every real dataset to carry a full retrieval → validation → transformation → frozen-dataset → checksum → benchmark-version provenance trail, and forbids depending on live upstream APIs for official runs.

## Decision
No real external dataset is committed to the repository until (a) its licence and redistribution status are explicitly confirmed (not merely assumed from the source organisation's general reputation — see `docs/suites/gb-bess/GB_SPECIFICITY.md`'s explicit caution about Elexon BMRS licence terms), and (b) it has gone through the full pipeline documented in `docs/architecture/DATA_MODEL.md`'s "Data provenance record" schema, ending in a checksummed, frozen artifact tied to a specific benchmark version. Official benchmark runs never make a live call to Elexon BMRS, NESO, Ofgem, or any other external API at execution time — only to frozen, versioned local data.

## Alternatives considered
- **Fetch live data at run time for realism** — rejected: master brief §34 explicitly forbids this; live dependency would also break reproducibility (a run executed today and the same run executed next month against a live feed would not be comparable) and introduces an availability dependency the benchmark's CI and contributors should not have to bear.
- **Assume government/quasi-government data sources are automatically redistributable** — rejected: master brief §35 explicitly warns not to assume uniform licensing even within one organisation; this project's own research (`GB_SPECIFICITY.md`) already found the Elexon BMRS licence terms could not be fully confirmed in one research pass, reinforcing why this caution is not hypothetical.

## Consequences
- Positive: every frozen dataset used in official results is independently reproducible and legally clean by construction, rather than by post-hoc audit.
- Negative: GB-BESS v0.1 currently runs on synthetic data calibrated to plausible GB ranges rather than real market data, because the licence-confirmation step for the most relevant real dataset (Elexon BMRS) has not yet been completed — an honest, stated limitation (`docs/suites/gb-bess/GB_SPECIFICITY.md`, "Honest self-assessment"), not a silent gap.
