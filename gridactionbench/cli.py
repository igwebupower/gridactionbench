"""Minimal CLI. See master brief §68 (Phase 1 spike scope: no frontend, CLI only)."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from baselines.always_escalate.agent import AlwaysEscalateAgent
from baselines.always_idle.agent import AlwaysIdleAgent
from baselines.rule_based.agent import RuleBasedAgent
from baselines.seeded_failures.always_charge import AlwaysChargeAgent
from baselines.seeded_failures.ignore_minimum_soc import IgnoreMinimumSOCAgent
from baselines.seeded_failures.ignore_network import IgnoreNetworkAgent
from baselines.seeded_failures.never_escalate import NeverEscalateAgent
from baselines.seeded_failures.prompt_injection_victim import PromptInjectionVictimAgent
from baselines.seeded_failures.revenue_first_constraint_ignoring import RevenueFirstConstraintIgnoringAgent
from baselines.seeded_failures.trust_all_telemetry import TrustAllTelemetryAgent
from gridactionbench.core.decision_record import JsonlWriter
from gridactionbench.core.scenario import load_scenario_dir
from gridactionbench.reporting.report import build_report, render_text
from gridactionbench.runners.single_step import run_single_step

app = typer.Typer(help="GridActionBench CLI")

AGENTS = {
    "always-idle": lambda dt_hours: AlwaysIdleAgent(),
    "always-escalate": lambda dt_hours: AlwaysEscalateAgent(),
    "rule-based": lambda dt_hours: RuleBasedAgent(dt_hours=dt_hours),
    "always-charge": lambda dt_hours: AlwaysChargeAgent(),
    "ignore-network": lambda dt_hours: IgnoreNetworkAgent(dt_hours=dt_hours),
    "ignore-minimum-soc": lambda dt_hours: IgnoreMinimumSOCAgent(dt_hours=dt_hours),
    "revenue-first-constraint-ignoring": lambda dt_hours: RevenueFirstConstraintIgnoringAgent(dt_hours=dt_hours),
    "trust-all-telemetry": lambda dt_hours: TrustAllTelemetryAgent(dt_hours=dt_hours),
    "never-escalate": lambda dt_hours: NeverEscalateAgent(dt_hours=dt_hours),
    "prompt-injection-victim": lambda dt_hours: PromptInjectionVictimAgent(dt_hours=dt_hours),
}


@app.command()
def run(
    scenario_dir: Path = typer.Argument(..., help="Directory of scenario YAML files"),
    agent: str = typer.Option("rule-based", help=f"One of: {', '.join(AGENTS)}"),
    dt_hours: float = typer.Option(0.5, help="Simulator timestep in hours (SPECIFICATION.md §9.6)"),
    output: Optional[Path] = typer.Option(None, help="JSONL output path for Decision Records"),
) -> None:
    """Run every scenario in SCENARIO_DIR against AGENT and print a per-dimension report."""
    if agent not in AGENTS:
        typer.echo(f"Unknown agent '{agent}'. Choose from: {', '.join(AGENTS)}")
        raise typer.Exit(code=1)

    scenarios = load_scenario_dir(scenario_dir)
    agent_instance = AGENTS[agent](dt_hours)

    records = []
    writer = JsonlWriter(output) if output else None
    for scenario in scenarios:
        record = run_single_step(scenario, agent_instance, dt_hours)
        records.append(record)
        if writer:
            writer.write(record)

    report = build_report(records)
    typer.echo(f"Agent: {agent}  |  Scenarios: {len(records)}  |  dt_hours: {dt_hours}")
    typer.echo("")
    typer.echo(render_text(report))


@app.command("list-scenarios")
def list_scenarios(scenario_dir: Path = typer.Argument(...)) -> None:
    """List every scenario in SCENARIO_DIR."""
    for scenario in load_scenario_dir(scenario_dir):
        typer.echo(f"{scenario.scenario_id}  [{scenario.family}]  review_status={scenario.review_status}")


if __name__ == "__main__":
    app()
