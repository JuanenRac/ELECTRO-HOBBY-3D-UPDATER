#!/usr/bin/env bash
# ELECTRO-HOBBY-3D-UPDATER - build.sh
# Creates/uses a project-local .venv, installs this project plus its three
# real ecosystem-updater dependencies (from GitHub) in editable mode, then
# compile-checks every module. GPL-3.0-or-later.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

if [ ! -d .venv ]; then
    python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install -e ".[dev,gui]"
python -m compileall -q src

echo "BUILD_RESULT=PASS"
if [[ -t 0 ]]; then read -r -p "Press Enter to close..."; fi
