# GB Context — GB-BESS v0.1

**Status:** Draft — Phase 0
**Purpose:** a short primer on the Great Britain electricity-system institutions and mechanisms GB-BESS scenarios are grounded in, for readers (including reviewers and contributors) without GB power-sector background. This is background reading, not a licensing or provenance document — see `GB_SPECIFICITY.md` for the evidenced claims and `docs/data/DATA_SOURCES.md` for licensing.

## Institutions referenced by GB-BESS scenario design

| Institution | Role | Relevance to GB-BESS |
|---|---|---|
| **NESO** (National Energy System Operator) | GB's electricity system operator (transmission-level), responsible for balancing supply and demand in real time, operating the Balancing Mechanism, and coordinating with DNOs on network capacity (Technical Limits, ANM) and the connections queue (Gate 2 reform) | Source of the network-headroom / ANM curtailment concept behind the NET scenario family; source of connections-queue context behind OPS scenario motivation |
| **DNOs** (Distribution Network Operators, regional) | Own and operate the local distribution networks most GB-connected BESS assets physically connect to; operate ANM schemes locally under Technical Limits agreed with NESO | Direct real-world analogue of `network.import_headroom_mw` / `network.export_headroom_mw` and of "temporary restriction imposed by operating policy" (OPS family) |
| **Elexon** | Runs the Balancing and Settlement Code (BSC); operates the Balancing Mechanism Reporting Service (BMRS), the primary source of GB wholesale/imbalance settlement price data | Source of the half-hourly settlement-period convention and the reference-price mechanic behind the MKT scenario family |
| **Ofgem** | GB energy regulator; sets network price controls, licence conditions, and (jointly with DESNZ) connections-reform policy | Source of policy context on battery oversubscription and connections reform (see `GB_SPECIFICITY.md`, Feature 3) |
| **DESNZ** (Department for Energy Security and Net Zero) | UK government department responsible for energy policy, including the Clean Power 2030 Action Plan and the Clean Flexibility Roadmap | Same as above; also the intended eventual audience for the Phase 12 evidence report (master brief §80) — GridActionBench does not claim DESNZ endorsement |

## How this maps to the benchmark's scenario taxonomy

- **NET** (network constraints) scenarios are modeled on DNO/NESO Active Network Management and Technical Limits — a real, named GB mechanism, not a generic "grid capacity" abstraction.
- **MKT** (economic objectives) scenarios are modeled on the shape of GB settlement pricing (half-hourly periods, the real possibility of negative prices during oversupply) via Elexon/BMRS, without implementing actual Balancing Mechanism bid/offer mechanics.
- **OPS** (operational policy) scenarios draw motivating realism from the current GB battery connections-queue and oversubscription situation (DESNZ/Ofgem, 2026) — reserve-SOC and temporary-restriction scenarios are not arbitrary; they reflect a system where more batteries are queued for connection than there is confirmed headroom to serve.
- **PHY, DATA, ADV, HUM** families are largely domain-general and are not claimed as GB-specific (see `GB_SPECIFICITY.md`, "What remains generic").

## What GB-BESS v0.1 explicitly does not model

- Balancing Mechanism bid/offer submission and acceptance mechanics.
- Capacity Market payments or auctions.
- Full BESS revenue-stacking (wholesale arbitrage + ancillary services + Balancing Mechanism, combined).
- Grid Code or Distribution Code compliance testing (protection settings, fault ride-through, frequency response performance standards, etc.).
- Real-time ANM signal protocols or DERMS command formats.
- Any live connection to NESO, DNO, or Elexon systems — see `docs/architecture/SECURITY.md` for the explicit physical/operational isolation guarantee.

This is a **behavioural evaluation environment informed by real GB institutional context**, not a certified model of any of these systems. See `docs/benchmark/BENCHMARK_CARD.md` for the full scope statement and out-of-scope uses.
