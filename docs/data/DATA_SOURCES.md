# Data Sources

**Status:** Draft — Phase 0 research. No real external dataset has been retrieved or committed as of this document's writing; this is a survey of candidate sources and their licensing status, per master brief §34-35.

## Candidate sources identified (Phase 0 research)

| Source | Organisation | What it could provide | Licence status (as researched 2026-09-08) | Committed to repo? |
|---|---|---|---|---|
| BMRS / Insights Solution API | Elexon | Half-hourly wholesale/imbalance settlement prices, generation mix, demand | Governed by "BMRS Data Licence Terms" and "BMRS API Terms of Use Policy"; free account + API key required. **Redistribution terms not fully confirmed** — the primary licence-terms page could not be retrieved during this research pass (403 response). See `docs/suites/gb-bess/GB_SPECIFICITY.md`, Feature 2. | **No** — pending licence confirmation |
| GOV.UK / DESNZ publications | DESNZ | Policy context (Clean Flexibility Roadmap, Connections Reform figures) used narratively in `GB_SPECIFICITY.md` | Typically Open Government Licence (OGL) — permits copy/publish/distribute/adapt, including commercial use, with attribution | Narrative citation only; no bulk data committed |
| NESO / DNO ANM & Technical Limits documentation | NESO, individual DNOs, ENA | Conceptual/structural grounding for the network-headroom model (not raw operational data) | Not assessed for redistribution — used as conceptual reference only, no data extracted or committed | N/A — no data extracted |

## Policy

Per `docs/architecture/adr/ADR-012-data-provenance.md`: **no dataset is committed to this repository with an unconfirmed or unclear redistribution status.** Where a source is valuable but its licence is unconfirmed (BMRS, currently), this project uses it only as narrative/contextual grounding (cited, not redistributed) until the licence is explicitly confirmed by a maintainer reading the actual current licence terms, at which point a proper `docs/data/DATA_PROVENANCE.md` entry and `DATA_LICENSES.md` entry would be added alongside the retrieval script.

## What GB-BESS v0.1 actually uses

**Synthetic data only**, calibrated to plausible parameter ranges informed by (but not extracted from) the sources above. Every synthetic scenario is explicitly tagged `source_type: synthetic` (master brief §36) and is never presented as derived from or equivalent to real historical GB data. See `docs/suites/gb-bess/SCENARIO_CATALOGUE.md`.

## Open research items

```text
RESEARCH TODO — NETWORK ACCESS REQUIRED
- Directly retrieve and read the current Elexon "BMRS Data Licence Terms" and "BMRS API
  Terms of Use Policy" documents in full (not a secondary summary) before any BMRS-derived
  data is used beyond narrative citation.
- If BMRS data is ever frozen into the benchmark (Phase 5), determine the correct
  attribution format required by Elexon's terms, and complete a full
  docs/data/DATA_PROVENANCE.md entry per the schema in docs/architecture/DATA_MODEL.md.
- Assess whether NESO publishes any open, licensed historical ANM/curtailment event data
  that could ground NET-family scenario parameter ranges more precisely than the current
  qualitative/narrative grounding in GB_SPECIFICITY.md.
```

## Relationship to other documents

This document is the source-survey layer; `docs/data/DATA_PROVENANCE.md` is where an actually-retrieved, frozen dataset's full provenance record would be documented (none exist yet); `DATA_LICENSES.md` (repository root) is the top-level licence summary a downstream user reads first.
