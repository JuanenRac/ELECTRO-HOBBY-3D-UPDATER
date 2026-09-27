#!/usr/bin/env bash
# ELECTRO-HOBBY-3D-UPDATER - run.sh
# Runs the CLI. Build first (build.sh) at least once per checkout.
#
# Usage:
#   ./run.sh status --ecosystem all                     - check every ecosystem
#   ./run.sh status --ecosystem armor                    - check just one
#   ./run.sh install --ecosystem urtc <PROJECT>           - clone + build one project
#   ./run.sh update  --ecosystem hydra-umc <PROJECT>      - pull + rebuild one project
# GPL-3.0-or-later.
cd "$(dirname "${BASH_SOURCE[0]}")"

# `action` is a required subcommand (see main.py's own argparse setup) -
# running this with zero arguments used to fail with a raw "the following
# arguments are required: action" error instead of doing anything useful.
# Default to the tool's own first documented example (a read-only status
# check of all three ecosystems) instead; any real argument list, right
# or wrong, is still passed through unchanged so a real CLI mistake still
# gets argparse's own real error.
if [ "$#" -eq 0 ]; then
    set -- status --ecosystem all
fi

if [ -x .venv/bin/python ]; then
    .venv/bin/python -m electro_hobby_3d_updater.main "$@"
else
    python3 -m electro_hobby_3d_updater.main "$@"
fi
status=$?

if [[ -t 0 ]]; then read -r -p "Press Enter to close..."; fi
exit $status
