#!/usr/bin/env python3
# =============================================================================
# ELECTRO-HOBBY-3D-UPDATER - tools/check_pins.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Warns when a pinned updater is behind the latest tag of its repository.

Used by the CI: each late pin becomes a `::warning::` line of the log. A
repository that cannot be reached is reported and skipped. By default the exit
code is always 0 so a late pin or a network failure never turns the CI red;
with `--strict` (the check before a release) a pin that is behind exits 1."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from electro_hobby_3d_updater.pins import check_pins, describe  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    strict = "--strict" in (sys.argv[1:] if argv is None else argv)
    behind = False
    for report in check_pins(ROOT / "pyproject.toml"):
        if report.behind:
            behind = True
            print(f"::warning title=Pinned updater is behind::{describe(report)}")
        else:
            print(describe(report))
    return 1 if strict and behind else 0


if __name__ == "__main__":
    raise SystemExit(main())
