# =============================================================================
# ELECTRO-HOBBY-3D-UPDATER - Text of the child processes: children.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""How the updaters this tool starts write their text, and how it is read.

A Python child writing to a pipe uses the code page of the system: a project or file name that it cannot hold ends the child with an error. Captured output is asked for in
UTF-8 and read as UTF-8; output that goes straight to the console keeps the encoding of the console and only replaces what it cannot hold. A byte that cannot be decoded is
replaced, never an error."""
from __future__ import annotations

import os

#: Keyword arguments to read captured text.
CAPTURED_TEXT = {"encoding": "utf-8", "errors": "replace"}


def child_environment(*, captured: bool, base: dict[str, str] | None = None) -> dict[str, str]:
    environment = dict(os.environ if base is None else base)
    if captured:
        environment["PYTHONIOENCODING"] = "utf-8:replace"
    else:
        environment.setdefault("PYTHONIOENCODING", ":replace")   # a choice of the person is kept
    return environment


def print_whatever_the_console_holds(*streams) -> None:
    """A character the console cannot hold is shown with a replacement mark instead of ending the command."""
    for stream in streams:
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(errors="replace")
