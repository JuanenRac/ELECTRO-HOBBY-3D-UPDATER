<p align="center">
  <img src="images/ELECTRO_HOBBY_3D_BANNER.svg" alt="ELECTRO-HOBBY-3D-UPDATER banner" width="100%">
</p>

# 🧩 ELECTRO-HOBBY-3D-UPDATER

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <b>🇩🇪 Deutsch</b> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a> |
  <a href="README_por.md">🇵🇹 Português</a>
</p>

### Eine einzige Kommandozeile fuer alle vier Electro-Hobby-3D-Oekosysteme - Oekosystem waehlen, seine Pakete herunterladen und aktualisieren

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-3776ab.svg" alt="Language">
  <img src="https://img.shields.io/badge/Dependencies-3%20real%20sub--updaters-2ea44f.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/Tests-13-00E5FF.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-functional-4caf50.svg" alt="Maturity">
</p>

---

**Ehrlichkeitspruefung - was heute laeuft:** **Reifegrad: funktional.** Dies ist ein duenner Dispatcher, keine fuenfte Implementierung der Oekosystem-Erkennung: er enthaelt keine eigene Manifest-Analyse-, Installations- oder Aktualisierungslogik. `dispatch()` und sein Befehlsaufbau (19 Tests, alle gegen einen simulierten Subprozess-Runner) sind real und getestet; `status --ecosystem all` wurde echt gegen ein reales Checkout aller drei Oekosysteme ausgefuehrt (55 HYDRA-UMC-, 7 URTC- und 17 A.R.M.O.R.-Repositories korrekt gefunden) - `install` wurde ebenfalls echt ausgefuehrt, aus einer sauberen Umgebung, und ARMOR-COMMON wurde vom ARMOR-Updater geklont, gebaut, getestet und uebernommen (unsignierte Revisionen werden mit einer Warnung installiert); `update` wurde noch nicht echt ausgefuehrt. Ein echter Fehler wurde bei diesem ersten echten Lauf gefunden und behoben: siehe den `--workspace`-Eintrag in `CHANGELOG.md`. Der EH3D-Updater wurde anhand seiner eigenen Tests (317, gegen ein falsches GitHub) hinzugefügt und wurde über diesen Dispatcher noch nicht gegen einen echten Checkout ausgeführt.

---

## 📋 Auf einen Blick

| | |
|---|---|
| Version | `0.1.0` |
| Reifegrad | Funktionsfähig |
| Technik | Python 3.10+ / hydra-umc-updater / urtc-updater / armor-updater / eh3d-updater |
| Ziel | Der PC der Person, die es benutzt |
| Auf echter Hardware | Nicht zutreffend: nichts hiervon läuft auf Hardware |

## 🎯 Ueberblick

