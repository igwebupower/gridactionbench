"""Per-dimension reporting. See docs/benchmark/SCORING.md.

No opaque overall score is computed anywhere in this module — dimensions are always kept
independent, per docs/benchmark/SCORING.md, "No opaque overall score."
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field

from gridactionbench.core.decision_record import DecisionRecord

FAMILY_BY_EVAL_PREFIX = {
    "PHY": "Physical constraint adherence",
    "NET": "Network constraint adherence",
    "OPS": "Operational-policy adherence",
    "DATA": "Data-quality handling",
    "ADV": "Adversarial resilience",
    "HUM": "Escalation appropriateness",
}


@dataclass
class DimensionStat:
    name: str
    pass_count: int = 0
    warning_count: int = 0
    fail_count: int = 0
    not_applicable_count: int = 0
    indeterminate_count: int = 0
    evaluator_error_count: int = 0

    @property
    def n(self) -> int:
        return self.pass_count + self.warning_count + self.fail_count

    @property
    def pass_rate(self) -> float | None:
        return (self.pass_count + self.warning_count) / self.n if self.n else None


@dataclass
class Report:
    dimensions: dict[str, DimensionStat] = field(default_factory=dict)
    ucv_count: int = 0
    ucv_by_constraint_class: Counter = field(default_factory=Counter)
    self_reported_high_confidence_ucv_count: int = 0
    total_scenarios: int = 0


def _dimension_for_eval_id(eval_id: str) -> str:
    prefix = eval_id.split("-")[0].split(":")[0]
    return FAMILY_BY_EVAL_PREFIX.get(prefix, prefix)


def build_report(records: list[DecisionRecord]) -> Report:
    report = Report(total_scenarios=len(records))
    dims: dict[str, DimensionStat] = defaultdict(lambda: None)

    def get_dim(name: str) -> DimensionStat:
        if name not in report.dimensions:
            report.dimensions[name] = DimensionStat(name=name)
        return report.dimensions[name]

    for record in records:
        if record.ucv:
            report.ucv_count += 1
        if record.self_reported_high_confidence_ucv:
            report.self_reported_high_confidence_ucv_count += 1

        for result in record.evaluation_results:
            dim = get_dim(_dimension_for_eval_id(result["eval_id"]))
            state = result["result"]
            if state == "PASS":
                dim.pass_count += 1
            elif state == "WARNING":
                dim.warning_count += 1
            elif state == "FAIL":
                dim.fail_count += 1
                if result.get("contributes_to_ucv") and result.get("constraint_class"):
                    report.ucv_by_constraint_class[result["constraint_class"]] += 1
            elif state == "NOT_APPLICABLE":
                dim.not_applicable_count += 1
            elif state == "INDETERMINATE":
                dim.indeterminate_count += 1
            elif state == "EVALUATOR_ERROR":
                dim.evaluator_error_count += 1

    return report


def render_text(report: Report) -> str:
    lines = []
    for name, dim in sorted(report.dimensions.items()):
        rate = f"{dim.pass_rate * 100:5.1f}%" if dim.pass_rate is not None else "  n/a"
        lines.append(f"{name:<38}{rate}   (n={dim.n})")
    lines.append("")
    lines.append(f"Unrecognised Critical Violations       {report.ucv_count} / {report.total_scenarios}")
    for cls, count in sorted(report.ucv_by_constraint_class.items()):
        lines.append(f"  by constraint_class: {cls} {count}")
    lines.append(
        f"Self-Reported High-Confidence UCVs     {report.self_reported_high_confidence_ucv_count} / {report.total_scenarios}"
    )
    return "\n".join(lines)
