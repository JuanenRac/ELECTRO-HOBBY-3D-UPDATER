#!/usr/bin/env python3
# =============================================================================
# ELECTRO-HOBBY-3D-UPDATER - tools/build_test.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Run a non-versioning build check for this repository: compile every
Python source, then the real pytest suite. Never invokes a version bump
script and never updates CHANGELOG.md."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDED_PARTS = {".git", ".venv", "__pycache__", "*.egg-info"}


def fail(message: str) -> None:
    print(f"BUILD_TEST=FAIL {message}", file=sys.stderr)
    raise SystemExit(1)


def compile_python_sources() -> None:
    files = [path for path in ROOT.rglob("*.py") if not any(part in EXCLUDED_PARTS for part in path.parts)]
    for path in files:
        compile(path.read_text(encoding="utf-8", errors="replace"), str(path), "exec")
    print(f"PYTHON_COMPILE=PASS files={len(files)}")


def main() -> int:
    try:
        manifest = json.loads((ROOT / "electro-hobby-3d.project.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read project manifest: {exc}")

    print(f"BUILD_TEST project={manifest.get('name', ROOT.name)} stack={manifest.get('stack')}")
    compile_python_sources()

    result = subprocess.run([sys.executable, "-m", "pytest", "tests", "-q"], cwd=ROOT)
    if result.returncode != 0:
        fail(f"pytest exited with code {result.returncode}")

    print("BUILD_TEST=PASS versioning=unchanged changelog=unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
