# =============================================================================
# ELECTRO-HOBBY-3D-UPDATER - tests/test_versions_padding.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""`versions` compares a three-number version with a four-number one as equal when the missing number is zero."""
from __future__ import annotations

import argparse

from electro_hobby_3d_updater.main import show_versions


def test_an_installed_0_8_0_is_not_behind_a_latest_0_8_0_0(capsys):
    args = argparse.Namespace(offline=False)
    assert show_versions(args, installed=lambda _d: "0.8.0", latest=lambda _r: "0.8.0.0") == 0
    assert "BEHIND" not in capsys.readouterr().out


def test_a_real_difference_is_still_behind(capsys):
    args = argparse.Namespace(offline=False)
    assert show_versions(args, installed=lambda _d: "0.8.0", latest=lambda _r: "0.8.0.1") == 2
