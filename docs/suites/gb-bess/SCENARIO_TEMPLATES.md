# Parameterised Scenario Templates — GB-BESS v0.1

**Status:** Phase 3 initial infrastructure (master brief §53, §71). This is a genuine, working start on parameterised scenario generation — **not** a claim of having met the Definition of Done's `≥100 templates` / `≥1,000 executions` targets. 20 templates, generating 300 scenario instances at the documented default (`n_per_template=15`), are shipped and tested as of this pass. See `docs/project/DEFINITION_OF_DONE.md` for the honest gap remaining.

## What this is

`gridactionbench/scenarios/generator.py` defines 20 `ScenarioTemplate`s spanning all 7 scenario families (including **MKT**, which the hand-authored initial 20 deliberately has zero dedicated scenarios for — see `docs/suites/gb-bess/SCENARIO_CATALOGUE.md`'s own coverage note — and **`OPS-TEMP-DISCHARGE-PROHIBITION-001`**, whose FAIL branch no hand-authored scenario exercises at all). Each template is a documented parameter-range recipe; `generate(templates, n_per_template, seed)` deterministically produces concrete `Scenario` instances from it — same `(templates, n_per_template, seed)` always reproduces byte-identical scenarios (`tests/unit/test_generator.py`).

```bash
gridactionbench run-generated --agent rule-based          # run the default 300-scenario set
gridactionbench coverage                                    # print the coverage report below
```

## Coverage dimensions (master brief §53)

Every template declares fixed tags for: `soc_regime`, `network_regime`, `price_regime`, `policy_state`, `information_quality`, `expected_escalation`, `boundary_condition`. Varying a template's *numeric* parameters (e.g. the exact SOC value, the exact price) does not change which *regime* it represents — that is a template-design choice, not a per-instance one. Current coverage (`gridactionbench coverage`, 20 templates):

| Dimension | Tags represented |
|---|---|
| `soc_regime` | mid (16), near_max (2), near_min (1), near_reserve (1) |
| `network_regime` | ample (14), constrained (3), missing (2), implausible (1) |
| `price_regime` | mixed (5), n/a (5), negative (4), positive (4), neutral (1), volatile (1) |
| `policy_state` | none (16), reserve_soc (1), charge_prohibited (1), discharge_prohibited (1), approval_required (1) |
| `information_quality` | fresh (13), missing (2), stale (1), conflicting (1), implausible (1), adversarial (1), conflicting+missing (1) |
| `expected_escalation` | none (11), required (5), conditional (2), permitted (1), unnecessary (1) |
| `boundary_condition` | n/a (11), one each of: soc_ceiling, soc_floor, charge_rate_limit, discharge_rate_limit, import_headroom, export_headroom, reserve_soc, staleness_threshold, conflict_tolerance |

**Honest read of this table:** `soc_regime` and `price_regime` are dominated by `mid`/`mixed` because most templates hold SOC and price at a representative midpoint while varying a different dimension (headroom, policy, information quality) — this is intentional, not an oversight, but it does mean SOC-regime and price-regime coverage specifically would benefit most from additional templates in a future pass, not from generating more instances of the existing 20.

## Capability and stress-dimension tags (added 2026-09-09)

Each `ScenarioTemplate` (and each `EpisodeSpec`, `gridactionbench/scenarios/gb_bess/episodes.py`) now additionally carries `primary_capability` (`docs/benchmark/CAPABILITY_TAXONOMY.md`), `complexity_rung`, `u_classes`, and `autonomy_burden` (`docs/benchmark/STRESS_DIMENSIONS.md`) — additive dataclass fields, independent of the `coverage` dict above, not a replacement for it. Current template-level breakdown:

| Dimension | Tags represented across the 20 templates |
|---|---|
| `primary_capability` | ACT (6: all PHY + NET), DECIDE (5: all OPS reserve/prohibition + both MKT + ADV), PERCEIVE (5: all DATA), ESCALATE (4: OPS-APPROVAL + both HUM) |
| `complexity_rung` | C0 (20 — GB-BESS v0.1 has no other rung implemented) |
| `u_classes` | U0 (13), U2 (2), U3 (1), U4 (1), U7 (2, one of which — `HUM-REQUIRED` — also carries U2 and U4) |
| `autonomy_burden` | low (20 — every `ScenarioTemplate` is Atomic) |

No `EpisodeSpec` is tagged ACT+ADAPT ambiguity away by convenience: `GB-BESS-EP-001` (progressive depletion, static conditions) is DECIDE, `GB-BESS-EP-002` (SOC-ceiling approach, static conditions) is ACT, and `GB-BESS-EP-003`/`004`/`005`/`007` are tagged ADAPT — `GB-BESS-EP-007` (day-ahead price forecast turns out wrong, added 2026-09-09) is the fourth, and the first episode representing U1/forecast uncertainty (`docs/benchmark/STRESS_DIMENSIONS.md`). `GB-BESS-EP-006` is ESCALATE, per `docs/benchmark/CAPABILITY_TAXONOMY.md`'s "closer to an Operational-task version of this capability" account. **`task_mode` (added 2026-09-09):** `GB-BESS-EP-001`/`EP-002` are `"Sequential"` (`autonomy_burden: medium`) — reclassified on finding their conditions are static, not changing, closing `docs/benchmark/TASK_MODEL.md`'s previously-claimed Sequential gap; `EP-003`-`EP-007` are `"Operational"` (`autonomy_burden: high`). See `tests/unit/test_capability_tags.py` for the test that pins every one of these assignments.

## What generating this set actually found (not a hypothetical benefit)

Running the 300-scenario generated set against `RuleBasedAgent` — the benchmark's own "correct" reference controller — surfaced a real bug: the agent never checked `telemetry.field_status.network` at all. This was invisible in the hand-authored initial 20 because the one scenario testing missing network headroom (`GB-BESS-HUM-019`) *also* has a conflicting SOC reading, which the agent did check — masking the network-specific gap entirely. The generator's `DATA-MISSING-NETWORK` template isolates network-missingness without a SOC conflict and produced 15 UCVs out of 300 scenarios, all from that one template, all from the same root cause. Fixed in `baselines/rule_based/agent.py`; the specific case is now a permanent regression test (`tests/golden/test_generated_scenarios.py`). This is the concrete argument for why `≥1,000 executions` is a real target and not busywork — a hand-picked 20-scenario set has structural blind spots that broader, systematic parameter coverage reliably finds.

## What remains for a full Phase 3 pass

- Templates: 20 shipped vs. `≥100` targeted. Priority gaps for the next batch: dedicated `soc_regime` and `price_regime` variation (see "Honest read," above); episode-mode (Mode B) template generation, not attempted at all yet; adversarial injection variants beyond the 4 currently hard-coded in `_INJECTION_VARIANTS`.
- Executions: 300 at the documented default vs. `≥1,000` targeted — trivially reachable by raising `n_per_template` (the generator and pipeline were stress-tested at this volume with no errors, and per-record performance was fixed during this pass — see `gridactionbench/provenance/capture.py`'s memoized git-commit capture, a real 10x speedup found by timing the test suite, not a hypothetical optimization) — not done in this pass because 20 templates × a larger `n_per_template` would not add genuinely new *coverage*, only volume within the coverage gaps already identified above. Expanding templates first, then scaling `n_per_template`, is the intended order.
- No domain review of template parameter ranges has occurred (same caveat as the hand-authored 20 — `docs/project/ASSUMPTIONS.md`).
- Public/private holdout generation (`docs/benchmark/PUBLIC_PRIVATE_POLICY.md`'s generator-based design) is architecturally compatible with this module (each template already has a fixed, documented seed-to-instance mapping) but no private-seed infrastructure has been built — everything generated by this module today is public development material, not an official holdout.
