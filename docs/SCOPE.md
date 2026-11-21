# ELECTRO-HOBBY-3D-UPDATER: scope

Status: **host-test**. ELECTRO-HOBBY-3D-UPDATER is a command line and a window that hand a job to the updater of one of the four ecosystems. It is tried on a computer against a fake process runner, and by hand by the maintainer on his own repositories: `status` has run for real and `install` once; `update` has not. This page says what it is for, what it will not do and where it sits among the other programs of the suite.

## Purpose

The one place from which a person who works with more than one ecosystem of Electro Hobby 3D sees all of them and picks the one to update. It installs the four updaters as pinned dependencies and runs the chosen one as a separate process; it holds no discovery, install or update logic of its own.

## What it does

* Runs `status` for one ecosystem, or for all four at the same time, and prints each report whole in a fixed order, saying which failed without stopping at the first.
* Hands `install` and `update` over to the updater of exactly one ecosystem with exactly one project name, and passes on the exit code of that updater.
* Refuses a project name that looks like an option before anything runs, and forwards the workspace explicitly (by default the parent folder of the tool).
* Stops an updater that does not finish within a time limit, together with the processes it started.
* Shows with `versions` the installed version of each updater and flags one that is behind the published one; `tools/check_pins.py` does the same for the pins of the repository.
* Opens a window (a card per ecosystem and a log, in eight languages) when it is run without arguments.

## What it will not do

* No update of everything across the ecosystems: `install` and `update` take one ecosystem and one project, and `all` is only for `status`.
* No discovery of projects: each ecosystem finds its own through the manifest of each repository.
* No signature check of its own: unsigned revisions are left to the updater that is run, which asks for its own confirmation.
* No control of any machine, and no change of anything on its own.

## Where it sits

* **It reads:** the options of the command line, the pins in `pyproject.toml`, the version of each updater that is installed and, only when it is not offline, the version published on GitHub.
* **It writes:** nothing of its own: the files that change are the ones that the updater it runs changes, one project at a time.
* **It is read by:** the person who runs it from a terminal or from the window; no other program of the suite depends on it.
* **It depends on:** the four updaters of the ecosystems, installed as pinned dependencies, and `PySide6` for the window only.

## What it never decides

Whether a revision of a project is good to install. That belongs to the updater of the ecosystem and to the person who reads the confirmation it asks for; this tool only passes the request on, so a project that was updated is not a project that was checked.

The requirements of the program, with the state of each and the test that shows it, are in `REQUIREMENTS.md`; the state in a paragraph is in `STATUS.md`.
