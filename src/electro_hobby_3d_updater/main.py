# =============================================================================
# ELECTRO-HOBBY-3D-UPDATER - Entry point: main.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
#
# This tool is deliberately a THIN dispatcher, never a fourth
# implementation of manifest discovery/install/update: `--ecosystem
# hydra-umc|urtc|armor|eh3d` picks which of the four real, independent,
# already-tested ecosystem updaters (hydra_umc_updater, urtc_updater, eh3d_updater,
# armor_updater) actually does the work, and this process runs it as a
# genuinely separate Python interpreter subprocess (`python -m <module>
# --cli ...`) - never imports its `main()` function directly into this
# same process. Four independent argparse CLIs, each free to call
# `sys.exit()` and each parsing its own `sys.argv`, would corrupt each
# other if composed in-process; a subprocess is the same isolation a user
# gets running each command by hand, and is trivially testable by
# replacing the `runner` this module's own `dispatch()` calls.
#
# `status --ecosystem all` is the one thing this tool does that no single
# sub-updater does on its own: run all four (in parallel - they are
# independent processes - with each one's output printed whole and in a
# fixed order) and report which ones failed, without stopping at the first.
# `versions` shows which version of each sub-updater is installed and
# warns when one is behind the latest on GitHub. `install`/`update` always
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
# project's own `pyproject.toml` pulls all four straight from GitHub),
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
import re
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from importlib import metadata
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
            "Hobby 3D) four real ecosystems - HYDRA-UMC, URTC, A.R.M.O.R. and EH3D. "
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
        help="which ecosystem to check, or 'all' for every one of the four in sequence",
    )
    status.add_argument("--offline", action="store_true", help="skip the GitHub check for every ecosystem run")
    status.add_argument("--workspace", help="Workspace root each ecosystem is scanned under (default: this tool's own parent directory).")
    status.add_argument("--timeout-seconds", type=float, default=900.0, help="stop an updater that has not finished after this long (0 = no limit; default 900)")

    for action_name, help_text in (
        ("install", "clone + build one project that isn't installed yet"),
        ("update", "pull + rebuild one project that IS installed"),
    ):
        action_parser = subparsers.add_parser(action_name, help=help_text)
        action_parser.add_argument("--ecosystem", required=True, choices=ECOSYSTEM_KEYS, help="which ecosystem's own updater owns this project")
        action_parser.add_argument("project", help="the exact project/repository name, as that ecosystem's own manifest declares it")
        action_parser.add_argument("--workspace", help="Workspace root (default: this tool's own parent directory).")
        action_parser.add_argument("--timeout-seconds", type=float, default=1800.0, help="stop an updater that has not finished after this long (0 = no limit; default 1800)")

    versions = subparsers.add_parser("versions", help="installed version of each ecosystem's updater, and whether it is behind GitHub")
    versions.add_argument("--offline", action="store_true", help="only show the installed versions, no GitHub check")

    return parser


def _command_for(ecosystem_key: str, args: argparse.Namespace) -> list[str]:
    ecosystem = ECOSYSTEMS_BY_KEY[ecosystem_key]
    command = [sys.executable, "-m", ecosystem.module, "--cli", args.action]
    if args.action == "status":
        if getattr(args, "offline", False):
            command.append("--offline")
    else:
        command.append(args.project)
    workspace = getattr(args, "workspace", None) or str(default_workspace_root())
    return command + ["--workspace", workspace]


def _timeout(args: argparse.Namespace) -> float | None:
    """The limit for one sub-updater run: a git prompt waiting for a credential, or a hung
    network, must not block this command for ever. 0 or less means no limit."""
    value = getattr(args, "timeout_seconds", None)
    return value if value and value > 0 else None


def _run_one(ecosystem_key: str, args: argparse.Namespace, *, runner) -> int:
    name = ECOSYSTEMS_BY_KEY[ecosystem_key].display_name
    print(f"=== {name} ===", file=sys.stderr)
    try:
        return runner(_command_for(ecosystem_key, args), timeout=_timeout(args)).returncode
    except subprocess.TimeoutExpired:
        print(f"{name}: did not finish within {_timeout(args):.0f} seconds and was stopped (change it with --timeout-seconds)", file=sys.stderr)
        return 1


