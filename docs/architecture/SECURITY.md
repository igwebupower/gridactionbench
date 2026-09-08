# Security — Physical-System Isolation

**Status:** Draft — Phase 0. This is an architectural guarantee, not a policy aspiration.

## The guarantee

**No component in GB-BESS v0.1 may issue commands to a physical energy asset or operational energy-system interface.** GB-BESS v0.1 is simulation-only.

## What is not implemented, by design

- SCADA command interfaces
- EMS (Energy Management System) write interfaces
- Inverter control interfaces
- DNO control interfaces
- Live DERMS write access
- Market bidding execution (no connection to any real Balancing Mechanism, exchange, or trading venue)
- Physical asset credentials of any kind (no API keys, certificates, or network access scoped to a real BESS, DNO, or NESO operational system are used, stored, or referenced anywhere in this codebase)

## How the architecture enforces this, not just states it

- The `SimulatorAdapter` interface (`docs/architecture/ARCHITECTURE.md`) has no method that accepts a real-world endpoint, credential, or device identifier — its entire input/output surface is `(pre_state, action) -> post_state`, operating purely on in-memory or file-backed simulated state.
- `EnergyObservationV1` and `AgentActionV1` (`docs/suites/gb-bess/SPECIFICATION.md`) contain no fields for physical-device addressing (no IP addresses, device IDs, SCADA point identifiers, or control-system endpoints) — the schemas are structurally incapable of routing an action anywhere but the simulator.
- No dependency on any commercial or open-source SCADA/EMS/DERMS client library is introduced anywhere in `gridactionbench/`.
- Any future `SimulatorAdapter` implementation for a real power-system simulator (e.g. a PyPSA- or Grid2Op-backed adapter, noted as a future possibility in `docs/architecture/adr/ADR-003-simulator-abstraction.md`) is explicitly scoped to *simulation* engines, not live control systems — this document's guarantee extends to any such future adapter by definition, not merely to `SimpleBessSimulator`.

## Threat model relationship

Physical-system isolation is an architectural property, distinct from the benchmark-integrity threats catalogued in `docs/benchmark/THREAT_MODEL.md`. This document exists because master brief §57 requires it to be stated and enforced explicitly, independent of and prior to any discussion of benchmark-gaming or contamination risk.

## Review obligation

Any pull request introducing a new `SimulatorAdapter`, a new dependency with network-call capability, or any code path that could plausibly reach a real operational endpoint must be reviewed against this document before merge, per the contribution governance in `GOVERNANCE.md`. This is a standing review obligation, not a one-time Phase 0 checklist item.
