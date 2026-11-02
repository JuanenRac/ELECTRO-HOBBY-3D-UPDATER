#!/usr/bin/env python3
# =============================================================================
# ELECTRO-HOBBY-3D-UPDATER - tools/check_pins.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Warns (never fails) when a pinned updater is behind the latest tag of its repository.

Used by the CI: each late pin becomes a `::warning::` line of the log. A
repository that cannot be reached is reported and skipped. The exit code is
always 0 so a late pin or a network failure never turns the CI red."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from electro_hobby_3d_updater.pins import check_pins, describe  # noqa: E402


def main() -> int:
    for report in check_pins(ROOT / "pyproject.toml"):
        if report.behind:
            print(f"::warning title=Pinned updater is behind::{describe(report)}")
        else:
            print(describe(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
