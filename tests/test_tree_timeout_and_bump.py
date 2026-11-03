# =============================================================================
# ELECTRO-HOBBY-3D-UPDATER - tests/test_tree_timeout_and_bump.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""A sub-updater that runs out of time is stopped with everything it started, and bump.py raises the version of this project through its own manifest."""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from electro_hobby_3d_updater.main import run_with_tree_timeout

ROOT = Path(__file__).resolve().parents[1]


def _alive(pid: int) -> bool:
    if os.name == "nt":
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True, check=False).stdout
        return str(pid) in out
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def test_a_run_that_times_out_stops_the_processes_it_started_too(tmp_path: Path):
    pid_file = tmp_path / "grandchild.pid"
    child = (
        "import subprocess, sys, time\n"
        "g = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(120)'])\n"
        f"open({str(pid_file)!r}, 'w').write(str(g.pid))\n"
        "time.sleep(120)\n"
    )
    with pytest.raises(subprocess.TimeoutExpired):
        run_with_tree_timeout([sys.executable, "-c", child], timeout=4)
    grandchild = int(pid_file.read_text())
    deadline = time.time() + 10
    while _alive(grandchild) and time.time() < deadline:
        time.sleep(0.2)
    assert not _alive(grandchild), "the process started by the sub-updater was left running"


def test_a_run_that_finishes_returns_its_output_and_code():
    result = run_with_tree_timeout([sys.executable, "-c", "print('hi'); raise SystemExit(3)"], timeout=30, capture_output=True, text=True)
    assert result.returncode == 3 and result.stdout.strip() == "hi"


def test_bump_py_shows_the_current_version_and_writes_nothing():
    before = (ROOT / "pyproject.toml").read_bytes()
    result = subprocess.run([sys.executable, str(ROOT / "bump.py"), "--dry-run"], capture_output=True, text=True, cwd=ROOT)
    assert result.returncode == 0 and "current version" in result.stdout
    assert (ROOT / "pyproject.toml").read_bytes() == before
