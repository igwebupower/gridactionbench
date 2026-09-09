"""EnergyObservationV1 — the agent-visible schema.

Field listing and semantics: docs/suites/gb-bess/SPECIFICATION.md §2.
Per that specification's Phase 0.5 note: the fields under `telemetry` describe what was
OBSERVED. Whether a given age/status counts as "too stale to act on" is never decided by
this schema — it is decided per-scenario by that scenario's own `information_requirements`
block (see gridactionbench.core.scenario.InformationRequirements).
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BatteryState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    soc: float = Field(ge=0.0, le=1.0)
    capacity_mwh: float = Field(gt=0.0)
    min_soc: float = Field(ge=0.0, le=1.0)
    max_soc: float = Field(ge=0.0, le=1.0)
    max_charge_mw: float = Field(ge=0.0)
    max_discharge_mw: float = Field(ge=0.0)
    charge_efficiency: float = Field(gt=0.0, le=1.0)
    discharge_efficiency: float = Field(gt=0.0, le=1.0)


class NetworkState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    import_headroom_mw: Optional[float] = None
    export_headroom_mw: Optional[float] = None


class MarketState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reference_price_gbp_mwh: Optional[float] = None
    # Added 2026-09-09 (docs/benchmark/STRESS_DIMENSIONS.md, U1 — forecast uncertainty): a
    # previously-issued forecast for this step's price, distinct from the actual/real-time
    # reference_price_gbp_mwh above. None for every scenario/episode not declaring one —
    # see docs/suites/gb-bess/SPECIFICATION.md §2 for the full field note.
    price_forecast_gbp_mwh: Optional[float] = None


class TelemetryFieldStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")

    soc: str = "fresh"
    network: str = "fresh"
    market: str = "fresh"


class TelemetryAgeSeconds(BaseModel):
    model_config = ConfigDict(extra="forbid")

    soc: Optional[int] = None
    network: Optional[int] = None


class Telemetry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field_status: TelemetryFieldStatus = Field(default_factory=TelemetryFieldStatus)
    age_seconds: TelemetryAgeSeconds = Field(default_factory=TelemetryAgeSeconds)
    missing_fields: list[str] = Field(default_factory=list)
    quality_flags: list[str] = Field(default_factory=list)
    # Second-reading support for DATA-CONFLICT-SOC-001-style scenarios (GB-BESS-DATA-016,
    # GB-BESS-HUM-019). v0.1 supports exactly two SOC readings (docs/suites/gb-bess/
    # EVALUATION_SPEC.md, DATA-CONFLICT-SOC-001 limitations) — N-way conflict is a future
    # extension, not modeled here.
    soc_reading_1: Optional[float] = None
    soc_reading_2: Optional[float] = None


class TemporaryLimits(BaseModel):
    model_config = ConfigDict(extra="forbid")

    charge_prohibited: bool = False
    discharge_prohibited: bool = False
    max_power_override_mw: Optional[float] = None


class OperationalPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reserve_soc: Optional[float] = None
    temporary_limits: TemporaryLimits = Field(default_factory=TemporaryLimits)
    approval_required: bool = False


class EnergyObservationV1(BaseModel):
    """Agent-visible observation. See docs/suites/gb-bess/SPECIFICATION.md §2."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = "1.1.0"
    benchmark: str = "gridactionbench"
    benchmark_version: str
    suite: str = "gb-bess"
    suite_version: str

    scenario_id: str
    timestamp: datetime

    battery: BatteryState
    network: NetworkState = Field(default_factory=NetworkState)
    market: MarketState = Field(default_factory=MarketState)
    telemetry: Telemetry = Field(default_factory=Telemetry)
    operational_policy: OperationalPolicy = Field(default_factory=OperationalPolicy)

    # Adversarial/injected content — present only on ADV-family scenarios
    # (docs/suites/gb-bess/SCENARIO_CATALOGUE.md, GB-BESS-ADV-018). Never authoritative;
    # never parsed by any evaluator's pass/fail logic (docs/benchmark/SPECIFICATION.md §12).
    injected_field: Optional[str] = None
