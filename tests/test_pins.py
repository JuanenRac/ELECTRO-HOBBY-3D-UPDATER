# =============================================================================
# ELECTRO-HOBBY-3D-UPDATER - tests/test_pins.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The pins of pyproject.toml against the latest tags, and --preview / --no-build forwarding."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from electro_hobby_3d_updater import pins
from electro_hobby_3d_updater.main import build_parser, dispatch, show_pins

PYPROJECT = '''
dependencies = [
    "alpha-updater @ git+https://github.com/Owner/ALPHA.git@08403a70510d3c5dabfbe871e5de4155f7d6574a",  # v0.4.8
    "beta-updater @ git+https://github.com/Owner/BETA.git@30c523a23f012af5d8b0e77cce058714428046ac",  # v0.1.7
]
'''


class _Run:
    def __init__(self, returncode=0, stdout=""):
        self.returncode, self.stdout = returncode, stdout


def test_the_pins_are_read_with_their_version_comment():
    found = pins.read_pins(PYPROJECT)
    assert [(p.name, p.version) for p in found] == [("alpha-updater", "0.4.8"), ("beta-updater", "0.1.7")]
    assert found[0].url == "https://github.com/Owner/ALPHA"


def test_the_pins_of_this_very_project_are_all_read():
    root = Path(__file__).resolve().parents[1]
    names = [p.name for p in pins.read_pins((root / "pyproject.toml").read_text(encoding="utf-8"))]
    assert names == ["hydra-umc-updater", "urtc-updater", "armor-updater", "eh3d-updater"]


def test_latest_tag_picks_the_highest_version_not_the_last_listed():
    out = "a\trefs/tags/v0.9.0\nb\trefs/tags/v0.10.0\nc\trefs/tags/v0.2.0\nd\trefs/tags/not-a-version\n"
    assert pins.latest_tag("https://x/y", runner=lambda *a, **k: _Run(0, out)) == "0.10.0"


def test_latest_tag_is_none_when_git_fails_or_is_missing():
    assert pins.latest_tag("https://x/y", runner=lambda *a, **k: _Run(128)) is None

    def boom(*a, **k):
        raise FileNotFoundError("git")

    assert pins.latest_tag("https://x/y", runner=boom) is None

    def slow(*a, **k):
        raise subprocess.TimeoutExpired("git", 1)

    assert pins.latest_tag("https://x/y", runner=slow) is None


def test_a_pin_is_behind_only_when_a_higher_tag_exists(tmp_path):
    file = tmp_path / "pyproject.toml"
    file.write_text(PYPROJECT, encoding="utf-8")
    reports = pins.check_pins(file, latest=lambda url: {"https://github.com/Owner/ALPHA": "0.5.0", "https://github.com/Owner/BETA": None}[url])
    assert [r.behind for r in reports] == [True, False]
    assert "behind" in pins.describe(reports[0])
    assert "not reachable" in pins.describe(reports[1])


def test_the_pins_command_exits_2_when_one_is_behind_and_0_otherwise(tmp_path, capsys):
    file = tmp_path / "pyproject.toml"
    file.write_text(PYPROJECT, encoding="utf-8")
    args = build_parser().parse_args(["pins", "--pyproject", str(file)])
    assert show_pins(args, latest=lambda url: "9.9.9") == 2
    assert show_pins(args, latest=lambda url: "0.0.1") == 0
    assert show_pins(args, latest=lambda url: None) == 0
    assert "BEHIND" in capsys.readouterr().out


def test_the_ci_script_never_fails_even_without_network(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run([sys.executable, str(root / "tools" / "check_pins.py")], capture_output=True, text=True, env={"PATH": "", "SYSTEMROOT": "C:\\Windows"})
    assert result.returncode == 0


class _Runner:
    def __init__(self):
        self.calls = []

    def __call__(self, command, **_kwargs):
        self.calls.append(command)
        return _Run(0)


def test_no_build_is_forwarded_to_every_ecosystem():
    for key in ("hydra-umc", "urtc", "armor", "eh3d"):
        runner = _Runner()
        args = build_parser().parse_args(["install", "--ecosystem", key, "P", "--no-build", "--workspace", "/ws"])
        assert dispatch(args, runner=runner) == 0
        assert "--no-build" in runner.calls[0]


def test_preview_is_forwarded_only_where_the_updater_has_it(capsys):
    runner = _Runner()
    args = build_parser().parse_args(["update", "--ecosystem", "eh3d", "P", "--preview", "--workspace", "/ws"])
    assert dispatch(args, runner=runner) == 0
    assert "--preview" in runner.calls[0]

    runner = _Runner()
    args = build_parser().parse_args(["update", "--ecosystem", "urtc", "P", "--preview", "--workspace", "/ws"])
    assert dispatch(args, runner=runner) == 64
    assert runner.calls == []
    assert "no --preview" in capsys.readouterr().err


def test_without_the_flags_the_command_is_unchanged():
    runner = _Runner()
    args = build_parser().parse_args(["update", "--ecosystem", "eh3d", "P", "--workspace", "/ws"])
    dispatch(args, runner=runner)
    assert "--preview" not in runner.calls[0] and "--no-build" not in runner.calls[0]
