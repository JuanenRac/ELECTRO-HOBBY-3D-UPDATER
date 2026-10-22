# =============================================================================
# ELECTRO-HOBBY-3D-UPDATER - The four real ecosystems: ecosystems.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The one place that names JuanenRac's (Electro Hobby 3D) four real,
independent software ecosystems and which installed package/CLI module
answers for each one. Adding a fifth ecosystem in the future is a one-line
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
    #: docstring for why: four independent argparse CLIs sharing one
    #: process's sys.argv/sys.exit would corrupt each other).
    module: str
    #: The manifest filename this ecosystem's own updater discovers by -
    #: purely informational here (status --help text), matched inside
    #: that ecosystem's own updater, never re-checked by this dispatcher.
    manifest_file: str
    #: The pip distribution name of that updater (`versions` reads its
    #: installed version) and its GitHub repository (`versions` reads the
    #: latest version from that repository's own pyproject.toml).
    distribution: str
    repository: str


ECOSYSTEMS: tuple[Ecosystem, ...] = (
    Ecosystem("hydra-umc", "HYDRA-UMC", "hydra_umc_updater.main", "hydra-umc.project.json", "hydra-umc-updater", "HYDRA-UMC-UPDATER"),
    Ecosystem("urtc", "URTC", "urtc_updater.main", "urtc.project.json", "urtc-updater", "URTC-UPDATER"),
    Ecosystem("armor", "A.R.M.O.R.", "armor_updater.main", "armor.project.json", "armor-updater", "ARMOR-UPDATER"),
    Ecosystem("eh3d", "EH3D", "eh3d_updater.main", "eh3d.project.json", "eh3d-updater", "EH3D-UPDATER"),
)

ECOSYSTEMS_BY_KEY: dict[str, Ecosystem] = {ecosystem.key: ecosystem for ecosystem in ECOSYSTEMS}
