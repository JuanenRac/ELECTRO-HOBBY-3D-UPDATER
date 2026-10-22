#!/usr/bin/env bash
# ELECTRO-HOBBY-3D-UPDATER - build.sh
# Creates/uses a project-local .venv, installs this project plus its three
# real ecosystem-updater dependencies (from GitHub) in editable mode, then
# compile-checks every module. GPL-3.0-or-later.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

# The venv is put first on the PATH instead of being activated: the python first on the PATH may be a stripped one (for example the one of ESP-IDF) whose venv has no activate script.
if [ ! -x .venv/bin/python ] && [ ! -x .venv/Scripts/python.exe ]; then
    (python3 -m venv .venv 2>/dev/null || python -m venv .venv)
fi
if [ -x .venv/bin/python ]; then VENV_BIN="$PWD/.venv/bin"; else VENV_BIN="$PWD/.venv/Scripts"; fi
if [ ! -x "$VENV_BIN/python" ] && [ ! -x "$VENV_BIN/python.exe" ]; then echo "ERROR: the venv has no python; delete the .venv folder and run this again." >&2; exit 1; fi
export VIRTUAL_ENV="$PWD/.venv"
export PATH="$VENV_BIN:$PATH"

python -m pip install -e ".[dev,gui]"
python -m compileall -q src

echo "BUILD_RESULT=PASS"
if [[ -t 0 ]]; then read -r -p "Press Enter to close..."; fi
