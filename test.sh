#!/usr/bin/env bash
# ELECTRO-HOBBY-3D-UPDATER test launcher: the tests and the checks of build-test, shown in a live panel; the version is never changed. GPL-3.0-or-later.
PRETTY_MODE=test exec bash "$(dirname "$0")/build-test.sh" "$@"