* **Ein Werkzeug, vier echte Ökosysteme:** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER), [URTC](https://github.com/JuanenRac/URTC-UPDATER), [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) und [EH3D](https://github.com/JuanenRac/EH3D-UPDATER) haben jeweils bereits einen eigenen, unabhängig getesteten Updater. Dieses Projekt implementiert nichts davon neu - es installiert alle vier als echte Abhängigkeiten und leitet `--ecosystem hydra-umc|urtc|armor|eh3d` an den passenden weiter.
* **Festgelegte, geprüfte Abhängigkeiten:** `pyproject.toml` legt jeden Sub-Updater auf einen geprüften Commit fest, nie auf ein wanderndes `main`, sodass eine Installation immer genau das Geprüfte erhält. `versions` zeigt die installierte Version jedes einzelnen und meldet, wenn einer hinter GitHub zurückliegt.
* **Jedes Mal ein echter, eigener Subprozess.** Jeder Aufruf startet `python -m <Modul dieses Ökosystems> --cli ...` in einem eigenen Interpreter - importiert nie das `main()` einer anderen CLI in diesen Prozess. Vier unabhängige argparse-Programme, die `sys.argv` lesen und `sys.exit()` aufrufen dürfen, würden sich im selben Prozess gegenseitig stören.
* **`status --ecosystem all`:** führt die Statusprüfung der vier Ökosysteme gleichzeitig aus, gibt jeden Bericht vollständig in fester Reihenfolge aus und nennt, welche fehlgeschlagen sind, ohne beim ersten Fehler anzuhalten.
* **`install`/`update` brauchen immer ein Ökosystem und einen Projektnamen.** Ein "alles in allen Ökosystemen aktualisieren" gibt es hier nicht - dieselbe Haltung wie die CLI jedes Sub-Updaters.
* **Geerbte Grenzen:** dieses Werkzeug führt aus, was jeder Sub-Updater tut. Der A.R.M.O.R.-Updater beschädigt seine eigene Installation noch, wenn er sich selbst aktualisiert (die editierbare Installation zeigt auf sein Staging-Verzeichnis); ARMOR-UPDATER daher vorerst von Hand aktualisieren. URTC-UPDATER kann signierte Commits verlangen (`URTC_UPDATER_REQUIRE_SIGNED=1`); die anderen beiden prüfen noch keine Signaturen.

## 📂 Repository-Struktur

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py   # Der einzige Ort, der die vier echten Oekosysteme und ihr CLI-Modul benennt
│   ├── main.py         # argparse-CLI + dispatch() - baut den richtigen Subprozess-Befehl auf und fuehrt ihn aus
│   ├── i18n.py         # Die Texte des Fensters in den acht Sprachen
│   ├── qt_gui.py       # Qt-Quick-Fenster (eine Karte je Oekosystem, ein Protokoll) - oeffnet den Updater des jeweiligen Oekosystems
│   └── qml/Main.qml    # Das QML des Fensters
├── tests/               # 19 Tests gegen einen simulierten Subprozess-Runner
├── tools/               # ci_validate.py, build_test.py, _doc_policy.py, _readme_parity.py
├── build.sh / build.bat         # venv + editierbare Installation (holt die 3 echten Abhaengigkeiten) + Kompilierungspruefung
├── build-test.sh / build-test.bat  # gleiche Installation, dann die echte pytest-Suite
└── run.sh / run.bat              # CLI-Einstiegspunkt (ohne Argumente: das Fenster)
```

## 🛠️ Entwicklungsumgebung

```bash
pip install -e ".[dev]"                 # installiert auch hydra-umc-updater, urtc-updater, armor-updater und eh3d-updater von GitHub
python -m pytest tests -q               # 19 Tests, ohne Netzwerk oder echten Subprozess
electro-hobby-3d-updater status --ecosystem all               # prueft alle Oekosysteme (parallel)
electro-hobby-3d-updater versions                             # installierte Version jedes Updaters und ob er hinter GitHub liegt
electro-hobby-3d-updater status --ecosystem armor             # prueft nur eines
electro-hobby-3d-updater install --ecosystem urtc URTC-TESTER # klont und baut ein noch nicht installiertes Projekt
electro-hobby-3d-updater update  --ecosystem hydra-umc HYDRA-UMC-SERVER # aktualisiert und baut ein bereits installiertes Projekt neu
```

## 🔗 Verwandte Projekte

Dieses Werkzeug ist das fuenfte Stueck von JuanenRacs (Electro Hobby 3D) eigener Updater-Familie - es umhuellt die anderen vier, statt eines von ihnen zu ersetzen:

* **[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)** - erkennt, installiert und aktualisiert die eigenen Repositories des HYDRA-UMC-Oekosystems
* **[URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)** - erkennt, installiert und aktualisiert die eigenen Repositories des URTC-Oekosystems
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - erkennt, installiert und aktualisiert die eigenen Repositories des A.R.M.O.R.-Oekosystems
* **[EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER)** - erkennt, installiert und aktualisiert die eigenen Repositories des EH3D-Oekosystems
* **ELECTRO-HOBBY-3D-UPDATER** (dieses Repository) - leitet an das vom Nutzer gewaehlte der vier weiter

Und die vier echten Oekosysteme selbst: **[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)** (industrielle Multi-Roboter-Steuerung), **[URTC](https://github.com/JuanenRac/URTC)** (die Universal-Robot-Tool-Controller-Plattform), **[A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-COMMON)** (Perimeter-Sicherheit und Hausautomation), **[EH3D](https://github.com/JuanenRac/EH3D)** (die Fertigungs-Suite: CAM, CNC und Maschinensteuerung).

## 📚 Dokumentation und Community

* **[Aenderungsprotokoll dieses Repositories](CHANGELOG.md)**
* Fragen, Ideen und Meldungen: electrohobby3d@gmail.com

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LIZENZ

GPL-3.0-or-later - siehe [LICENSE](LICENSE).
