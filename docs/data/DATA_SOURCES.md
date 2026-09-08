# Data Sources

**Status:** Revised — Phase 0.5 correction pass (2026-09-08). Corrects a factual error in the Phase 0 draft about Elexon API access requirements — see "Correction" below. No real external dataset has been retrieved or committed as of this document's writing; this is a survey of candidate sources and their licensing status, per master brief §34-35.

## Correction: Elexon API access (Phase 0.5)

The Phase 0 draft of this document, and of `docs/suites/gb-bess/GB_SPECIFICITY.md`, incorrectly stated that "a free Elexon account and API key" are required to access BMRS/Insights Solution data. This was checked against current primary and secondary sources on 2026-09-08 and found to be wrong for the API this project would actually use.

- **Current Elexon Insights Solution APIs** (`developer.data.elexon.co.uk`, `bmrs.elexon.co.uk`) — the RESTful APIs serving current settlement/generation/demand data — are **public with no account or API key required**. The developer portal states directly: *"All our APIs are public and no API key is required."* Confirmed by direct fetch of `developer.data.elexon.co.uk` (2026-09-08) and cross-confirmed by independent search-indexed summaries of the same portal referencing "no API key is required" and Open API principles.
- **The account/API-key requirement described in the Phase 0 draft applied to a legacy BMRS arrangement** (an older "scripting key" system referenced in third-party integration guides, distinct from the current Insights Solution REST APIs) and should not have been generalized to the current API without checking. This project's Phase 0 research conflated the two; this pass corrects that conflation everywhere it appeared (this document and `GB_SPECIFICITY.md`).
- **What remains unconfirmed, and is not assumed:** redistribution/commercial-use licensing terms. Two Elexon pages appear to govern this — a "BMRS Data Licence Terms" / copyright page (`elexon.co.uk/bsc/data/balancing-mechanism-reporting-agent/copyright-licence-bmrs-data/`) and a separate "Copyright: Licence to use BMRS APIs" page (`elexon.co.uk/bsc/data/balancing-mechanism-reporting-agent/copyright-licence-use-bmrs-api/`). Both returned HTTP 403 to this project's automated fetch tool on 2026-09-08 and could not be read directly. Secondary, search-indexed summaries of these pages were inconsistent — one indicated data "may be exploited, including commercially," another described a licence granted "for non-commercial purposes." This inconsistency is reported, not resolved — per explicit instruction, no assumption is made about redistribution rights either way. A maintainer must read both primary pages directly (e.g., via an ordinary authenticated browser session, since the automated fetch tool used in this research pass was blocked) before any Elexon-derived data is committed to this repository.

## Candidate sources identified (Phase 0 research, access-requirement corrected Phase 0.5)

| Source | Organisation | What it could provide | Licence status (corrected 2026-09-08) | Committed to repo? |
|---|---|---|---|---|
| Elexon Insights Solution API (current) | Elexon | Half-hourly wholesale/imbalance settlement prices, generation mix, demand | No account/API key required to access. Redistribution/commercial-use terms unconfirmed — primary licence pages blocked (HTTP 403) to automated fetch; secondary summaries inconsistent on commercial vs. non-commercial scope. See "Correction," above. | No — pending direct primary-source licence confirmation by a maintainer |
| Legacy BMRS scripting-key arrangement | Elexon | Same underlying data, older access method | Distinct from the current API above; not used or referenced further by this project | No — not applicable, superseded by the current Insights Solution API |
| GOV.UK / DESNZ publications | DESNZ | Policy context (Clean Flexibility Roadmap, Connections Reform figures) used narratively in `docs/suites/gb-bess/GB_CONTEXT.md` | Typically Open Government Licence (OGL) — permits copy/publish/distribute/adapt, including commercial use, with attribution | Narrative citation only; no bulk data committed |
| NESO / DNO ANM & Technical Limits documentation | NESO, individual DNOs, ENA | Conceptual/structural grounding for the network-headroom model (not raw operational data) | Not assessed for redistribution — used as conceptual reference only, no data extracted or committed | N/A — no data extracted |

## Policy

Per `docs/architecture/adr/ADR-012-data-provenance.md`: no dataset is committed to this repository with an unconfirmed or unclear redistribution status. Elexon Insights Solution data is now confirmed freely *accessible* (no API key), but its redistribution/commercial-use terms remain unconfirmed (see above) — access ease does not imply redistribution rights, and this project treats the two as separate questions. Until the licence is explicitly confirmed by a maintainer reading the actual current licence terms, this project uses Elexon-sourced information only as narrative/contextual grounding (cited, not redistributed).

## What GB-BESS v0.1 actually uses

**Synthetic data only**, calibrated to plausible parameter ranges informed by (but not extracted from) the sources above. Every synthetic scenario is explicitly tagged `source_type: synthetic` (master brief §36) and is never presented as derived from or equivalent to real historical GB data. See `docs/suites/gb-bess/SCENARIO_CATALOGUE.md`.

## Open research items

```text
RESEARCH TODO — direct human browser access required (automated fetch blocked)
- Directly read the current Elexon "Copyright: Licence to use BMRS data" and "Copyright:
  Licence to use BMRS APIs" pages in full (not a secondary summary) before any
  Elexon-derived data is used beyond narrative citation. Both pages returned HTTP 403 to
  this project's automated fetch tool on 2026-09-08; a maintainer with normal browser
  access should complete this check.
- Resolve the commercial-vs-non-commercial inconsistency noted above between secondary
  summaries of the two pages.
- If Elexon data is ever frozen into the benchmark (Phase 5), determine the correct
  attribution format required by Elexon's terms (a secondary source suggests "Contains
  BMRS data (c) Elexon Limited copyright and database right [year]", unconfirmed against
  primary text), and complete a full docs/data/DATA_PROVENANCE.md entry per the schema in
  docs/architecture/DATA_MODEL.md.
- Assess whether NESO publishes any open, licensed historical ANM/curtailment event data
  that could ground NET-family scenario parameter ranges more precisely than the current
  qualitative/narrative grounding in GB_SPECIFICITY.md.
```

## Relationship to other documents

This document is the source-survey layer; `docs/data/DATA_PROVENANCE.md` is where an actually-retrieved, frozen dataset's full provenance record would be documented (none exist yet); `DATA_LICENSES.md` (repository root) is the top-level licence summary a downstream user reads first.
