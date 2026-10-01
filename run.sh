#!/usr/bin/env bash
# ELECTRO-HOBBY-3D-UPDATER - run.sh
# Opens the window (no arguments) or runs the CLI. Build first (build.sh) at least once per checkout.
#
# Usage:
#   ./run.sh status --ecosystem all                     - check every ecosystem
#   ./run.sh status --ecosystem armor                    - check just one
#   ./run.sh install --ecosystem urtc <PROJECT>           - clone + build one project
#   ./run.sh update  --ecosystem hydra-umc <PROJECT>      - pull + rebuild one project
# GPL-3.0-or-later.
cd "$(dirname "${BASH_SOURCE[0]}")"

# No arguments (a double click) opens the window; with arguments this is the
# command line, exactly as before.

if [ -x .venv/bin/python ]; then
    .venv/bin/python -m electro_hobby_3d_updater.main "$@"
else
    python3 -m electro_hobby_3d_updater.main "$@"
fi
status=$?

if [[ -t 0 ]]; then read -r -p "Press Enter to close..."; fi
exit $status
