"""Decision Record — the immutable atomic unit of evidence. See docs/benchmark/
SPECIFICATION.md §7 and docs/architecture/adr/ADR-009-decision-record-format.md.

Serialization: JSONL, one record per line, append-only per run.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from gridactionbench import FRAMEWORK_VERSION
from gridactionbench.evaluators.base import EvaluationResult
from gridactionbench.evaluators.gb_bess import EVALUATOR_SET_VERSION
from gridactionbench.schemas.action import AgentActionV1
from gridactionbench.schemas.observation import EnergyObservationV1
from gridactionbench.simulators.base import StepResult
from gridactionbench.simulators.simple_bess import SIMULATOR_VERSION


class DecisionRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    benchmark_version: str = FRAMEWORK_VERSION
    suite: str = "gb-bess"
    suite_version: str
    evaluator_set_version: str = EVALUATOR_SET_VERSION
    simulator_version: str = SIMULATOR_VERSION
    run_id: str

    scenario_id: str
    scenario_version: str
    scenario_source_type: str

    agent_id: str
    agent_version: str
    agent_type: str

    observation: EnergyObservationV1
    raw_agent_response: Optional[dict[str, Any]] = None
    parsed_action: Optional[AgentActionV1] = None
    schema_valid: bool
    schema_repairs: list[str] = []

    simulator_pre_state: dict[str, Any]
    simulator_post_state: Optional[dict[str, Any]] = None

    evaluation_results: list[dict[str, Any]] = []
    hard_constraint_valid: Optional[bool] = None
    ucv: bool = False
    self_reported_high_confidence_ucv: bool = False

    errors: list[str] = []

    dt_hours: float
    random_seed: Optional[int] = None
    git_commit: Optional[str] = None
    runtime_version: str
    environment_metadata: dict[str, str] = {}

    timestamp: datetime


def evaluation_result_to_dict(r: EvaluationResult) -> dict[str, Any]:
    return {
        "eval_id": r.eval_id,
        "version": r.version,
        "constraint_class": r.constraint_class.value if r.constraint_class else None,
        "severity": r.severity.value,
        "ucv_eligible": r.ucv_eligible,
        "result": r.result.value,
        "evidence": r.evidence,
        "contributes_to_ucv": r.contributes_to_ucv,
    }


def step_result_to_dict(s: StepResult) -> dict[str, Any]:
    return {"resulting_soc": s.resulting_soc, "energy_stored_delta_mwh": s.energy_stored_delta_mwh}


class JsonlWriter:
    """Append-only JSONL writer for a Run's Decision Records."""

    def __init__(self, path: Path | str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, record: DecisionRecord) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(record.model_dump_json())
            f.write("\n")

    def read_all(self) -> list[DecisionRecord]:
        if not self.path.exists():
            return []
        records = []
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(DecisionRecord(**json.loads(line)))
        return records
