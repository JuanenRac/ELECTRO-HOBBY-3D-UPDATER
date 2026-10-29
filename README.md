<p align="center">
  <img src="images/ELECTRO_HOBBY_3D_BANNER.svg" alt="ELECTRO-HOBBY-3D-UPDATER banner" width="100%">
</p>

# 🧩 ELECTRO-HOBBY-3D-UPDATER

<p align="center">🇺🇸 <b>English</b> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### One command line and one window for all four Electro Hobby 3D ecosystems: pick a system, download and update its packages through the updater that system already has

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Python%203.10%2B-3776AB.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.1.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-4CAF50.svg" alt="Maturity">
</p>

---

**Honesty check - what actually runs today:** this is a thin dispatcher, not a fifth implementation of ecosystem discovery: it holds no manifest-parsing, install or update logic of its own. Each of the four ecosystems has its own updater that finds its projects through the `<ecosystem>.project.json` manifest of every repository; this tool installs the four as pinned dependencies and runs the one you pick as a separate process (`status` for all four at once). The dispatching and the commands it builds are tested (18 tests pass, with a fake process runner). `status --ecosystem all` has been run for real against a real checkout of three of the ecosystems and `install` once from a clean environment (one project cloned, built, tested and promoted by the A.R.M.O.R. updater); `update` has not been run for real, and the hand-over to the EH3D updater was added from that updater's own tests and has not been run through this tool against a real checkout.

---

> **Safety and security status:** it replaces files on your machine through the updaters it runs, so it does only what each of them does, one project at a time and after the confirmation that updater asks for. It does not run anything by itself, never updates "everything across the ecosystems", and controls no machine. Each updater is pinned to a reviewed commit, never to a moving branch; unsigned revisions are installed with a warning unless that updater is set to require signatures.

## 📋 At a glance

| | |
|---|---|
| Version | `0.1.1` |
| Maturity | Functional |
| Tests | 18 |
| Stack | Python 3.10+ (PySide6 for the window) |
| On real hardware | Not applicable: it runs on the PC of the person using it |

