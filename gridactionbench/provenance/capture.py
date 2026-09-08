"""Reproducibility metadata capture: git commit, runtime version, environment.

See docs/benchmark/SPECIFICATION.md §7 (Decision Record fields) and docs/benchmark/
VERSIONING.md.
"""

from __future__ import annotations

import platform
import subprocess
import sys
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=None)
def capture_git_commit(repo_root: Path | str | None = None) -> str | None:
    """Memoized: the current commit cannot change mid-process, and a benchmark run may
    produce thousands of Decision Records (master brief §53's >=1,000-execution target) —
    shelling out to git once per record was a real, measured performance bottleneck during
    Phase 3 (spawning a subprocess per generated scenario), not a hypothetical concern."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
        return result.stdout.strip()
    except Exception:
        # Reproducibility metadata is best-effort — a missing git binary or a non-repo
        # working directory must not crash a benchmark run; it is recorded as unknown.
        return None


def capture_runtime_version() -> str:
    return f"Python {sys.version.split()[0]}"


def capture_environment_metadata() -> dict[str, str]:
    return {
        "platform": platform.platform(),
        "python_implementation": platform.python_implementation(),
    }
