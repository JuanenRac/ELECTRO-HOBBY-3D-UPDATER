# =============================================================================
# ELECTRO-HOBBY-3D-UPDATER - tests/test_children.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Names outside ASCII in what the updaters write, a version download cut in the middle and a damaged pyproject.toml.
The children are real processes of this Python; the network is replaced by functions."""
from __future__ import annotations

import http.client
import io
import subprocess
import sys

import pytest

from electro_hobby_3d_updater import main as main_module
from electro_hobby_3d_updater import pins
from electro_hobby_3d_updater.children import CAPTURED_TEXT, child_environment, print_whatever_the_console_holds

NAMES = "configuraci\u00f3n \u201d \u65e5\u672c"
PRINT_NAMES = f"import sys; print('{NAMES}'); print('{NAMES}', file=sys.stderr)"
EXPECTED = NAMES


def _cp1252_system(**extra: str) -> dict[str, str]:
    """An environment in which a child would write to a pipe with a code page that cannot hold every name."""
    return {**child_environment(captured=True), "PYTHONUTF8": "0", **extra}


def test_names_outside_ascii_come_back_whole_from_a_captured_updater():
    done = main_module.run_with_tree_timeout(
        [sys.executable, "-c", PRINT_NAMES], timeout=60, capture_output=True, text=True, env=_cp1252_system(), **CAPTURED_TEXT)
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == EXPECTED
    assert done.stderr.strip() == EXPECTED


def test_output_that_goes_to_the_console_replaces_what_the_console_cannot_hold():
    environment = child_environment(captured=False, base={**_cp1252_system(), "PYTHONIOENCODING": "cp1252:replace"})
    assert environment["PYTHONIOENCODING"] == "cp1252:replace"   # the choice of the person is kept
    done = subprocess.run([sys.executable, "-c", PRINT_NAMES], capture_output=True, env=environment, timeout=60, check=False)
    assert done.returncode == 0, done.stderr
    assert done.stdout.startswith(b"configuraci\xf3n")
    assert child_environment(captured=False, base={})["PYTHONIOENCODING"] == ":replace"


def test_status_all_asks_for_utf8_and_reads_it_as_utf8():
    seen = []

    def runner(command, **kwargs):
        seen.append(kwargs)
        return subprocess.CompletedProcess(command, 0, "", "")

    args = main_module.build_parser().parse_args(["status", "--ecosystem", "all", "--workspace", "/ws"])
    assert main_module.dispatch(args, runner=runner) == 0
    assert len(seen) == 4
    assert all(k["encoding"] == "utf-8" and k["errors"] == "replace" and k["env"]["PYTHONIOENCODING"] == "utf-8:replace" for k in seen)


def test_a_name_the_console_cannot_hold_is_printed_with_a_mark():
    raw = io.BytesIO()
    console = io.TextIOWrapper(raw, encoding="cp1252", newline="\n")
    print_whatever_the_console_holds(console, object())
    console.write("\u65e5.txt\n")
    console.flush()
    assert raw.getvalue() == b"?.txt\n"


@pytest.mark.parametrize("error", [http.client.IncompleteRead(b"v", 100), http.client.BadStatusLine("x"), ConnectionResetError()])
def test_a_cut_version_download_is_an_unknown_version(monkeypatch, error):
    def urlopen(*_args, **_kwargs):
        raise error

    monkeypatch.setattr(main_module.urllib.request, "urlopen", urlopen)
    assert main_module.latest_version_on_github("EH3D-UPDATER") is None


@pytest.mark.parametrize("raw", ["[project]\n".encode("utf-16"), b"# se\xf1al\n", b'[project]\nname = "x"\ndependencies = ["eh3d-updater @ git+https://git'])
def test_a_damaged_pyproject_is_a_message_and_not_an_all_clear(tmp_path, capsys, raw):
    damaged = tmp_path / "pyproject.toml"
    damaged.write_bytes(raw)
    args = main_module.build_parser().parse_args(["pins", "--pyproject", str(damaged)])
    assert main_module.show_pins(args, latest=lambda _url: "9.9.9") == 64
    assert str(damaged) in capsys.readouterr().err


def test_a_pyproject_with_a_byte_order_mark_is_read(tmp_path):
    file = tmp_path / "pyproject.toml"
    file.write_bytes(b'\xef\xbb\xbf"alpha @ git+https://github.com/Owner/ALPHA.git@0123456789012345678901234567890123456789", # v0.1.0\n')
    assert [report.pin.name for report in pins.check_pins(file, latest=lambda _url: None)] == ["alpha"]


def test_git_output_that_is_not_in_the_code_page_does_not_end_the_check():
    def runner(command, **kwargs):
        assert kwargs["encoding"] == "utf-8" and kwargs["errors"] == "replace"
        return subprocess.CompletedProcess(command, 0, "abc\trefs/tags/v0.2.0\nabc\trefs/tags/\ufffd\n", "")

    assert pins.latest_tag("https://x/y", runner=runner) == "0.2.0"


def test_the_window_says_so_when_an_updater_cannot_be_started(monkeypatch, tmp_path):
    pytest.importorskip("PySide6")
    from electro_hobby_3d_updater import qt_gui

    def popen(*_args, **_kwargs):
        raise FileNotFoundError("the folder is gone")

    monkeypatch.setattr(qt_gui, "installed", lambda _module: True)
    monkeypatch.setattr(qt_gui.subprocess, "Popen", popen)
    bridge = qt_gui.Bridge(tmp_path)
    bridge.openUpdater("urtc")
    assert "the folder is gone" in bridge.log
