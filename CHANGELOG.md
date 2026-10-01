# Changelog: ELECTRO-HOBBY-3D-UPDATER

All notable changes to this project will be documented in this file. The
version number follows this ecosystem's "odometer" scheme: PATCH +1 on
every real build, rolling into MINOR past 9 (`0.0.9` -> `0.1.0`); MAJOR is
bumped manually only.

## [0.0.3] - A window, like the other updaters

- **A Qt Quick window** (same family as the HYDRA-UMC, URTC and A.R.M.O.R. updaters): one card per ecosystem that opens that ecosystem's own updater or asks it for its status, a "check all three" button, an offline switch, the workspace folder, a log of what the updaters answered, and the seven languages. It is still only a dispatcher: nothing in it discovers, installs or updates by itself.
- **No arguments opens the window** (a double click on `run.bat` / `run.sh`); with arguments it is the command line exactly as before. The window needs the optional `gui` extra (`pip install -e ".[gui]"`, done by `build`); without it a clear hint is printed.
- 2 new tests (12 in all).

## [0.0.2] - run.bat/run.sh errored out when double-clicked with no arguments

- **Real bug, reported by the user:** `action` is a required argparse subcommand, so running `run.bat`/`run.sh` with zero arguments - exactly what a double-click does - always failed immediately with a raw `the following arguments are required: action` error instead of doing anything useful. Both launchers now default to the tool's own first documented example, `status --ecosystem all` (a real, read-only check of all three ecosystems), when given no arguments; any real argument list, right or wrong, is still passed through unchanged, so a genuine CLI mistake still gets argparse's own real error. `main.py` itself is untouched - the default lives in the convenience launcher, not the CLI contract.

## [0.0.1] - First release: one updater for all three ecosystems

- **New project.** ELECTRO-HOBBY-3D-UPDATER is a thin dispatcher over JuanenRac's (Electro Hobby 3D) three real, independent ecosystem updaters - hydra-umc-updater, urtc-updater and armor-updater - each installed as a real dependency straight from its own GitHub repository. `--ecosystem hydra-umc|urtc|armor` picks which one actually runs; `status --ecosystem all` runs all three in sequence and reports which one(s) failed without stopping at the first.
- Deliberately holds no manifest-parsing, discovery or install/update logic of its own: every `status`/`install`/`update` call runs the chosen ecosystem's own `python -m <module> --cli ...` as a real, separate subprocess - the same isolation a person gets typing each command by hand.
- **Real bug found and fixed while first exercising this end to end:** every sub-updater's own `default_workspace_root()` resolves relative to its OWN installed package location, correct only when it runs from its own local sibling checkout. Installed as a regular dependency of this project instead (pulled straight from GitHub), that heuristic silently resolved to somewhere under this project's own `.venv` and found zero projects, no error. Fixed by always forwarding an explicit `--workspace` to every dispatched call, defaulting to this project's own parent directory. Verified for real afterward: `status --ecosystem all` correctly found all 55 HYDRA-UMC, 7 URTC and 15 A.R.M.O.R. repositories on a real checkout.
- 10 tests, all against a fake subprocess runner so the suite never actually needs the three real ecosystem updaters installed or a real network call.
