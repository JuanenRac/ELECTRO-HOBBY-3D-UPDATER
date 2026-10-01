"""ELECTRO-HOBBY-3D-UPDATER - a thin dispatcher over the three real,
independent ecosystem updaters by the same author (JuanenRac / Electro
Hobby 3D): hydra-umc-updater, urtc-updater and armor-updater. It holds no
discovery, manifest-parsing or install/update logic of its own - each
ecosystem's own updater already has that, real and tested, and duplicating
it here would create a second, independently-drifting implementation.

pyproject.toml's own `version` field is the real source of truth -
`__version__` below is a mirror bump_version.py keeps in sync on every
real build, kept here (rather than reading it back out of installed
package metadata) so this module has a version to report even before
`pip install -e .` has ever run against a bare checkout.
"""
__version__ = "0.0.3"
