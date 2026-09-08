"""Reproducibility metadata capture: git commit, runtime version, environment.

See docs/benchmark/SPECIFICATION.md §7 (Decision Record fields) and docs/benchmark/
VERSIONING.md.
"""

from __future__ import annotations

import platform
import subprocess
import sys
from pathlib import Path


def capture_git_commit(repo_root: Path | str | None = None) -> str | None:
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
