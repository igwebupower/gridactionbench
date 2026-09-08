# Data Provenance

**Status:** Draft — Phase 0. No frozen real-world dataset exists yet. This document will hold one provenance record (per `docs/architecture/DATA_MODEL.md`'s schema) for every real dataset frozen into the benchmark, starting in Phase 5. It is created now, empty of real entries, so the required structure and discipline are established before any data is actually committed.

## Provenance record schema (recap, see `docs/architecture/DATA_MODEL.md` for the authoritative version)

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
checksum: string
benchmark_version: string
```

## Current entries

None. No dataset has been retrieved, transformed, or frozen as of Phase 0 (2026-09-08). GB-BESS v0.1 uses synthetic data exclusively — see `docs/suites/gb-bess/SCENARIO_CATALOGUE.md` and `docs/data/DATA_SOURCES.md`.

## Synthetic scenario provenance (distinct from real-dataset provenance, but still tracked)

Every synthetic scenario in `docs/suites/gb-bess/SCENARIO_CATALOGUE.md` carries its own lightweight provenance via the scenario file schema's `author`, `created_date`, and `source_type: synthetic` fields (`docs/architecture/DATA_MODEL.md`, "Scenario file"). This satisfies master brief §44's per-scenario provenance requirement without conflating synthetic-scenario authorship tracking with real-dataset licensing provenance, which are different concerns with different risk profiles (a synthetic scenario has no licensing risk; a real dataset does).

## Process this document commits to, once a real dataset is added

```text
Authoritative Source -> Retrieval -> Validation -> Transformation -> Frozen Dataset -> Checksum -> Benchmark Version
```

Every step recorded, in order, for every dataset, per master brief §34. No step is skipped or retroactively documented after the fact — a dataset is not committed to the repository until its provenance record here is complete.
