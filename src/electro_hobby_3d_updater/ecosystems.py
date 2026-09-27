# =============================================================================
# ELECTRO-HOBBY-3D-UPDATER - The three real ecosystems: ecosystems.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The one place that names JuanenRac's (Electro Hobby 3D) three real,
independent software ecosystems and which installed package/CLI module
answers for each one. Adding a fourth ecosystem in the future is a one-line
change here - main.py itself never hardcodes an ecosystem name."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Ecosystem:
    #: The `--ecosystem` CLI value - short, stable, never localized.
    key: str
    #: Human-readable name for status output and the About text.
    display_name: str
    #: The installed package's own CLI module, run as `python -m MODULE
    #: --cli ...` - never imported directly (see main.py's own module
    #: docstring for why: three independent argparse CLIs sharing one
    #: process's sys.argv/sys.exit would corrupt each other).
    module: str
    #: The manifest filename this ecosystem's own updater discovers by -
    #: purely informational here (status --help text), matched inside
    #: that ecosystem's own updater, never re-checked by this dispatcher.
    manifest_file: str


ECOSYSTEMS: tuple[Ecosystem, ...] = (
    Ecosystem("hydra-umc", "HYDRA-UMC", "hydra_umc_updater.main", "hydra-umc.project.json"),
    Ecosystem("urtc", "URTC", "urtc_updater.main", "urtc.project.json"),
    Ecosystem("armor", "A.R.M.O.R.", "armor_updater.main", "armor.project.json"),
)

ECOSYSTEMS_BY_KEY: dict[str, Ecosystem] = {ecosystem.key: ecosystem for ecosystem in ECOSYSTEMS}
