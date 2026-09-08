"""AgentActionV1 — the agent-produced schema.

Field listing, validation rules: docs/suites/gb-bess/SPECIFICATION.md §3.
Sign convention: docs/suites/gb-bess/SPECIFICATION.md §9.2 — power_mw is always
non-negative; direction comes from `action`, never from the sign of power_mw.
Confidence: self-reported and uncalibrated — see docs/benchmark/SPECIFICATION.md §8 and
docs/benchmark/METHODOLOGY.md §4. Never used to determine a pass/fail verdict.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ActionType(str, Enum):
    CHARGE = "CHARGE"
    DISCHARGE = "DISCHARGE"
    IDLE = "IDLE"
    ESCALATE = "ESCALATE"


class ReasonCode(str, Enum):
    """Machine-readable ESCALATE reason codes.

    Compiled from docs/suites/gb-bess/SPECIFICATION.md §3's base set plus the codes used
    across docs/suites/gb-bess/SCENARIO_CATALOGUE.md's 20 initial scenarios. Free text alone
    is never sufficient for ESCALATE (SPECIFICATION.md §3).
    """

    TELEMETRY_CONFLICT = "TELEMETRY_CONFLICT"
    MISSING_CRITICAL_DATA = "MISSING_CRITICAL_DATA"
    STALE_CRITICAL_DATA = "STALE_CRITICAL_DATA"
    IMPLAUSIBLE_TELEMETRY = "IMPLAUSIBLE_TELEMETRY"
    AMBIGUOUS_POLICY = "AMBIGUOUS_POLICY"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    TOOL_FAILURE = "TOOL_FAILURE"
    UNSUPPORTED_CONDITION = "UNSUPPORTED_CONDITION"
    SUSPECTED_ADVERSARIAL_INPUT = "SUSPECTED_ADVERSARIAL_INPUT"


class AgentActionV1(BaseModel):
    """Structured agent output. Strictly validated — see module docstring."""

    model_config = ConfigDict(extra="forbid")

    action: ActionType
    power_mw: Optional[float] = None
    reason_code: Optional[ReasonCode] = None
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    optional_explanation: Optional[str] = None

    # Populated by the runner post-validation, not by the agent itself — flags a
    # zero-power CHARGE/DISCHARGE as a schema irregularity per SPECIFICATION.md §9.8,
    # without treating it as schema_valid=False (zero is a valid float, not malformed).
    zero_power_irregularity: bool = False

    @model_validator(mode="after")
    def _validate_action_rules(self) -> "AgentActionV1":
        if self.power_mw is not None and self.power_mw < 0.0:
            raise ValueError(
                "power_mw must be non-negative (SPECIFICATION.md §9.2): direction comes "
                "from `action`, never from the sign of power_mw."
            )

        if self.action in (ActionType.CHARGE, ActionType.DISCHARGE):
            if self.power_mw is None:
                raise ValueError(f"{self.action} requires a present power_mw.")
            if self.power_mw == 0.0:
                object.__setattr__(self, "zero_power_irregularity", True)

        elif self.action is ActionType.IDLE:
            if self.power_mw not in (None, 0.0):
                raise ValueError(
                    "IDLE must not request meaningful power (any non-zero power_mw on "
                    "IDLE is a schema violation)."
                )

        elif self.action is ActionType.ESCALATE:
            if self.reason_code is None:
                raise ValueError(
                    "ESCALATE requires a machine-readable reason_code; free text alone "
                    "is insufficient (SPECIFICATION.md §3)."
                )

        return self
