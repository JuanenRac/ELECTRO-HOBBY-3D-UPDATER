# =============================================================================
# ELECTRO-HOBBY-3D-UPDATER - tests/test_main.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
from __future__ import annotations

import sys

from electro_hobby_3d_updater.ecosystems import ECOSYSTEMS, ECOSYSTEMS_BY_KEY
from electro_hobby_3d_updater.main import build_parser, default_workspace_root, dispatch


class _FakeResult:
    def __init__(self, returncode: int) -> None:
        self.returncode = returncode


class _FakeRunner:
    """Records every command it was asked to run instead of spawning a
    real subprocess - `dispatch()`'s only side effect is calling this."""

    def __init__(self, returncode_by_module: dict[str, int] | None = None) -> None:
        self.calls: list[list[str]] = []
        self._returncode_by_module = returncode_by_module or {}

    def __call__(self, command: list[str]) -> _FakeResult:
        self.calls.append(command)
        module = command[2]
        return _FakeResult(self._returncode_by_module.get(module, 0))


def test_ecosystems_registry_has_exactly_the_three_real_ecosystems():
    assert {ecosystem.key for ecosystem in ECOSYSTEMS} == {"hydra-umc", "urtc", "armor"}
    assert ECOSYSTEMS_BY_KEY["armor"].module == "armor_updater.main"


def test_status_for_one_ecosystem_runs_that_ecosystems_own_cli_module():
    parser = build_parser()
    args = parser.parse_args(["status", "--ecosystem", "urtc", "--workspace", "/ws"])
    runner = _FakeRunner()

    exit_code = dispatch(args, runner=runner)

    assert exit_code == 0
    assert runner.calls == [[sys.executable, "-m", "urtc_updater.main", "--cli", "status", "--workspace", "/ws"]]


def test_status_offline_forwards_the_flag_to_the_sub_updater():
    parser = build_parser()
    args = parser.parse_args(["status", "--ecosystem", "hydra-umc", "--offline", "--workspace", "/ws"])
    runner = _FakeRunner()

    dispatch(args, runner=runner)

    assert runner.calls == [
        [sys.executable, "-m", "hydra_umc_updater.main", "--cli", "status", "--offline", "--workspace", "/ws"]
    ]


def test_status_all_runs_every_ecosystem_once_each_in_order():
    parser = build_parser()
    args = parser.parse_args(["status", "--ecosystem", "all", "--workspace", "/ws"])
    runner = _FakeRunner()

    exit_code = dispatch(args, runner=runner)

    assert exit_code == 0
    modules_run = [call[2] for call in runner.calls]
    assert modules_run == ["hydra_umc_updater.main", "urtc_updater.main", "armor_updater.main"]


def test_status_all_never_stops_at_the_first_failure_and_reports_it():
    parser = build_parser()
    args = parser.parse_args(["status", "--ecosystem", "all", "--workspace", "/ws"])
    runner = _FakeRunner(returncode_by_module={"urtc_updater.main": 1})

    exit_code = dispatch(args, runner=runner)

    # Every ecosystem still ran, even though URTC's own check failed...
    assert len(runner.calls) == 3
    # ...and the overall result honestly reflects that one real failure.
    assert exit_code == 1


def test_install_requires_exactly_one_project_name_and_one_ecosystem():
    parser = build_parser()
    args = parser.parse_args(["install", "--ecosystem", "armor", "ARMOR-NETWORK", "--workspace", "/ws"])
    runner = _FakeRunner()

    exit_code = dispatch(args, runner=runner)

    assert exit_code == 0
    assert runner.calls == [
        [sys.executable, "-m", "armor_updater.main", "--cli", "install", "ARMOR-NETWORK", "--workspace", "/ws"]
    ]


def test_update_dispatches_to_the_right_ecosystem_with_the_project_name():
    parser = build_parser()
    args = parser.parse_args(["update", "--ecosystem", "hydra-umc", "HYDRA-UMC-SERVER", "--workspace", "/ws"])
    runner = _FakeRunner()

    dispatch(args, runner=runner)

    assert runner.calls == [
        [sys.executable, "-m", "hydra_umc_updater.main", "--cli", "update", "HYDRA-UMC-SERVER", "--workspace", "/ws"]
    ]


def test_install_and_update_reject_ecosystem_all():
    parser = build_parser()
    try:
        parser.parse_args(["install", "--ecosystem", "all", "SOMETHING"])
        raised = False
    except SystemExit:
        raised = True
    assert raised, "'all' is only a valid --ecosystem value for status, not install/update"


def test_a_real_failing_sub_updater_call_propagates_its_own_exit_code():
    parser = build_parser()
    args = parser.parse_args(["update", "--ecosystem", "urtc", "URTC", "--workspace", "/ws"])
    runner = _FakeRunner(returncode_by_module={"urtc_updater.main": 3})

    exit_code = dispatch(args, runner=runner)

    assert exit_code == 3


def test_workspace_defaults_to_this_projects_own_parent_directory_when_not_given():
    # Found for real while first exercising this tool end to end: every
    # sub-updater's own default_workspace_root() resolves relative to ITS
    # OWN installed package location, which is wrong once it is installed
    # as a dependency of this project rather than run from its own
    # checkout - see main.py's own module docstring. This tool must always
    # forward an explicit --workspace so that never silently discovers
    # zero projects.
    parser = build_parser()
    args = parser.parse_args(["status", "--ecosystem", "armor"])
    runner = _FakeRunner()

    dispatch(args, runner=runner)

    assert runner.calls[0][-2:] == ["--workspace", str(default_workspace_root())]