**Jump to:** [Overview](#-overview) · [Architecture](#-architecture) · [Quick start](#-quick-start) · [Testing](#-testing) · [Structure](#-repository-structure) · [Related](#-related-projects)

## 🚦 Project status

Each line is one part of this repository and the light says how far it is today. It is written from what the repository can show (tests, builds, runs), not from what is planned.

🟢 Done and verified · 🟡 Works, with known limits · 🟠 Partly done or not verified yet · 🔴 Not done or not working

| Area | State | What it means here |
|---|---|---|
| Software | 🟡 | A thin dispatcher: it holds no discovery, install or update logic of its own and hands `--ecosystem hydra-umc\|urtc\|armor\|eh3d` over to the updater of each ecosystem, which it installs as pinned dependencies. |
| Tests | 🟢 | 18 tests pass (`pytest`) against a fake process runner; one more is skipped when PySide6 is not installed. |
| Real use | 🟠 | `status` has run against a real checkout of three of the ecosystems and `install` has run once from a clean environment; `update` has not been run for real. |
| Window | 🟡 | The window (a card per ecosystem, a log, eight languages) opens each ecosystem's own updater; its texts and its thread rules are tested, the rest only by hand. |
| Integration | 🟠 | The hand-over to the EH3D updater was added from that updater's own tests and has not been run through this dispatcher against a real checkout. |
| Security | 🟡 | Each sub-updater is pinned to a reviewed commit, never to a moving branch; every run is its own process with a time limit; unsigned revisions are installed with a warning and there has been no independent review. |
| Real hardware | 🟢 | Not applicable: it runs on the PC of the person using it. |
| Documentation | 🟢 | README in eight languages, checked against the manifest and the changelog on every change. |

## 🎯 Overview

* **One tool, four ecosystems:** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER), [URTC](https://github.com/JuanenRac/URTC-UPDATER), [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) and [EH3D](https://github.com/JuanenRac/EH3D-UPDATER) each have their own updater, independently tested. This project re-implements none of that: it installs all four as dependencies and dispatches `--ecosystem hydra-umc|urtc|armor|eh3d` to the matching one.
* **Discovery stays with each updater:** every ecosystem finds its projects through the manifest of each repository (`hydra-umc.project.json`, `urtc.project.json`, `armor.project.json`, `eh3d.project.json`), so a new repository appears in its ecosystem by having a manifest and nothing in this tool lists the projects. This tool's own manifest, `electro-hobby-3d.project.json`, belongs to none of the four by design.
* **Pinned, reviewed dependencies:** `pyproject.toml` pins each updater to a reviewed commit, never to a moving `main`. `versions` shows the installed version of each one and flags any that is behind GitHub.
* **A separate process every time:** each call runs `python -m <that ecosystem's module> --cli ...` as its own interpreter; four argparse programs that may each call `sys.exit()` would corrupt each other if composed in one process.
* **`status --ecosystem all`:** runs the four status checks at the same time, prints each report whole in a fixed order and says which failed without stopping at the first.
* **`install` and `update` always need one ecosystem and one project name:** there is no "update everything across every ecosystem", the same stance each updater takes.
* **A window:** with no arguments a Qt Quick window shows a card per ecosystem and a log, opens each ecosystem's own updater and asks it for its status, in eight languages.

## 🧩 Role in Electro Hobby 3D

ELECTRO-HOBBY-3D-UPDATER is the fifth piece of the updater family of Electro Hobby 3D and sits above the four ecosystems: it wraps the other four rather than replacing any of them. It is the one place where a person who works with more than one ecosystem can see all of them and pick the one to update.

## 🏛️ Architecture

<p align="center">
  <img src="images/architecture.svg" alt="ELECTRO-HOBBY-3D-UPDATER architecture: who uses it, what it holds and what it depends on" width="100%">
</p>

How the parts of this repository fit together: who uses it, what it holds and what it depends on. The picture is drawn from `docs/architecture.json` and checked against the code.

## 🔒 Security & Safety

| Threat | Defense |
|---|---|
| A moving or compromised `main` of an updater reaching this tool | each updater is pinned in `pyproject.toml` to a reviewed commit, never to a branch; to move to a newer one it is reviewed first and the pin changed here |
| One updater breaking another | each call runs the updater as its own interpreter process (`python -m <module> --cli ...`), never imported into this one, so none can change another's arguments, state or exit |
| An updater that hangs (a git prompt waiting for a credential, a dead network) | a time limit on every run: 900 s for `status` and 1800 s for `install` and `update`, changeable with `--timeout-seconds` (0 means no limit) |
| An unwanted bulk change | `install` and `update` take exactly one ecosystem and one project name and refuse `--ecosystem all`; each updater asks for its own confirmation |
| Looking at the wrong folder | the workspace is always forwarded explicitly (by default the parent of this tool), because an installed updater would otherwise search under this tool's virtual environment and silently find nothing |
| A commit of unknown origin | left to each updater: unsigned revisions are installed with a warning unless that updater is told to require signatures (EH3D-UPDATER and URTC-UPDATER have that option) |
| Failure of one ecosystem hiding the others | `status --ecosystem all` runs all four, prints every report and names the ones that failed |

**What is not defended:** this tool runs whatever each updater does, with your rights, including the build script of the project you install; the updater of A.R.M.O.R. still breaks its own installation when it updates itself, so update ARMOR-UPDATER by hand; and the tool has had no independent review. Report a vulnerability privately (see [SECURITY.md](SECURITY.md)).

## 🔌 Interfaces

| Interface | What it is | Where |
|---|---|---|
| Command line | `electro-hobby-3d-updater` with `status`, `install`, `update` and `versions`; `--version`; exit codes 0, 1 (a run failed or timed out) and 2 (`versions`: an updater is behind GitHub) | `main.py` |
| Window | no arguments opens a Qt Quick window (a card per ecosystem and a log); it needs the optional `PySide6` extra | `qt_gui.py`, `qml/Main.qml` |
| To each updater | a separate process: `python -m <hydra_umc_updater.main, urtc_updater.main, armor_updater.main or eh3d_updater.main> --cli <action> [project] --workspace <folder>` | `ecosystems.py` |
| GitHub | `versions` reads the `pyproject.toml` of each updater's repository on `main` to compare versions; nothing else | `main.py` |

## ⚙️ Configuration

Nothing has to be configured; the options of the command line are the whole configuration, and everything else belongs to each updater.

| Option | Default | Range | What it does |
|---|---|---|---|
| `--ecosystem` | none | `hydra-umc`, `urtc`, `armor` or `eh3d`; `all` only for `status` | which updater does the work |
| `--workspace` | the parent folder of this tool | a folder | the workspace that every updater scans (always forwarded) |
| `--offline` (`status`, `versions`) | off | on or off | skip the GitHub check |
| `--timeout-seconds` | 900 for `status`, 1800 for `install` and `update` | a number of seconds; 0 or less means no limit | stop an updater that has not finished |
| the pins | four commits in `pyproject.toml` | a reviewed commit of each updater | which updater code is installed; changed only after reviewing a newer one |

The pins of this release are HYDRA-UMC-UPDATER 0.4.8, URTC-UPDATER 0.1.7, ARMOR-UPDATER 0.1.4 and EH3D-UPDATER 0.0.1.

## 🚀 Quick start

You need Python 3.10 or newer; the window also needs PySide6.

```bash
build.bat                                   # ./build.sh on Linux: a venv and an editable install (pulls the four pinned updaters)
pip install -e ".[dev]"                     # the same by hand; add ".[gui]" for the window
python -m pytest tests -q
electro-hobby-3d-updater status --ecosystem all
electro-hobby-3d-updater versions
electro-hobby-3d-updater install --ecosystem urtc URTC-TESTER
electro-hobby-3d-updater update  --ecosystem hydra-umc HYDRA-UMC-SERVER
```

`run.bat` / `run.sh` with no arguments open the window. `install` and `update` need one ecosystem and one project name, spelled as that ecosystem's own manifest declares it.

## 🧪 Testing

The suite has 18 tests that pass (`pytest tests`), and one more that is skipped when PySide6 is not installed. They run against a fake process runner, with no network and no real subprocess, and cover: the registry has exactly the four ecosystems; `status` runs the right module and forwards `--offline`; `status --ecosystem all` runs every ecosystem once, prints them in order, runs them at the same time and never stops at the first failure; `install` and `update` need one ecosystem and one project and reject `all`; a failing updater passes its own exit code on; the workspace defaults to the parent folder; `versions` reports the installed versions, flags an updater that is behind and never contacts GitHub with `--offline`; an updater that hangs is stopped with a clear message and a zero timeout means no limit; and the texts of the window exist in all eight languages. The CI runs `python tools/ci_validate.py` (manifest, version, changelog and README parity) and then `python tools/build_test.py`, which compiles every source and runs the suite.

## 🏗️ Build & Release

The version lives in `pyproject.toml`, in `electro-hobby-3d.project.json` and in the package, and each version has its entry in [CHANGELOG.md](CHANGELOG.md). `build.sh` / `build.bat` make a virtual environment, install this tool with its four pinned updaters and compile-check it; `build-test.sh` / `build-test.bat` do the same and then run the suite; `test.sh` / `test.bat` run only the tests, each in a live panel, and none changes the version. Releases are published on GitHub (the latest is 0.1.1); the tool is installed from this repository and is not on PyPI.

## 🩺 Troubleshooting

| Symptom | What to do |
|---|---|
| An ecosystem reports no projects | The updater scans the workspace for sibling folders with its manifest; pass `--workspace` with the folder that holds the repositories. |
| `versions` says an updater is BEHIND (exit code 2) | The pins are deliberate: review the newer commit of that updater, put it in `pyproject.toml`, bump this tool's version and reinstall. |
| The window does not open | It needs PySide6: `pip install -e ".[gui]"`; the command line works without it. |
| An updater ran for too long | It was stopped after the limit (900 s for `status`, 1800 s for `install` and `update`); raise it with `--timeout-seconds`, or 0 for no limit. |
| ARMOR-UPDATER breaks after updating itself | Its editable install points at its staging folder: update ARMOR-UPDATER by hand and run `build.bat` / `build.sh` again. |

## 📂 Repository Structure

<p align="center">
  <img src="images/repository-structure.svg" alt="Repository structure of ELECTRO-HOBBY-3D-UPDATER" width="100%">
</p>

<details>
<summary>Text version of the tree</summary>

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py                            the one place that names the four ecosystems
│   ├── main.py                                  the command line, the dispatch and the versions
│   ├── qt_gui.py qml/                           the Qt Quick window and its QML
│   ├── i18n.py                                  the words of the window in eight languages
│   └── assets/                                  the icon of the program
├── tests/                                       the dispatching against a fake process runner
├── docs/                                        the data of the Architecture and Repository Structure pictures
├── tools/                                       CI check, build check, README check, picture tools
├── images/                                      banner and the Architecture and Repository Structure pictures
├── .github/                                     CI and release workflows, issue and pull-request templates
├── build.sh build.bat                           venv, editable install and compile check in a live panel
├── build-test.sh build-test.bat                 the same, then the real test suite
├── run.sh run.bat                               start the window, or the command line with arguments
├── bump*.py                                     the scripts that raise the version
├── electro-hobby-3d.project.json                the manifest: version, role and maturity
├── pyproject.toml                               the package and the four pinned updaters
├── CHANGELOG.md                                 what changed in each version
├── SECURITY.md SUPPORT.md                       how to report a vulnerability and where to ask
└── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   how to contribute, the code of conduct and the licence
```

</details>

## 🗺️ Roadmap & Known limits

**Known limits today**

* `update` has not been run for real, and `install` only once; `status` has run against a real checkout of three ecosystems.
* The hand-over to EH3D-UPDATER has not been run through this tool against a real checkout.
* There is no "update everything across the ecosystems", by design.
* Whether a commit must be signed is up to each updater, and the A.R.M.O.R. updater breaks its own installation when it updates itself.
* The tool has had no independent review, and it is not on PyPI.

**Next**

* Run `status`, `install` and `update` for the EH3D projects through this tool on a real checkout.
* Move the pins to newer reviewed commits of the four updaters as they release.
* Run `update` for real on an ecosystem and record what shows up.

## 🌍 Languages

README and texts exist in English, Spanish, French, Italian, German, Chinese, Japanese and European Portuguese.

## 🔗 Related Projects

This tool is the fifth piece of the updater family of JuanenRac (Electro Hobby 3D); it wraps the other four rather than replacing any of them:

* [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER): detects, installs and updates the HYDRA-UMC repositories
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER): detects, installs and updates the URTC repositories
* [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER): detects, installs and updates the A.R.M.O.R. repositories
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER): detects, installs and updates the EH3D repositories
* [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC), [URTC](https://github.com/JuanenRac/URTC), [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-COMMON) and [EH3D](https://github.com/JuanenRac/EH3D-DOCS): the four ecosystems themselves

## 📚 Documentation

* [Changelog](CHANGELOG.md): every version, what changed and what was found.
* [Contributing](CONTRIBUTING.md), [Security policy](SECURITY.md) and [Support](SUPPORT.md).
* The documentation of each ecosystem's own updater lives in its repository (see Related Projects).

## 🤝 Contributing & Community

* Before a pull request run `python -m pytest tests -q` and `python tools/ci_validate.py`: both must pass. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [code of conduct](CODE_OF_CONDUCT.md).
* The README exists in eight languages: a change to the text is made in all eight files, and the two pictures are drawn from `docs/architecture.json` and `docs/structure.json` by `tools/make_architecture.py` and `tools/make_structure.py`.
* This tool must stay a dispatcher: logic that discovers, installs or updates belongs in the updater of the ecosystem, not here, and a new ecosystem is a one-line change in `ecosystems.py`.
* Report a vulnerability privately: [SECURITY.md](SECURITY.md). Questions, ideas and reports: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTHOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENSE

Software: GPL-3.0-or-later. See [LICENSE](LICENSE). Hardware designs of the suite use CERN OHL-S.
