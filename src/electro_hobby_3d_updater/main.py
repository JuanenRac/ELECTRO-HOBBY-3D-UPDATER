# =============================================================================
# ELECTRO-HOBBY-3D-UPDATER - Entry point: main.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
#
# This tool is deliberately a THIN dispatcher, never a fourth
# implementation of manifest discovery/install/update: `--ecosystem
# hydra-umc|urtc|armor` picks which of the three real, independent,
# already-tested ecosystem updaters (hydra_umc_updater, urtc_updater,
# armor_updater) actually does the work, and this process runs it as a
# genuinely separate Python interpreter subprocess (`python -m <module>
# --cli ...`) - never imports its `main()` function directly into this
# same process. Three independent argparse CLIs, each free to call
# `sys.exit()` and each parsing its own `sys.argv`, would corrupt each
# other if composed in-process; a subprocess is the same isolation a user
# gets running each command by hand, and is trivially testable by
# replacing the `runner` this module's own `dispatch()` calls.
#
# `status --ecosystem all` is the one thing this tool does that no single
# sub-updater does on its own: run all three in sequence and report which
# ones failed, without stopping at the first. `install`/`update` always
# need exactly one ecosystem and one project name - there is no "update
# everything across every ecosystem" here, same non-negotiable stance
# each sub-updater's own CLI already takes for its own projects.
#
# `--workspace` MUST be forwarded explicitly - found for real while first
# exercising this tool end to end: every sub-updater's own
# `default_workspace_root()` resolves to ITS OWN package's parent
# directory (`Path(__file__).resolve().parents[3]`), correct only when
# that sub-updater is run from its own local sibling checkout. Once it is
# installed as a regular dependency of THIS project instead (this
# project's own `pyproject.toml` pulls all three straight from GitHub),
# that heuristic resolves to somewhere under THIS project's own `.venv`,
# not the user's real workspace - silently discovering zero projects
# instead of failing loudly. Defaulting `--workspace` here to this
# project's own parent directory (the same depth, `parents[3]` from this
# file) and always forwarding it fixes that for the common case where
# ELECTRO-HOBBY-3D-UPDATER itself is checked out as a sibling of every
# other real repository, the same layout every sub-updater already
# assumes; `--workspace` stays overridable for anything else.
# =============================================================================
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from . import __version__
from .ecosystems import ECOSYSTEMS, ECOSYSTEMS_BY_KEY

ECOSYSTEM_KEYS = tuple(ecosystem.key for ecosystem in ECOSYSTEMS)


def default_workspace_root() -> Path:
    """This project's own parent directory - see this module's header
    comment for why forwarding it explicitly to every sub-updater call is
    required, not optional."""
    return Path(__file__).resolve().parents[3]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="electro-hobby-3d-updater",
        description=(
            "Detects, installs, and updates every one of JuanenRac's (Electro "
            "Hobby 3D) three real ecosystems - HYDRA-UMC, URTC and A.R.M.O.R. "
            "- by delegating to each ecosystem's own dedicated updater. This "
            "tool holds no discovery or install logic of its own."
        ),
    )
    parser.add_argument("--version", action="version", version=f"electro-hobby-3d-updater {__version__}")
    subparsers = parser.add_subparsers(dest="action", required=True)

    status = subparsers.add_parser("status", help="what's installed, what version, what's on GitHub")
    status.add_argument(
        "--ecosystem",
        required=True,
        choices=(*ECOSYSTEM_KEYS, "all"),
        help="which ecosystem to check, or 'all' for every one of the three in sequence",
    )
    status.add_argument("--offline", action="store_true", help="skip the GitHub check for every ecosystem run")
    status.add_argument("--workspace", help="Workspace root each ecosystem is scanned under (default: this tool's own parent directory).")

    for action_name, help_text in (
        ("install", "clone + build one project that isn't installed yet"),
        ("update", "pull + rebuild one project that IS installed"),
    ):
        action_parser = subparsers.add_parser(action_name, help=help_text)
        action_parser.add_argument("--ecosystem", required=True, choices=ECOSYSTEM_KEYS, help="which ecosystem's own updater owns this project")
        action_parser.add_argument("project", help="the exact project/repository name, as that ecosystem's own manifest declares it")
        action_parser.add_argument("--workspace", help="Workspace root (default: this tool's own parent directory).")

    return parser


def _run_one(ecosystem_key: str, args: argparse.Namespace, *, runner) -> int:
    ecosystem = ECOSYSTEMS_BY_KEY[ecosystem_key]
    command = [sys.executable, "-m", ecosystem.module, "--cli", args.action]
    if args.action == "status":
        if getattr(args, "offline", False):
            command.append("--offline")
    else:
        command.append(args.project)
    workspace = getattr(args, "workspace", None) or str(default_workspace_root())
    command += ["--workspace", workspace]
    print(f"=== {ecosystem.display_name} ===", file=sys.stderr)
    result = runner(command)
    return result.returncode


def dispatch(args: argparse.Namespace, *, runner=subprocess.run) -> int:
    """Runs the real sub-updater(s) this call resolves to. `runner` takes
    a command list and returns an object with a `.returncode` attribute -
    the exact shape of `subprocess.run`'s own return value, swapped out in
    tests for a fake that never actually spawns a process."""
    if args.action == "status" and args.ecosystem == "all":
        exit_codes = [_run_one(ecosystem.key, args, runner=runner) for ecosystem in ECOSYSTEMS]
        failed = [ecosystem.display_name for ecosystem, code in zip(ECOSYSTEMS, exit_codes) if code != 0]
        if failed:
            print(f"FAILED: {', '.join(failed)}", file=sys.stderr)
            return 1
        return 0
    return _run_one(args.ecosystem, args, runner=runner)


def launch_window() -> int:
    """The window (qt_gui.py), when the optional PySide6 is installed; otherwise a clear hint and the command-line help."""
    try:
        from .qt_gui import launch_qt_gui
    except ImportError:
        print("The window needs PySide6: pip install -e \".[gui]\"  (the command line works without it)", file=sys.stderr)
        build_parser().print_help()
        return 1
    return launch_qt_gui(default_workspace_root())


def main() -> int:
    # Without arguments (a double click) the window opens; with arguments this is the command line, exactly as before.
    if len(sys.argv) == 1:
        return launch_window()
    parser = build_parser()
    args = parser.parse_args()
    return dispatch(args)


if __name__ == "__main__":
    raise SystemExit(main())
