"""Resolves the private seed used to draw official GB-BESS holdout instances from the
public generator templates (docs/benchmark/PUBLIC_PRIVATE_POLICY.md, "GridActionBench's
policy for GB-BESS v0.1," item 3: "Official evaluation instances are drawn from the
published templates using a private seed, held in a separate, not-publicly-committed
location.").

This module never hardcodes a seed and never falls back to the public generator's own
default seed (42, gridactionbench/scenarios/generator.py) — doing so would silently defeat
the entire point of a private holdout. Absence of a configured seed is a hard error, not a
default.
"""

from __future__ import annotations

import os
from pathlib import Path

ENV_VAR = "GRIDACTIONBENCH_PRIVATE_SEED"
LOCAL_SEED_FILE = Path("fixtures/private_dev_only/private_seed.txt")


class PrivateSeedNotConfigured(RuntimeError):
    pass


def resolve_private_seed() -> int:
    """Checks $GRIDACTIONBENCH_PRIVATE_SEED first, then fixtures/private_dev_only/
    private_seed.txt (both git-ignored — docs/benchmark/PUBLIC_PRIVATE_POLICY.md's
    "Local private fixtures"). Raises PrivateSeedNotConfigured, with setup instructions,
    if neither exists."""
    env_value = os.environ.get(ENV_VAR)
    if env_value:
        return _parse(env_value, f"${ENV_VAR}")
    if LOCAL_SEED_FILE.exists():
        return _parse(LOCAL_SEED_FILE.read_text(encoding="utf-8").strip(), str(LOCAL_SEED_FILE))
    raise PrivateSeedNotConfigured(
        f"No private seed configured. Set ${ENV_VAR} or create it locally:\n"
        f"  mkdir -p {LOCAL_SEED_FILE.parent}\n"
        f"  echo <your-integer-seed> > {LOCAL_SEED_FILE}\n"
        "See docs/benchmark/PUBLIC_PRIVATE_POLICY.md — never reuse the public generator's "
        "default seed (42) for official holdouts."
    )


def _parse(raw: str, source: str) -> int:
    try:
        return int(raw)
    except ValueError as exc:
        raise PrivateSeedNotConfigured(f"{source} must contain a single integer seed, got {raw!r}") from exc
