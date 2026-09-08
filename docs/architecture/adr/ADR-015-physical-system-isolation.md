# ADR-015: Physical-System Isolation

**Status:** Proposed — this ADR records an architectural constraint treated as non-negotiable, not a trade-off among options.

## Context
Master brief §57 requires that no GB-BESS v0.1 component be capable of issuing commands to a physical energy asset or operational energy-system interface.

## Decision
`SimulatorAdapter` (`docs/architecture/ARCHITECTURE.md`) and every schema in `docs/suites/gb-bess/SPECIFICATION.md` are structurally incapable of addressing a real-world endpoint: no device-identifier, credential, or network-endpoint field exists anywhere in `EnergyObservationV1`, `AgentActionV1`, or the `SimulatorAdapter` interface. No SCADA/EMS/DERMS client library is a dependency of `gridactionbench/`. Full enumeration and enforcement mechanism in `docs/architecture/SECURITY.md`.

## Alternatives considered
There is no alternative under consideration here — this ADR exists to make the constraint an explicit, reviewable architectural record (so any future PR introducing a network-addressable field or a SCADA dependency is automatically a deviation from a documented decision, not an ambiguous judgment call at review time), not to weigh trade-offs between isolation and some other property. Master brief §57 states this as a hard requirement for v0.1, and no phase of the project plan (Phase 0-11) calls for relaxing it.

## Consequences
- Positive: GB-BESS v0.1 carries no real-world operational risk by construction; this is also a credibility asset when engaging with DESNZ/Ofgem-adjacent audiences (`docs/project/PID.md`, "Relationship with DESNZ/Ofgem") who would otherwise reasonably ask about exactly this risk.
- Negative: none — this is a scope boundary, not a capability trade-off; if a future, explicitly separate project phase ever wanted shadow-mode or sandboxed real-system observation (master brief §64's "shadow / controlled testing" step in the regulatory-sandbox pipeline), that would be an entirely new, separately-approved architecture, explicitly out of GB-BESS v0.1's scope.
