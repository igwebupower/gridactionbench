"""Integration tests: the full Scenario -> Observation -> Agent -> Action -> Simulator ->
Evaluation -> Decision Record pipeline, wired together end-to-end.

See docs/testing/TEST_STRATEGY.md, "Integration tests."
"""

from __future__ import annotations

from pathlib import Path

from gridactionbench.agents.rule_based import RuleBasedAgent
from gridactionbench.core.decision_record import JsonlWriter
from gridactionbench.core.scenario import load_scenario_dir
from gridactionbench.runners.single_step import run_single_step

SCENARIO_DIR = Path(__file__).resolve().parent.parent.parent / "suites" / "gb_bess" / "v0_1" / "scenarios"
DT_HOURS = 0.5


def test_every_scenario_runs_end_to_end_without_error():
    scenarios = load_scenario_dir(SCENARIO_DIR)
    assert len(scenarios) == 20
    agent = RuleBasedAgent(dt_hours=DT_HOURS)
    for scenario in scenarios:
        record = run_single_step(scenario, agent, DT_HOURS)
        assert record.scenario_id == scenario.scenario_id
        assert record.schema_valid is True
        assert record.simulator_post_state is not None
        assert record.errors == []


def test_scenario_id_preserved_through_to_decision_record():
    scenarios = load_scenario_dir(SCENARIO_DIR)
    agent = RuleBasedAgent(dt_hours=DT_HOURS)
    for scenario in scenarios:
        record = run_single_step(scenario, agent, DT_HOURS)
        assert record.scenario_id == scenario.scenario_id
        assert record.scenario_version == scenario.scenario_version


def test_every_evaluation_result_carries_eval_id_and_version():
    scenarios = load_scenario_dir(SCENARIO_DIR)
    agent = RuleBasedAgent(dt_hours=DT_HOURS)
    for scenario in scenarios:
        record = run_single_step(scenario, agent, DT_HOURS)
        for result in record.evaluation_results:
            assert result["eval_id"]
            assert result["version"]


def test_decision_records_round_trip_through_jsonl(tmp_path):
    scenarios = load_scenario_dir(SCENARIO_DIR)
    agent = RuleBasedAgent(dt_hours=DT_HOURS)
    writer = JsonlWriter(tmp_path / "run.jsonl")
    for scenario in scenarios:
        writer.write(run_single_step(scenario, agent, DT_HOURS))

    read_back = writer.read_all()
    assert len(read_back) == len(scenarios)
    assert {r.scenario_id for r in read_back} == {s.scenario_id for s in scenarios}


def test_irrelevant_metadata_cannot_alter_physical_verdict():
    """Two scenarios identical except for author/created_date-equivalent metadata must
    produce identical evaluation results — docs/testing/TEST_STRATEGY.md."""
    scenarios = load_scenario_dir(SCENARIO_DIR)
    phy_001 = next(s for s in scenarios if s.scenario_id == "GB-BESS-PHY-001")
    clone = phy_001.model_copy(update={"scenario_id": "GB-BESS-PHY-001-CLONE"})
    agent = RuleBasedAgent(dt_hours=DT_HOURS)
    r1 = run_single_step(phy_001, agent, DT_HOURS)
    r2 = run_single_step(clone, agent, DT_HOURS)
    assert [x["result"] for x in r1.evaluation_results] == [x["result"] for x in r2.evaluation_results]
