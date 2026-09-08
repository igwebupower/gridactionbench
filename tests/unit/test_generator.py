"""Tests for the parameterised scenario generator (gridactionbench/scenarios/generator.py).

See docs/suites/gb-bess/SCENARIO_TEMPLATES.md for what this generator is (and is not) —
these tests check the generator's own mechanical correctness (determinism, uniqueness,
schema validity), not calibration outcomes (those live in tests/golden/).
"""

from __future__ import annotations

from gridactionbench.scenarios.generator import TEMPLATES, coverage_report, generate


def test_generate_is_deterministic_given_the_same_seed():
    a = generate(n_per_template=5, seed=7)
    b = generate(n_per_template=5, seed=7)
    assert [s.model_dump() for s in a] == [s.model_dump() for s in b]


def test_generate_produces_different_scenarios_for_different_seeds():
    a = generate(n_per_template=5, seed=1)
    b = generate(n_per_template=5, seed=2)
    assert [s.model_dump() for s in a] != [s.model_dump() for s in b]


def test_every_generated_scenario_has_a_unique_id():
    scenarios = generate(n_per_template=15, seed=42)
    ids = [s.scenario_id for s in scenarios]
    assert len(ids) == len(set(ids))


def test_generated_scenario_count_matches_templates_times_n():
    n_per_template = 10
    scenarios = generate(n_per_template=n_per_template, seed=1)
    assert len(scenarios) == len(TEMPLATES) * n_per_template


def test_all_seven_families_are_represented_in_the_templates():
    families = {t.family for t in TEMPLATES}
    assert families == {"PHY", "NET", "OPS", "DATA", "MKT", "ADV", "HUM"}


def test_coverage_report_covers_every_declared_dimension():
    report = coverage_report()
    for template in TEMPLATES:
        for dimension in template.coverage:
            assert dimension in report
            assert sum(report[dimension].values()) == len(TEMPLATES)


def test_adding_a_template_does_not_change_another_templates_generated_instances():
    """Reproducibility guarantee stated in the generator's own docstring: each template is
    seeded from (seed, template_id), so the template list's composition doesn't leak into
    another template's random draws."""
    full = {s.scenario_id: s.model_dump() for s in generate(TEMPLATES, n_per_template=3, seed=42)}
    subset = generate(TEMPLATES[:5], n_per_template=3, seed=42)
    for s in subset:
        assert full[s.scenario_id] == s.model_dump()
