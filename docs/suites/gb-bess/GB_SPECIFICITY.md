# GB Specificity — GB-BESS v0.1

**Status:** Draft — Phase 0 required deliverable (master brief §33)
**Purpose:** answer, with evidence rather than assertion, the question: *what specifically makes GB-BESS a Great Britain benchmark rather than a generic battery benchmark denominated in GBP?*

This document does not claim GB-BESS v0.1 implements complete Grid Code or Distribution Code compliance. It documents which design choices are genuinely traceable to GB institutions, mechanisms, or policy, which are generic-but-plausible, and which are currently GBP-only decoration that should either be strengthened or explicitly labeled as non-GB-specific.

---

## Format

For each claimed GB-specific feature:

```text
feature / source / source_organisation / why_GB_specific / benchmark_relevance / simplification / licence / limitations
```

---

### Feature 1 — Network headroom modeled as a distribution-level, dynamically curtailable constraint (not a fixed connection capacity)

- **source:** "Active Network Management (ANM): Opportunities and risks for Smart Local Energy Systems" (Energy Systems Catapult); ENA "Grid Supply Point Technical Limits for accelerated non-firm connections"; Aurora Power, "Understanding DNO/DSO Curtailment"
- **source_organisation:** Energy Systems Catapult; Energy Networks Association (ENA); Distribution Network Operators (DNOs) collectively
- **why_GB_specific:** Great Britain's distribution network operators run live **Active Network Management (ANM)** schemes and **Technical Limits** agreed between NESO and individual DNOs at Grid Supply Points, under which non-firm-connected assets (including BESS) accept automated, real-time curtailment of import/export in exchange for faster, cheaper grid connection. This is a specific institutional mechanism of the GB distribution system, not a universal feature of electricity grids — it is a direct consequence of GB's connection-queue and non-firm-connection policy landscape (see Feature 3).
- **benchmark_relevance:** This is the direct real-world referent for GridActionBench's `network.import_headroom_mw` / `network.export_headroom_mw` fields (`EnergyObservationV1`) and the entire NET scenario family (§17 of the master brief) — specifically the "changing headroom" and "stale headroom" scenario types. Without ANM as a real mechanism, "network headroom that changes mid-episode and that the agent must respect even when it conflicts with a strong price incentive" would be an arbitrary simulation choice; with it, it is a direct, named GB operational reality.
- **simplification:** GB-BESS v0.1 models headroom as a single scalar MW value with a staleness/freshness flag. Real ANM schemes involve multi-signal telemetry, DERMS instructions, and per-GSP Technical Limit curves that vary by time of day and system condition. GB-BESS does not model ANM signal protocols, DERMS command formats, or multi-GSP topology.
- **licence:** N/A — this is a design pattern, not a redistributed dataset. Cited documents are publicly accessible industry/consultancy publications, not government open data; no redistribution of their content is planned.
- **limitations:** GB-BESS's headroom constraint is a **simplified conceptual model** of ANM/Technical Limits, not a certified representation of any real DNO's ANM logic. It should not be used to argue that an agent would be safe under a real DNO's ANM scheme.

---

### Feature 2 — Reference price signal grounded in GB wholesale/balancing market structure (Elexon BMRS)

- **source:** Elexon, "Making electricity market data more openly available"; Elexon BMRS API documentation (`developer.data.elexon.co.uk`, `bmrs.elexon.co.uk`)
- **source_organisation:** Elexon (GB Balancing and Settlement Code Company)
- **why_GB_specific:** The Balancing Mechanism Reporting Service (BMRS) is GB's specific, named settlement and balancing data system, publishing half-hourly (48 settlement periods/day) wholesale and imbalance price data under the GB Balancing and Settlement Code. This half-hourly settlement-period structure — and the existence of negative imbalance/system prices during periods of oversupply — is a real, documented characteristic of the GB market, not an arbitrary synthetic assumption.
- **benchmark_relevance:** Directly grounds the MKT scenario family's core mechanic (§19 of the master brief): negative reference price, high positive reference price, price-vs-constraint conflicts. GB-BESS's `market.reference_price_gbp_mwh` field and its half-hourly timestep design are modeled on this real settlement structure, even though v0.1 uses synthetic or frozen historical price series rather than live BMRS calls (per master brief §34, no live-API dependency for official runs).
- **simplification:** GB-BESS v0.1 does **not** implement Balancing Mechanism bid/offer mechanics, imbalance settlement, Capacity Market payments, or any BESS revenue-stacking model (ancillary services, Balancing Mechanism participation, wholesale arbitrage combined). It uses a single scalar reference price per timestep as an economic-incentive signal only. Master brief §19 explicitly forbids claiming this represents complete GB BESS revenue optimization, and this document reiterates that prohibition.
- **licence:** BMRS/Insights Solution data is governed by the **BMRS Data Licence Terms** and **BMRS API Terms of Use Policy** (Elexon); access requires a free Elexon account and API key. **Redistribution terms were not fully confirmed in this research pass** (the primary licence terms page returned an access error during research; only a secondary summary was available). See `docs/data/DATA_SOURCES.md` for the explicit TODO — no BMRS-derived data will be committed to this repository until the licence is directly confirmed.
- **limitations:** If/when real historical BMRS price data is frozen into the benchmark (Phase 5, master brief §73), it must go through the full retrieval → validation → transformation → checksum pipeline (§34) with the licence question resolved first, per the "do not commit if redistribution rights are unclear" rule (§35).

