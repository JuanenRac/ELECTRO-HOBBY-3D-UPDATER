# Changelog

All notable changes to this project are documented here.

## [0.1.0] - The fourth ecosystem

- **EH3D is the fourth ecosystem:** `--ecosystem eh3d` dispatches to EH3D-UPDATER (pinned to its first release, 0.0.1), `status --ecosystem all` runs the four at the same time and prints them in the fixed order HYDRA-UMC / URTC / A.R.M.O.R. / EH3D, and `versions` lists the fourth updater too.
- **Window:** a fourth card for EH3D with its own accent and description, "Check all four" and the texts of the subtitle, the tagline and the About window, in the eight languages.
- **Documents:** the eight README files, the manifest and the keywords name the four ecosystems; the EH3D updater has been added from its own tests and has not been run through this dispatcher against a real checkout yet.
- **Tests:** the registry, the order of the report, the simultaneous run and `versions` are covered for four ecosystems (19 tests).

## [0.0.9] - Window threads, time limits, the right workspace for the sub-updater windows

- **Window:** the worker thread that runs a check used to change the log and the busy flag of an object that belongs to the window's thread, and two fast clicks could start two workers because the flag was set inside the worker. The worker now only emits signals that Qt delivers to the window's thread, and the busy flag is set before the worker starts.
- **Sub-updater windows:** "open" started the window of an updater without telling it which folder holds the projects, so an updater installed in this tool's virtual environment looked for them inside that environment. The window now starts in the chosen workspace and receives it through `HYDRA_UMC_WORKSPACE` and `ARMOR_WORKSPACE` (URTC-UPDATER uses the current folder).
- **Time limits:** `status`, `install` and `update` stop a sub-updater that has not finished after `--timeout-seconds` (900 for status, 1800 for install and update, 0 for no limit) and say so, instead of waiting for ever for a git prompt.
- **`versions`:** the hint for an updater that is behind the main branch now says to update the pinned commit in `pyproject.toml` (reinstalling would install the same pin again).
- **Scripts:** `build.sh` and `build-test.sh` find the virtual environment of Windows under Git Bash (`.venv/Scripts`) as well as `.venv/bin`.
- **Tests:** timeouts and the thread hand-over are covered (19 tests).

## [0.0.8] - Functional

- Maturity moves from scaffolding to functional: `install` has now been run for real from a clean environment (ARMOR-COMMON cloned, built, tested and promoted by the ARMOR updater), on top of the real `status` and `versions` runs.
- The URTC updater is pinned to its current commit (0.1.2), which installs an unsigned revision with a warning instead of refusing it.
- The READMEs in the eight languages say what has run for real and that `update` has not yet.

## [0.0.7] - Portuguese, updaters pinned to current commits

- European Portuguese is the eighth language: the window texts (`i18n.py`), the language selector and a full `README_por.md`; every README links to it from its language bar, and the documentation checks now require it.
- The three sub-updaters are pinned to their current commits (HYDRA-UMC-UPDATER 0.4.7, URTC-UPDATER 0.1.1, ARMOR-UPDATER 0.1.4).
- The log has a small copy button (an icon of two sheets) that copies the whole log, so it can be pasted into a message; it turns green for a moment when it has copied.

## [0.0.6] - Pinned sub-updaters, `versions`, parallel `status all`

- **Pinned dependencies:** the three sub-updaters are pinned to reviewed
  commits (HYDRA-UMC-UPDATER 0.4.6, URTC-UPDATER 0.0.7, ARMOR-UPDATER 0.0.7)
  instead of `@main`, so an install always gets exactly what was reviewed.
- **`versions` (new):** shows the installed version of each sub-updater and
  flags one that is behind its GitHub `main` (exit code 2); `--offline`
  shows only what is installed.
- **`status --ecosystem all` runs the three at the same time** and prints
  each report whole, in the fixed HYDRA-UMC / URTC / A.R.M.O.R. order.
- **build-test.sh/.bat** install the dependencies only when `pyproject.toml`
  changed since the last run (16 s -> 2 s on a repeat run); otherwise they
  only relink this project.
- **Tests:** 16 (new: parallel run, output order, `versions` online and
  offline).
- READMEs in all 7 languages: real repository counts from a fresh
  `status --ecosystem all` (55 HYDRA-UMC, 7 URTC, 17 A.R.M.O.R.), the
  pinned dependencies, `versions`, and the limits inherited from the
  sub-updaters (ARMOR-UPDATER breaking itself when it updates itself; only
  URTC-UPDATER verifies commit signatures).

## [0.0.5] - The logo shows when the updater is opened from Electro Hobby 3D Updater

- The window icon and the emblem at the top of the window are now looked for inside the package (`assets/`), so they also show when it is installed and not run from its own folder.

## [0.0.4] - The check box, an About window and the icon

- **The check box *Without asking GitHub* no longer sits on top of its text:** it had no text of its own, so Qt centred its box over the label; the text now belongs to the check box.
- **About window**, like the one of the HYDRA-UMC, URTC and A.R.M.O.R. updaters: emblem, name, what it does, version, author, email, license and a button to open the project on GitHub, in the seven languages. It opens from the button next to the version at the bottom of the window.
- **Icon:** the window and the taskbar show the emblem of Electro Hobby 3D (`images/ELECTRO_HOBBY_3D_ICON.svg` and an `.ico` with seven sizes made from it), and the emblem also heads the window. The window is given its icon itself and the process its own identity on Windows, so it does not depend on the application-wide icon being picked up.

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
