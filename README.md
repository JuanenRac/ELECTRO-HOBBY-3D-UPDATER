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
  <a href="README_jpn.md">🇯🇵 日本語</a>
</p>

### One command line for all three Electro Hobby 3D ecosystems - pick a system, download and update its packages

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-3776ab.svg" alt="Language">
  <img src="https://img.shields.io/badge/Dependencies-3%20real%20sub--updaters-2ea44f.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/Tests-10-00E5FF.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-ff9800.svg" alt="Maturity">
</p>

---

**Honesty check - what runs today:** **Maturity: scaffolding.** This is a thin dispatcher, not a fourth implementation of ecosystem discovery: it holds no manifest-parsing, install or update logic of its own. `dispatch()` and its command-building (10 tests, all against a fake subprocess runner) are real and tested; `status --ecosystem all` has been run for real against a real checkout of all three ecosystems (55 HYDRA-UMC + 7 URTC + 15 A.R.M.O.R. repositories correctly found) - `install`/`update` have not. A real bug was found and fixed during that first real run: see `CHANGELOG.md`'s `--workspace` entry.

---

## 🎯 Overview

* **One tool, three real ecosystems:** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER), [URTC](https://github.com/JuanenRac/URTC-UPDATER) and [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) each already have their own dedicated, independently-tested updater. This project does not re-implement any of that - it installs all three as real dependencies (straight from their own GitHub repositories) and dispatches `--ecosystem hydra-umc|urtc|armor` to the matching one.
* **A real, separate subprocess every time.** Each call runs `python -m <that ecosystem's module> --cli ...` as its own interpreter process - never imports another CLI's `main()` into this one. Three independent argparse programs, each free to parse `sys.argv` and call `sys.exit()`, would corrupt each other if composed in-process; a subprocess is the same isolation a person gets typing each command by hand.
* **`status --ecosystem all`:** the one thing no single sub-updater does on its own - runs all three ecosystems' own status check in sequence and reports which one(s) failed, without stopping at the first.
* **`install`/`update` always need one ecosystem and one project name.** There is no "update everything across every ecosystem" here, the same non-negotiable stance each sub-updater's own CLI already takes for its own projects.

## 📂 Repository Structure

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py   # The one place naming the three real ecosystems and their CLI module
│   └── main.py         # argparse CLI + dispatch() - builds and runs the right subprocess command
├── tests/               # 9 tests against a fake subprocess runner
├── tools/               # ci_validate.py, build_test.py, _doc_policy.py, _readme_parity.py
├── build.sh / build.bat         # venv + editable install (pulls the 3 real dependencies) + compile-check
├── build-test.sh / build-test.bat  # same install, then the real pytest suite
└── run.sh / run.bat              # CLI entry point
```

## 🛠️ Development Environment

```bash
pip install -e ".[dev]"                 # also installs hydra-umc-updater, urtc-updater, armor-updater from GitHub
python -m pytest tests -q               # 9 tests, no network or real subprocess needed
electro-hobby-3d-updater status --ecosystem all               # check every ecosystem in sequence
electro-hobby-3d-updater status --ecosystem armor             # check just one
electro-hobby-3d-updater install --ecosystem urtc URTC-TESTER # clone + build one project not yet installed
electro-hobby-3d-updater update  --ecosystem hydra-umc HYDRA-UMC-SERVER # pull + rebuild one project already installed
```

## 🔗 Related Projects

This tool is the fourth piece of JuanenRac's (Electro Hobby 3D) own updater family - it wraps the other three rather than replacing any of them:

* **[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)** - detects, installs and updates the HYDRA-UMC ecosystem's own repositories
* **[URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)** - detects, installs and updates the URTC ecosystem's own repositories
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - detects, installs and updates the A.R.M.O.R. ecosystem's own repositories
* **ELECTRO-HOBBY-3D-UPDATER** (this repository) - dispatches to whichever of the three the user picks

And the three real ecosystems themselves: **[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)** (industrial multi-robot cell control), **[URTC](https://github.com/JuanenRac/URTC)** (the Universal Robot Tool Controller platform), **[A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-COMMON)** (perimeter security and home automation).

## 📚 Documentation & Community

* **[Changelog of this repository](CHANGELOG.md)**
* Questions, ideas and reports: electrohobby3d@gmail.com

## 👤 AUTHOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENSE

GPL-3.0-or-later - see [LICENSE](LICENSE).
