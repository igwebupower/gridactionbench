"""Draws candidate official holdout instances from the public generator templates using a
private seed, filters them through the acceptance criteria (acceptance.py), and writes
only the accepted instances plus a manifest to a git-ignored output directory — never the
public repository's git history (docs/benchmark/PUBLIC_PRIVATE_POLICY.md).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from gridactionbench.holdouts.acceptance import AcceptanceResult, check_acceptance
from gridactionbench.scenarios.generator import TEMPLATES, ScenarioTemplate, generate

DEFAULT_OUTPUT_DIR = Path("holdouts_private")
DEFAULT_N_PER_TEMPLATE = 5


@dataclass
class HoldoutGenerationSummary:
    candidates_generated: int
    accepted: int
    rejected: int
    sensitivity_flagged: int
    rejection_reasons: dict[str, int] = field(default_factory=dict)


def generate_holdouts(
    private_seed: int,
    n_per_template: int = DEFAULT_N_PER_TEMPLATE,
    templates: list[ScenarioTemplate] = TEMPLATES,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> HoldoutGenerationSummary:
    """The private seed must come from gridactionbench.holdouts.private_seed.
    resolve_private_seed() at the actual call site (CLI) — accepted as a plain argument
    here so this function stays unit-testable with an explicit, non-secret test seed."""
    candidates = generate(templates=templates, n_per_template=n_per_template, seed=private_seed)
    results: list[AcceptanceResult] = [check_acceptance(s) for s in candidates]
    accepted_pairs = [(s, r) for s, r in zip(candidates, results) if r.accepted]

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "private_seed": private_seed,
        "n_per_template": n_per_template,
        "candidates_generated": len(candidates),
        "accepted": len(accepted_pairs),
        "instances": [
            {"scenario_id": s.scenario_id, "sensitivity_flagged": r.sensitivity_flagged} for s, r in accepted_pairs
        ],
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    for scenario, _result in accepted_pairs:
        (output_dir / f"{scenario.scenario_id}.json").write_text(scenario.model_dump_json(indent=2), encoding="utf-8")

    rejection_reasons: dict[str, int] = {}
    for result in results:
        for reason in result.reasons:
            rejection_reasons[reason] = rejection_reasons.get(reason, 0) + 1

    return HoldoutGenerationSummary(
        candidates_generated=len(candidates),
        accepted=len(accepted_pairs),
        rejected=len(candidates) - len(accepted_pairs),
        sensitivity_flagged=sum(1 for r in results if r.sensitivity_flagged),
        rejection_reasons=rejection_reasons,
    )
