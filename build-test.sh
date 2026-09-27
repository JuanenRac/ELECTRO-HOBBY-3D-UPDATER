#!/usr/bin/env bash
# ELECTRO-HOBBY-3D-UPDATER - build-test.sh
# Non-mutating build verification: same install as build.sh, then the real
# pytest suite. Never bumps a version or writes CHANGELOG.md.
# GPL-3.0-or-later.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

if [ ! -d .venv ]; then
    python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install -e ".[dev]"
python -m pytest tests -q

echo "BUILD_TEST_RESULT=PASS"
if [[ -t 0 ]]; then read -r -p "Press Enter to close..."; fi
