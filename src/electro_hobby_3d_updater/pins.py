# =============================================================================
# ELECTRO-HOBBY-3D-UPDATER - Pins of the four updaters: pins.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Compares the commits this project pins its four updaters to with the latest
tag of each repository.

The dependencies of pyproject.toml look like
``"eh3d-updater @ git+https://github.com/JuanenRac/EH3D-UPDATER.git@<sha>"  # v0.0.3``;
the comment is the version the pinned commit was reviewed as. A pin whose
version is lower than the latest tag of that repository is "behind". This only
informs: a repository that cannot be reached is reported as unknown, never as
an error, and nothing here changes a file.

Standard library only, so the CI can run it before anything is installed."""
from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

#: One dependency line: name, repository URL, pinned commit, and the version in the trailing comment.
_PIN_RE = re.compile(
    r'"(?P<name>[A-Za-z0-9._-]+)\s*@\s*git\+(?P<url>https://[^@"\s]+?)(?:\.git)?@(?P<sha>[0-9a-fA-F]{7,40})"\s*,?\s*#\s*v?(?P<version>\d+(?:\.\d+){1,3})'
)
_TAG_RE = re.compile(r"^v?(\d+(?:\.\d+){1,3})$")


@dataclass(frozen=True)
class Pin:
    name: str
    url: str
    sha: str
    version: str


@dataclass(frozen=True)
class PinReport:
    pin: Pin
    #: The highest version tag of the repository, or None when it could not be read.
    latest: str | None

    @property
    def behind(self) -> bool:
        return self.latest is not None and version_tuple(self.pin.version) < version_tuple(self.latest)


def version_tuple(text: str) -> tuple[int, ...]:
    parts = [int(part) for part in re.findall(r"\d+", text)[:4]]
    return tuple(parts + [0] * (4 - len(parts)))


def read_pins(pyproject_text: str) -> list[Pin]:
    """The pins of a pyproject.toml (only the dependencies that name a git commit and carry a version comment)."""
    return [Pin(m["name"], m["url"], m["sha"], m["version"]) for m in _PIN_RE.finditer(pyproject_text)]


def latest_tag(url: str, *, runner: Callable[..., subprocess.CompletedProcess] = subprocess.run, timeout: float = 30.0) -> str | None:
    """The highest version tag of the repository at `url` (`git ls-remote --tags`), or None when git or the network fail."""
    try:
        result = runner(
            ["git", "ls-remote", "--tags", "--refs", url + ".git"],
            capture_output=True, text=True, timeout=timeout, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    versions = []
    for line in result.stdout.splitlines():
        ref = line.split("\t")[-1].strip()
        match = _TAG_RE.match(ref.removeprefix("refs/tags/"))
        if match:
            versions.append(match.group(1))
    return max(versions, key=version_tuple) if versions else None


def check_pins(pyproject: Path, *, latest: Callable[[str], str | None] = latest_tag) -> list[PinReport]:
    return [PinReport(pin, latest(pin.url)) for pin in read_pins(pyproject.read_text(encoding="utf-8"))]


def describe(report: PinReport) -> str:
    pin = report.pin
    if report.latest is None:
        return f"{pin.name}: pinned v{pin.version}, latest tag unknown (repository not reachable)"
    if report.behind:
        return f"{pin.name}: pinned v{pin.version} is behind the latest tag v{report.latest}"
    return f"{pin.name}: pinned v{pin.version} is the latest tag"
