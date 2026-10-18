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
# the virtual environment of Linux/macOS (bin) or of Windows under Git Bash (Scripts)
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
else
    source .venv/Scripts/activate
fi

# Dependencies (the three pinned sub-updaters, pytest) are installed only
# when pyproject.toml changed since the last run - not re-downloaded on
# every build-test - and this project itself is (re)linked without touching
# them.
stamp=".venv/.deps-installed"
want="$(python -c 'import hashlib,sys; print(hashlib.sha256(open("pyproject.toml","rb").read()).hexdigest())')"
if [ ! -f "$stamp" ] || [ "$(cat "$stamp")" != "$want" ]; then
    python -m pip install -e ".[dev]"
    echo "$want" > "$stamp"
else
    python -m pip install --no-deps -e . >/dev/null
fi
python -m pytest tests -q

echo "BUILD_TEST_RESULT=PASS"
if [[ -t 0 ]]; then read -r -p "Press Enter to close..."; fi
