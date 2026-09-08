# ADR-009: Decision Record Format

**Status:** Proposed

## Context
Master brief §13 requires a portable, non-proprietary structured representation for the immutable Decision Record produced by every execution.

## Decision
JSONL (one JSON object per line), one file per Run, append-only during execution. Field schema per `docs/benchmark/SPECIFICATION.md` §7 and `docs/architecture/DATA_MODEL.md`. No dependency on any proprietary tracing/observability backend to produce or read a Decision Record — a Decision Record file is valid and fully self-describing on its own, openable with any JSONL-capable tool (including `jq`, `pandas.read_json(lines=True)`, or a plain text editor for a single line).

## Alternatives considered
- **A relational database (e.g. SQLite) as the primary Decision Record store** — rejected as the *primary* format: adds a schema-migration burden and a binary artifact that is harder to diff/review in a pull request or archive alongside a published result; a SQLite export remains a reasonable optional convenience layer built *from* the canonical JSONL, not a replacement for it.
- **A proprietary tracing SDK format (e.g. OpenTelemetry-native spans as the only representation)** — rejected as the sole format: directly contradicts master brief §13's explicit instruction; OTel-compatible export is a reasonable *additional* optional output for teams that already have OTel infrastructure (e.g. Enprompta, per master brief §61's "optional future Enprompta integration"), but JSONL remains canonical and is never a downstream derivative of it.

## Consequences
- Positive: Decision Records are trivially archivable, diffable at the line level, and consumable by any downstream analysis tool without requiring GridActionBench-specific client libraries.
- Negative: JSONL has no built-in schema enforcement at rest — a separate schema-validation step (Phase 1 implementation, using the same `pydantic` models chosen in ADR-001) is required to catch malformed records early rather than relying on JSONL's format alone.
