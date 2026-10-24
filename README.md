<p align="center">
  <img src="images/ELECTRO_HOBBY_3D_BANNER.svg" alt="ELECTRO-HOBBY-3D-UPDATER banner" width="100%">
</p>

# 🧩 ELECTRO-HOBBY-3D-UPDATER

<p align="center">
  🇺🇸 <b>English</b> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a> |
  <a href="README_por.md">🇵🇹 Português</a>
</p>

### One command line for all four Electro Hobby 3D ecosystems - pick a system, download and update its packages

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-3776ab.svg" alt="Language">
  <img src="https://img.shields.io/badge/Dependencies-3%20real%20sub--updaters-2ea44f.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/Tests-13-00E5FF.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-functional-4caf50.svg" alt="Maturity">
</p>

---

**Honesty check - what runs today:** **Maturity: functional.** This is a thin dispatcher, not a fifth implementation of ecosystem discovery: it holds no manifest-parsing, install or update logic of its own. `dispatch()` and its command-building (19 tests, all against a fake subprocess runner) are real and tested; `status --ecosystem all` has been run for real against a real checkout of all three ecosystems (55 HYDRA-UMC + 7 URTC + 17 A.R.M.O.R. repositories correctly found) - `install` has also been run for real, from a clean environment, and ARMOR-COMMON was cloned, built, tested and promoted by the ARMOR updater (unsigned revisions are installed with a warning); `update` has not been run for real. A real bug was found and fixed during that first real run: see `CHANGELOG.md`'s `--workspace` entry. The EH3D updater was added from its own tests (317, against a fake GitHub) and has not been run through this dispatcher against a real checkout yet.

---

## 📋 At a glance

| | |
|---|---|
| Version | `0.1.1` |
| Maturity | Functional |
| Stack | Python 3.10+ / hydra-umc-updater / urtc-updater / eh3d-updater / armor-updater |
| Target | The PC of the person using it |
| On real hardware | Not applicable: nothing here runs on hardware |

## 🚦 Project status

Each line is one part of this repository and the light says how far it is today. It is written from what the repository can show (tests, builds, runs), not from what is planned.

🟢 Done and verified · 🟡 Works, with known limits · 🟠 Partly done or not verified yet · 🔴 Not done or not working

| Area | State | What it means here |
|---|---|---|
| Software | 🟡 | A thin dispatcher: it holds no discovery, install or update logic of its own and hands `--ecosystem hydra-umc\|urtc\|armor\|eh3d` over to the updater of each ecosystem, which it installs as pinned dependencies. |
| Tests | 🟢 | 19 tests cover the dispatching and the commands it builds, all against a fake subprocess runner. |
| Real use | 🟠 | `status` has run against a real checkout of all three older ecosystems, and `install` has run once from a clean environment; `update` has not been run for real. |
| Integration | 🟠 | The hand-over to the EH3D updater was added from that updater's own tests and has not been run through this dispatcher against a real checkout. |
| Security | 🟡 | Each sub-updater is pinned to a reviewed commit, never to a moving branch; unsigned revisions are installed with a warning, and there has been no independent review. |
| Real hardware | 🟢 | Not applicable: it runs on the PC of the person using it. |
| Documentation | 🟢 | README in eight languages, checked against the manifest and the changelog on every change. |

## 🎯 Overview

* **One tool, four real ecosystems:** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER), [URTC](https://github.com/JuanenRac/URTC-UPDATER), [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) and [EH3D](https://github.com/JuanenRac/EH3D-UPDATER) each already have their own dedicated, independently-tested updater. This project does not re-implement any of that - it installs all four as real dependencies and dispatches `--ecosystem hydra-umc|urtc|armor|eh3d` to the matching one.
* **Pinned, reviewed dependencies:** `pyproject.toml` pins each sub-updater to a reviewed commit, never to a moving `main`, so an install always gets exactly what was reviewed. `versions` shows the installed version of each one and flags any that is behind GitHub.
* **A real, separate subprocess every time.** Each call runs `python -m <that ecosystem's module> --cli ...` as its own interpreter process - never imports another CLI's `main()` into this one. Four independent argparse programs, each free to parse `sys.argv` and call `sys.exit()`, would corrupt each other if composed in-process.
* **`status --ecosystem all`:** runs the four ecosystems' own status checks at the same time, prints each report whole in a fixed order, and says which one(s) failed without stopping at the first.
* **`install`/`update` always need one ecosystem and one project name.** There is no "update everything across every ecosystem" here, the same stance each sub-updater's own CLI already takes.
* **Inherited limits:** this tool runs whatever each sub-updater does. A.R.M.O.R.'s updater still breaks its own installation when it updates itself (the editable install points at its staging directory), so update ARMOR-UPDATER by hand for now. URTC-UPDATER can require signed commits (`URTC_UPDATER_REQUIRE_SIGNED=1`); the other two do not verify signatures yet.

## 📂 Repository Structure

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py   # The one place naming the four real ecosystems and their CLI module
│   ├── main.py         # argparse CLI + dispatch() - builds and runs the right subprocess command
│   ├── i18n.py         # The words of the window in the eight languages
│   ├── qt_gui.py       # Qt Quick window (a card per ecosystem, a log) - opens each ecosystem's own updater
│   └── qml/Main.qml    # The window's QML
├── tests/               # 19 tests against a fake subprocess runner
├── tools/               # ci_validate.py, build_test.py, _doc_policy.py, _readme_parity.py
├── build.sh / build.bat         # venv + editable install (pulls the 4 real dependencies) + compile-check
├── build-test.sh / build-test.bat  # same install, then the real pytest suite
└── run.sh / run.bat              # CLI entry point (no arguments: the window)
```

## 🛠️ Development Environment

```bash
pip install -e ".[dev]"                 # also installs hydra-umc-updater, urtc-updater, armor-updater, eh3d-updater from GitHub
python -m pytest tests -q               # 19 tests, no network or real subprocess needed
electro-hobby-3d-updater status --ecosystem all               # check every ecosystem (in parallel)
electro-hobby-3d-updater versions                             # installed version of each updater, and whether it is behind GitHub
electro-hobby-3d-updater status --ecosystem armor             # check just one
electro-hobby-3d-updater install --ecosystem urtc URTC-TESTER # clone + build one project not yet installed
electro-hobby-3d-updater update  --ecosystem hydra-umc HYDRA-UMC-SERVER # pull + rebuild one project already installed
```

## 🔗 Related Projects

This tool is the fifth piece of JuanenRac's (Electro Hobby 3D) own updater family - it wraps the other four rather than replacing any of them:

* **[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)** - detects, installs and updates the HYDRA-UMC ecosystem's own repositories
* **[URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)** - detects, installs and updates the URTC ecosystem's own repositories
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - detects, installs and updates the A.R.M.O.R. ecosystem's own repositories
* **[EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER)** - detects, installs and updates the EH3D ecosystem's own repositories
* **ELECTRO-HOBBY-3D-UPDATER** (this repository) - dispatches to whichever of the four the user picks

And the four real ecosystems themselves: **[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)** (industrial multi-robot cell control), **[URTC](https://github.com/JuanenRac/URTC)** (the Universal Robot Tool Controller platform), **[A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-COMMON)** (perimeter security and home automation), **[EH3D](https://github.com/JuanenRac/EH3D)** (the fabrication suite: CAM, CNC and machine control).

## 📚 Documentation & Community

* **[Changelog of this repository](CHANGELOG.md)**
* Questions, ideas and reports: electrohobby3d@gmail.com

## 👤 AUTHOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENSE

GPL-3.0-or-later - see [LICENSE](LICENSE).
