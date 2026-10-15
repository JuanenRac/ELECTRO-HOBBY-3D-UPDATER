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
    def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class _FakeRunner:
    """Records every command it was asked to run instead of spawning a
    real subprocess - `dispatch()`'s only side effect is calling this."""

    def __init__(self, returncode_by_module: dict[str, int] | None = None) -> None:
        self.calls: list[list[str]] = []
        self._returncode_by_module = returncode_by_module or {}

    def __call__(self, command: list[str], **_kwargs) -> _FakeResult:
        self.calls.append(command)
        module = command[2]
        return _FakeResult(self._returncode_by_module.get(module, 0), stdout=f"report from {module}\n")


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


def test_status_all_runs_every_ecosystem_once_and_prints_them_in_order(capsys):
    parser = build_parser()
    args = parser.parse_args(["status", "--ecosystem", "all", "--workspace", "/ws"])
    runner = _FakeRunner()

    exit_code = dispatch(args, runner=runner)

    assert exit_code == 0
    # They run in parallel, so the call order is not fixed...
    assert sorted(call[2] for call in runner.calls) == ["armor_updater.main", "hydra_umc_updater.main", "urtc_updater.main"]
    # ...but the report always comes out in the fixed ECOSYSTEMS order.
    out = capsys.readouterr().out
    assert out.index("hydra_umc_updater") < out.index("urtc_updater") < out.index("armor_updater")


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


def test_the_window_texts_exist_in_all_seven_languages():
    from electro_hobby_3d_updater import i18n

    codes = [code for code, _name in i18n.LANGUAGES]
    assert codes == ["en", "es", "de", "fr", "it", "ja", "zh"]
    for key in i18n.keys():
        for code in codes:
            assert i18n.text(code, key).strip(), (key, code)
    # an unknown language falls back to English, an unknown key to itself
    assert i18n.text("xx", "open") == i18n.text("en", "open")
    assert i18n.text("en", "no-such-key") == "no-such-key"
    for ecosystem in ECOSYSTEMS:
        assert f"tag_{ecosystem.key}" in i18n.keys()


def test_without_arguments_the_window_is_opened_and_with_arguments_the_cli_is_used(monkeypatch):
    from electro_hobby_3d_updater import main as main_module

    opened = []
    monkeypatch.setattr(main_module, "launch_window", lambda: opened.append(True) or 0)
    monkeypatch.setattr(sys, "argv", ["electro-hobby-3d-updater"])
    assert main_module.main() == 0 and opened == [True]
    called = []
    monkeypatch.setattr(main_module, "dispatch", lambda args: called.append(args.action) or 0)
    monkeypatch.setattr(sys, "argv", ["electro-hobby-3d-updater", "status", "--ecosystem", "all"])
    assert main_module.main() == 0 and called == ["status"]


def test_the_window_has_its_icon_and_the_about_texts():
    from pathlib import Path

    from electro_hobby_3d_updater import i18n

    images = Path(__file__).resolve().parents[1] / "images"
    assert (images / "ELECTRO_HOBBY_3D_ICON.svg").is_file()
    icon = (images / "ELECTRO_HOBBY_3D_ICON.ico").read_bytes()
    assert icon[:4] == b"\x00\x00\x01\x00" and int.from_bytes(icon[4:6], "little") >= 4  # an .ico with several sizes
    for key in ("menu_about", "about_tagline", "about_description", "about_version_label", "about_author_label", "about_email_label", "about_license_label", "about_license", "open_github", "close"):
        assert key in i18n.keys(), key


def test_status_all_really_runs_the_three_at_the_same_time():
    import threading
    started = threading.Barrier(3, timeout=5)

    def runner(command, **_kwargs):
        started.wait()  # only returns once all three are running at once
        return _FakeResult(0)

    args = build_parser().parse_args(["status", "--ecosystem", "all", "--workspace", "/ws"])
    assert dispatch(args, runner=runner) == 0


def test_versions_reports_installed_and_flags_an_updater_behind_github(capsys):
    from electro_hobby_3d_updater.main import show_versions
    args = build_parser().parse_args(["versions"])
    installed = {"hydra-umc-updater": "0.4.6", "urtc-updater": "0.0.6", "armor-updater": None}.get
    latest = {"HYDRA-UMC-UPDATER": "0.4.6", "URTC-UPDATER": "0.0.7", "ARMOR-UPDATER": "0.0.7"}.get
    assert show_versions(args, installed=installed, latest=latest) == 2
    lines = capsys.readouterr().out.splitlines()
    assert "BEHIND" not in lines[0]
    assert "BEHIND" in lines[1] and "0.0.6" in lines[1]
    assert "NOT INSTALLED" in lines[2] and "BEHIND" in lines[2]


def test_versions_offline_never_contacts_github(capsys):
    from electro_hobby_3d_updater.main import show_versions
    args = build_parser().parse_args(["versions", "--offline"])

    def latest(_repository):
        raise AssertionError("--offline must not look anything up on GitHub")

    assert show_versions(args, installed=lambda _d: "1.0.0", latest=latest) == 0
    assert "latest" not in capsys.readouterr().out
