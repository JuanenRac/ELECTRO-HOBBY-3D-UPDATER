# ELECTRO-HOBBY-3D-UPDATER: status

## Current state

ELECTRO-HOBBY-3D-UPDATER is a thin dispatcher that works on a computer: the dispatching, the commands it builds, the versions and the pins are covered by tests against a fake process runner, with no network and no real subprocess. `status` has run against a real checkout of three of the ecosystems and `install` once from a clean environment; `update` has not been run for real, and the hand-over to the EH3D updater has not been run through this tool against a real checkout.

## Capabilities

The official state of each capability is in `REQUIREMENTS.md`. The register has 34 requirements: 29 implemented, 1 prototype, 4 planned and 0 validated. By progress: 29 done, 1 partial, 0 pending and 4 blocked. This page never states a state that `REQUIREMENTS.md` does not.

## Open questions

* Whether `update` should offer a preview in every ecosystem or only where the updater has one (today it is forwarded only where it exists).
* Whether the window should show the versions as well as the status.

## What it needs from other repositories

* The four updaters, each at the commit named in `pyproject.toml`; a newer one is reviewed before its pin moves.
* `PySide6`, for the window only.

## Known technical debt and omitted tests

* `update` has never been run for real through this tool; only the commands it builds are tested.
* The window is tested for its texts and its thread rules, not by a person at a screen on each system.
* The updater of A.R.M.O.R. breaks its own installation when it updates itself, so it is updated by hand.
