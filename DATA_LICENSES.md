# Data Licenses

This file summarizes the licensing status of all data used by GridActionBench. It is the top-level entry point; full provenance detail lives in `docs/data/DATA_PROVENANCE.md` and source research in `docs/data/DATA_SOURCES.md`.

## Summary

**GB-BESS v0.1 uses only synthetic data.** No real-world third-party dataset is currently bundled with this repository. All scenario data is authored, synthetic, and tagged `source_type: synthetic` in every scenario file (see `docs/suites/gb-bess/SCENARIO_CATALOGUE.md`).

Synthetic scenario data authored by GridActionBench contributors is licensed the same as the project's code — see `LICENSE` (Apache License 2.0) — unless a future dataset-specific licence is required (e.g. if a real, third-party-sourced dataset is ever added, per the process in `docs/data/DATA_PROVENANCE.md`, its licence will be documented here as a distinct entry, separate from the code licence).

## Candidate future data sources under evaluation (not yet included)

| Source | Status |
|---|---|
| Elexon Insights Solution API (wholesale/balancing price data) | Freely accessible, no API key required (corrected 2026-09-08 — see `docs/data/DATA_SOURCES.md`, "Correction"). Redistribution/commercial-use licence terms not yet confirmed from primary source; not included. |
| DESNZ/GOV.UK publications | Used only as narrative/contextual citation (typically OGL-licensed); no bulk data included. |

## Policy

No dataset with an unconfirmed or unclear redistribution status will be committed to this repository. See `docs/architecture/adr/ADR-012-data-provenance.md` for the full rationale.

This file will be updated whenever a real dataset is added, per the provenance process in `docs/data/DATA_PROVENANCE.md`.
