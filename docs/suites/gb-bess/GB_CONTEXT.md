# GB Context — GB-BESS v0.1

**Status:** Revised — Phase 0.5 methodology correction pass. This document now holds contextual/motivational GB material that does **not** meet `GB_SPECIFICITY.md`'s benchmark-affecting test (removing it would change no scenario, evaluator, observation field, or parameter distribution) but is nonetheless real, sourced, and useful for understanding why this project matters to a GB audience. Two sections below (connections-queue policy, currency/timestep convention) were moved here from `GB_SPECIFICITY.md` during this pass, where they had been incorrectly presented as benchmark-affecting features.
**Purpose:** a short primer on the Great Britain electricity-system institutions and mechanisms GB-BESS scenarios are grounded in, for readers (including reviewers and contributors) without GB power-sector background. This is background reading, not a licensing or provenance document, and not a claim that any of this material makes the benchmark itself GB-specific — see `GB_SPECIFICITY.md` for the (narrower) evidenced benchmark-affecting claims and `docs/data/DATA_SOURCES.md` for licensing.

## Institutions referenced by GB-BESS scenario design

| Institution | Role | Relevance to GB-BESS |
|---|---|---|
| **NESO** (National Energy System Operator) | GB's electricity system operator (transmission-level), responsible for balancing supply and demand in real time, operating the Balancing Mechanism, and coordinating with DNOs on network capacity (Technical Limits, ANM) and the connections queue (Gate 2 reform) | Source of the network-headroom / ANM curtailment concept behind the NET scenario family; source of connections-queue context behind OPS scenario motivation |
| **DNOs** (Distribution Network Operators, regional) | Own and operate the local distribution networks most GB-connected BESS assets physically connect to; operate ANM schemes locally under Technical Limits agreed with NESO | Direct real-world analogue of `network.import_headroom_mw` / `network.export_headroom_mw` and of "temporary restriction imposed by operating policy" (OPS family) |
| **Elexon** | Runs the Balancing and Settlement Code (BSC); operates the Balancing Mechanism Reporting Service (BMRS), the primary source of GB wholesale/imbalance settlement price data | Source of the half-hourly settlement-period convention and the reference-price mechanic behind the MKT scenario family |
| **Ofgem** | GB energy regulator; sets network price controls, licence conditions, and (jointly with DESNZ) connections-reform policy | Source of policy context on battery oversubscription and connections reform (see "Why this matters to GB policy right now," below — contextual, not a benchmark-affecting feature; corrected Phase 0.5, was previously miscited as `GB_SPECIFICITY.md` Feature 3, which no longer exists there) |
| **DESNZ** (Department for Energy Security and Net Zero) | UK government department responsible for energy policy, including the Clean Power 2030 Action Plan and the Clean Flexibility Roadmap | Same as above; also the intended eventual audience for the Phase 12 evidence report (master brief §80) — GridActionBench does not claim DESNZ endorsement |

## How this maps to the benchmark's scenario taxonomy

- **NET** (network constraints) scenarios are modeled on DNO/NESO Active Network Management and Technical Limits — a real, named GB mechanism, not a generic "grid capacity" abstraction.
- **MKT-adjacent pricing behaviour** (negative price as a core, not exotic, condition — see `GB_SPECIFICITY.md` Feature 2) is a genuinely benchmark-affecting GB instantiation, not merely contextual.
- **OPS** (operational policy) scenarios are *motivated* by the current GB battery connections-queue and oversubscription situation (DESNZ/Ofgem, 2026, see "Why this matters to GB policy right now" above) — but per the Phase 0.5 correction, this motivation is contextual, not benchmark-affecting: the reserve-SOC/temporary-restriction scenario design itself is generic operational-policy modeling, not something that would differ in a non-GB benchmark. Do not read the OPS family as a "GB-specific" family — it is a generically necessary family that happens to be well-motivated by current GB circumstances.
- **PHY, DATA, ADV, HUM** families are domain-general and are not claimed as GB-specific (see `GB_SPECIFICITY.md`, "What remains generic").

## Why this matters to GB policy right now (contextual, not benchmark-affecting)

*Moved from `GB_SPECIFICITY.md` during the Phase 0.5 correction pass — this material explains why the project is topical for a GB audience; it does not change any scenario, evaluator, or parameter in GB-BESS v0.1, and is not cited as a "GB-specific feature" of the benchmark itself.*

As of a 16 April 2026 joint open letter, DESNZ and Ofgem confirmed they remain committed to a market environment supporting **23-27 GW of grid-scale batteries by 2030** (the Clean Power 2030 Action Plan range), against a connection queue that — after NESO's Gate 2 reform filtered out 221 GW of non-viable projects — still holds roughly **14.8 GW** of battery capacity above the top of that 2030 range and **61.7 GW** above projected 2035 system need. A Connection Use of System Code modification proposal (CMP470) proposes an "Oversubscribed Technologies Commitment Fee" to encourage non-viable projects to leave the queue. Source: "Open letter from DESNZ and Ofgem on connections reform delivery" (GOV.UK, 16 April 2026); DESNZ, "Clean Flexibility Roadmap" (2026 update). Access date 2026-09-08.

This is real, current, sourced context for why AI-assisted BESS operational decision-making is a live GB policy topic — a system with many more connected/queued batteries than confirmed network headroom is exactly the system where reserve-SOC policy, temporary restrictions, and appropriate escalation stop being academic. It is presented here, rather than in `GB_SPECIFICITY.md`, because removing this context would not change a single evaluator, scenario parameter, or observation field in GB-BESS v0.1 — the OPS scenario family's design (reserve SOC, temporary restrictions, approval requirements) is generic operational-policy modeling applicable to any regulated grid, motivated equally well without this specific policy backdrop. GOV.UK publications are typically released under the Open Government Licence (OGL) — permitting reuse with attribution; no bulk data is reproduced here, only narrative citation.

## Currency convention (contextual, not benchmark-affecting)

*Partially updated Phase 1: the timestep half of this section has moved back to `GB_SPECIFICITY.md` as Feature 3, since the condition this section itself set for that move — the simulator's timestep actually being fixed to the GB settlement period — is now satisfied (`dt_hours = 0.5` is implemented, not merely discussed). Currency remains here, unchanged.*

GBP as the currency unit is an artifact of the GB Balancing and Settlement Code (Elexon). This, by itself, still does not establish GB specificity — using GBP as a unit label changes no benchmark behaviour on its own, independent of the (now benchmark-affecting) timestep decision documented in `GB_SPECIFICITY.md`, Feature 3.

## What GB-BESS v0.1 explicitly does not model

- Balancing Mechanism bid/offer submission and acceptance mechanics.
- Capacity Market payments or auctions.
- Full BESS revenue-stacking (wholesale arbitrage + ancillary services + Balancing Mechanism, combined).
- Grid Code or Distribution Code compliance testing (protection settings, fault ride-through, frequency response performance standards, etc.).
- Real-time ANM signal protocols or DERMS command formats.
- Any live connection to NESO, DNO, or Elexon systems — see `docs/architecture/SECURITY.md` for the explicit physical/operational isolation guarantee.

This is a **behavioural evaluation environment informed by real GB institutional context**, not a certified model of any of these systems. See `docs/benchmark/BENCHMARK_CARD.md` for the full scope statement and out-of-scope uses.
