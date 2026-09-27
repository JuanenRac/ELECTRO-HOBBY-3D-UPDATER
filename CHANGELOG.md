# Changelog: ELECTRO-HOBBY-3D-UPDATER

All notable changes to this project will be documented in this file. The
version number follows this ecosystem's "odometer" scheme: PATCH +1 on
every real build, rolling into MINOR past 9 (`0.0.9` -> `0.1.0`); MAJOR is
bumped manually only.

## [0.0.1] - First release: one updater for all three ecosystems

- **New project.** ELECTRO-HOBBY-3D-UPDATER is a thin dispatcher over JuanenRac's (Electro Hobby 3D) three real, independent ecosystem updaters - hydra-umc-updater, urtc-updater and armor-updater - each installed as a real dependency straight from its own GitHub repository. `--ecosystem hydra-umc|urtc|armor` picks which one actually runs; `status --ecosystem all` runs all three in sequence and reports which one(s) failed without stopping at the first.
- Deliberately holds no manifest-parsing, discovery or install/update logic of its own: every `status`/`install`/`update` call runs the chosen ecosystem's own `python -m <module> --cli ...` as a real, separate subprocess - the same isolation a person gets typing each command by hand.
- **Real bug found and fixed while first exercising this end to end:** every sub-updater's own `default_workspace_root()` resolves relative to its OWN installed package location, correct only when it runs from its own local sibling checkout. Installed as a regular dependency of this project instead (pulled straight from GitHub), that heuristic silently resolved to somewhere under this project's own `.venv` and found zero projects, no error. Fixed by always forwarding an explicit `--workspace` to every dispatched call, defaulting to this project's own parent directory. Verified for real afterward: `status --ecosystem all` correctly found all 55 HYDRA-UMC, 7 URTC and 15 A.R.M.O.R. repositories on a real checkout.
- 10 tests, all against a fake subprocess runner so the suite never actually needs the three real ecosystem updaters installed or a real network call.
