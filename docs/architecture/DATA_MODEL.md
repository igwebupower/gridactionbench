# Data Model

**Status:** Draft — Phase 0. Field-level schema reference; conceptual relationships are in `docs/architecture/DOMAIN_MODEL.md`.

## EnergyObservationV1

See `docs/suites/gb-bess/SPECIFICATION.md` §2 for the full field listing and types. Serialization: JSON, versioned via `schema_version`.

## AgentActionV1

See `docs/suites/gb-bess/SPECIFICATION.md` §3 for the full field listing, types, and validation rules.

## Scenario file (source-of-truth authoring format)

YAML, one file per scenario (or, for Phase 3 generated instances, one template file plus generator config). Required top-level keys, per master brief §44:

```yaml
scenario_id: string
scenario_version: string        # semver

suite: string
suite_version: string
family: PHY | NET | OPS | MKT | DATA | ADV | HUM

source_type: synthetic | historical   # historical requires verified provenance, unused in v0.1
author: string
created_date: date

parameters: {...}               # scenario-specific numeric/categorical inputs
seed: int | null                # for any stochastic element of scenario generation

oracle: {...}                   # full ground truth, per docs/suites/gb-bess/SPECIFICATION.md §2 fields
observation_generation: {...}   # rule/spec for deriving agent_observation from oracle (identity, redaction, corruption)

permitted_actions: [...]
prohibited_actions: [...]
preferred_actions: [...]        # optional

escalation:
  required: bool
  permitted: bool

evaluator_coverage: [eval_id, ...]   # must match the scenario's relevant_evaluators
data_provenance: {...}               # required if source_type: historical; N/A for synthetic

review_status: DRAFT | ENGINEERING_REVIEWED | BENCHMARK_REVIEWED | VERIFIED
review_history: [...]
```

This is the format `docs/suites/gb-bess/SCENARIO_CATALOGUE.md`'s 20 initial scenarios are specified in (informally, as embedded YAML blocks); Phase 1 implementation formalizes this into an actual JSON Schema under `gridactionbench/schemas/` and back-fills the initial 20 as real scenario files under `suites/gb_bess/v0_1/`.

## Decision Record

See `docs/benchmark/SPECIFICATION.md` §7 for the full field listing. Serialization: **JSONL**, one record per line, append-only per run — chosen specifically because it is a portable, streaming-friendly, dependency-free format that does not require proprietary tracing infrastructure to produce or consume (master brief §13), and because it matches the logging convention already validated by prior art (`docs/research/PRIOR_ART.md`, PowerAgentBench's own JSONL evidence logs).

## EvaluationResult (per-evaluator output, embedded in a Decision Record's `evaluation_results`)

```yaml
eval_id: string
version: string
result: pass | warning | failure
evidence: {...}          # evaluator-specific supporting data (e.g. computed resulting_soc, headroom margin)
contributes_to_ucv: bool
```

## Report (aggregated output, not persisted per-record — computed from a Run's Decision Records)

```yaml
run_id: string
versions: {framework, suite, scenario_set, evaluator_set, simulator, agent_configuration}
dimensions:
  - name: string          # e.g. "Physical constraint adherence"
    pass_rate: float
    n: int
ucv_count: int
high_confidence_ucv_count: int
total_scenarios: int
```

Matches `docs/benchmark/SCORING.md`'s required reporting format exactly — this schema exists so the reporting format is enforced structurally, not just by convention in documentation.

## Data provenance record (for any real, licence-confirmed dataset — Phase 5)

```yaml
dataset_name: string
source: string
source_url: string
retrieval_date: date
licence: string
redistribution_status: redistributable | attribution-required | not-redistributable | unconfirmed
required_attribution: string | null
transformation: string
original_units: string
benchmark_units: string
checksum: string           # e.g. sha256
benchmark_version: string
```

Matches master brief §35 exactly. No dataset with `redistribution_status: unconfirmed` is committed to this repository — see `docs/data/DATA_SOURCES.md`.