---

### Feature 3 — Battery connection-queue and oversubscription context (Clean Power 2030 / Connections Reform)

- **source:** "Open letter from DESNZ and Ofgem on connections reform delivery" (16 April 2026, GOV.UK); DESNZ, "Clean Flexibility Roadmap" (2026 update)
- **source_organisation:** Department for Energy Security and Net Zero (DESNZ); Ofgem
- **why_GB_specific:** As of the 2026 open letter, DESNZ and Ofgem state they remain committed to a market environment supporting **23–27 GW of grid-scale batteries by 2030** (the Clean Power 2030 Action Plan range), against a connection queue that — after NESO's Gate 2 reform filtered out 221 GW of non-viable projects — still holds roughly **14.8 GW** of battery capacity above the top of that 2030 range and **61.7 GW** above projected 2035 system need. This specific numeric oversupply-vs-target relationship, and mechanisms like the proposed CMP470 "Oversubscribed Technologies Commitment Fee," are concrete, dated GB policy facts, not generic industry background.
- **benchmark_relevance:** This context is the real-world justification for *why* operational and network constraints (OPS and NET families) matter more, not less, as GB battery deployment scales — a system with many more connected batteries than headroom to serve them is exactly the system where ANM curtailment, reserve-SOC operational policy, and appropriate escalation become operationally significant, rather than academic edge cases. This grounds the benchmark's emphasis (master brief §5, §18) that "physically possible does not necessarily mean operationally permitted" in a documented, current GB policy reality rather than an assumed one.
- **simplification:** GB-BESS v0.1 does not model the connection queue, Gate 2 process, or CMP470 mechanics themselves — it uses this context only as narrative/motivational grounding for why OPS-family scenarios (reserve SOC, temporary restrictions, approval requirements) are realistic rather than contrived.
- **licence:** GOV.UK publications are typically released under the **Open Government Licence (OGL)** — permits copying, publishing, distributing, and adapting, including commercial use, with attribution to the information provider and source, and (where possible) a link to the source and the OGL itself. No redistribution of the source documents themselves is planned; this document cites and summarizes only.
- **limitations:** This is time-sensitive policy context (explicitly dated 2026) that will go stale; GB-BESS v0.1's Benchmark Card should note the context's currency date and flag that later benchmark versions should re-verify rather than assume continuity of these figures.

---

### Feature 4 — Currency and settlement-period timestep convention

- **source:** Elexon BSC (see Feature 2)
- **source_organisation:** Elexon
- **why_GB_specific:** GBP as unit and 30-minute settlement periods (48 per day) as the natural timestep granularity are both direct artifacts of the GB Balancing and Settlement Code, not arbitrary choices.
- **benchmark_relevance:** Sets `market.reference_price_gbp_mwh` units and informs (but does not yet fix, pending simulator design work in Phase 1) the `SimpleBessSimulator` timestep.
- **simplification:** Use of GBP and a half-hour-like timestep alone is explicitly called out in this document's own opening question as *insufficient* to establish GB specificity by itself — it is necessary but not sufficient, and is listed here as one of four features precisely so it is not mistaken for the whole answer.
- **licence:** N/A (unit/convention choice, not redistributed data).
- **limitations:** None beyond the general caution above.

---

## What remains generic (not claimed as GB-specific)

- The physical battery model (SOC bounds, charge/discharge power limits, round-trip efficiency) is generic BESS physics, not GB-specific, and is not claimed as such.
- The core action space (CHARGE/DISCHARGE/IDLE/ESCALATE) and the Oracle/Observation/Evaluation architecture are domain-general benchmark design, applicable to any electricity market.
- Adversarial (ADV) and data-quality (DATA) scenario families are generic robustness testing, not GB-specific, though they are instantiated using GB-flavored surface details (e.g., a fabricated "NESO override" instruction in an ADV scenario) for realism.

## Honest self-assessment

GB-BESS v0.1's GB specificity is currently **contextual and structural** (real GB institutions, mechanisms, and current policy numbers inform which scenarios exist and why they matter) rather than **data-grounded** (no real, licensed GB price or network data is yet frozen into the benchmark — that is Phase 5 work, explicitly gated on licence confirmation). This document should be revisited and strengthened once Phase 5 (GB Data) either freezes real BMRS-derived data under a confirmed licence, or confirms that synthetic data calibrated to realistic GB parameter ranges is the permanent v0.1 approach. Until then, GB-BESS's honest claim is: *"designed around real, current GB market and network mechanisms, using synthetic data calibrated to plausible GB parameter ranges,"* not *"trained or tested on real GB market data."*
