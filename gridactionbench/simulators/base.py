"""SimulatorAdapter interface. See docs/architecture/adr/ADR-003-simulator-abstraction.md.

Exactly two methods, by design — no simulator implementation may add a physical-asset
addressing capability to this interface (docs/architecture/SECURITY.md, ADR-015).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from gridactionbench.schemas.action import AgentActionV1
from gridactionbench.schemas.observation import BatteryState


@dataclass(frozen=True)
class StepResult:
    """Result of one deterministic simulation step.

    energy_stored_delta_mwh is the signed, battery-side energy change: positive for a net
    increase in stored energy (CHARGE), negative for a net decrease (DISCHARGE), zero for
    IDLE/ESCALATE. Exposed explicitly (not just resulting_soc) so property tests can assert
    the energy-conservation invariant directly — docs/suites/gb-bess/SPECIFICATION.md §9.4,
    docs/testing/TEST_STRATEGY.md "Physical invariants."
    """

    resulting_soc: float
    energy_stored_delta_mwh: float


class SimulatorAdapter(Protocol):
    def step(
        self, battery: BatteryState, action: AgentActionV1, dt_hours: float, seed: int | None = None
    ) -> StepResult: ...

    def validate_action(self, battery: BatteryState, action: AgentActionV1) -> bool:
        """Hard-constraint pre-check only — see gridactionbench.core.validator for the
        Action Validator that actually gates simulator execution. This method exists on
        the interface for adapters that want to expose a cheap validity pre-check; the
        canonical, evaluator-driven check lives in the Action Validator, not here."""
        ...