class _TimedOut:
    """Stands in for a finished run whose updater had to be stopped."""

    returncode = 1
    stdout = ""

    def __init__(self, message: str) -> None:
        self.stderr = message + chr(10)


def _status_all(args: argparse.Namespace, *, runner) -> int:
    """The four sub-updaters run at the same time (they are independent
    processes, and each one spends most of its time waiting on GitHub);
    their captured output is printed whole, one ecosystem after another in
    the fixed ECOSYSTEMS order, so the report reads the same as before."""
    def run(ecosystem):
        try:
            return runner(_command_for(ecosystem.key, args), capture_output=True, text=True, timeout=_timeout(args))
        except subprocess.TimeoutExpired:
            return _TimedOut(f"{ecosystem.display_name}: did not finish within {_timeout(args):.0f} seconds and was stopped (change it with --timeout-seconds)")

    with ThreadPoolExecutor(max_workers=len(ECOSYSTEMS)) as pool:
        results = list(pool.map(run, ECOSYSTEMS))
    failed = []
    for ecosystem, result in zip(ECOSYSTEMS, results, strict=True):
        print(f"=== {ecosystem.display_name} ===", file=sys.stderr)
        if getattr(result, "stdout", None):
            sys.stdout.write(result.stdout)
            sys.stdout.flush()
        if getattr(result, "stderr", None):
            sys.stderr.write(result.stderr)
        if result.returncode != 0:
            failed.append(ecosystem.display_name)
    if failed:
        print(f"FAILED: {', '.join(failed)}", file=sys.stderr)
        return 1
    return 0


def _version_tuple(text: str) -> tuple[int, ...]:
    return tuple(int(part) for part in re.findall(r"\d+", text)[:4])


def latest_version_on_github(repository: str) -> str | None:
    """The version in the repository's own pyproject.toml on main, or None
    when GitHub cannot be reached."""
    url = f"https://raw.githubusercontent.com/JuanenRac/{repository}/main/pyproject.toml"
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "electro-hobby-3d-updater"})
        with urllib.request.urlopen(request, timeout=15) as response:
            text = response.read().decode("utf-8", errors="replace")
    except OSError:
        return None
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.M)
    return match.group(1) if match else None


def installed_version(distribution: str) -> str | None:
    try:
        return metadata.version(distribution)
    except metadata.PackageNotFoundError:
        return None


def show_versions(args: argparse.Namespace, *, installed=installed_version, latest=latest_version_on_github) -> int:
    behind = 0
    for ecosystem in ECOSYSTEMS:
        have = installed(ecosystem.distribution)
        line = f"{ecosystem.display_name:<11} {ecosystem.distribution:<18} installed {have or 'NOT INSTALLED'}"
        if not args.offline:
            newest = latest(ecosystem.repository)
            if newest is None:
                line += "  (GitHub not reachable)"
            else:
                line += f"  latest {newest}"
                if have is None or _version_tuple(have) < _version_tuple(newest):
                    line += "  <- BEHIND the main branch: this tool pins each updater to a reviewed commit in pyproject.toml; update the pin there, then reinstall"
                    behind += 1
        print(line)
    return 0 if behind == 0 else 2


def dispatch(args: argparse.Namespace, *, runner=subprocess.run) -> int:
    """Runs the real sub-updater(s) this call resolves to. `runner` takes
    a command list (plus subprocess.run keyword arguments) and returns an
    object with `.returncode` (and, when output is captured, `.stdout`/
    `.stderr`) - the shape of `subprocess.run`'s own return value, swapped
    out in tests for a fake that never actually spawns a process."""
    if args.action == "versions":
        return show_versions(args)
    if args.action == "status" and args.ecosystem == "all":
        return _status_all(args, runner=runner)
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
