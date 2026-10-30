<p align="center">
  <img src="images/ELECTRO_HOBBY_3D_BANNER.svg" alt="ELECTRO-HOBBY-3D-UPDATER banner" width="100%">
</p>

# 🧩 ELECTRO-HOBBY-3D-UPDATER

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | 🇫🇷 <b>Français</b> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Une ligne de commande et une fenêtre pour les quatre écosystèmes d'Electro Hobby 3D : choisir un système, télécharger et mettre à jour ses paquets avec l'outil de mise à jour que ce système possède déjà

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Python%203.10%2B-3776AB.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.1.2-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-4CAF50.svg" alt="Maturity">
</p>

---

**Vérification d'honnêteté - ce qui tourne aujourd'hui :** ceci est un répartiteur mince, pas une cinquième implémentation de la découverte des écosystèmes : il n'a aucune logique propre d'analyse de manifestes, d'installation ou de mise à jour. Chacun des quatre écosystèmes a son propre outil de mise à jour, qui trouve ses projets par le manifeste `<écosystème>.project.json` de chaque dépôt ; cet outil installe les quatre comme dépendances épinglées et lance celui que tu choisis comme un processus séparé (`status` pour les quatre à la fois). Le routage et les commandes qu'il construit sont testés (18 tests réussissent, avec un exécuteur de processus simulé). `status --ecosystem all` a été exécuté pour de vrai sur une vraie copie de trois des écosystèmes et `install` une fois depuis un environnement propre (un projet cloné, construit, testé et promu par l'outil de mise à jour d'A.R.M.O.R.) ; `update` n'a pas été exécuté pour de vrai, et le passage à l'outil de mise à jour d'EH3D a été ajouté à partir des tests de celui-ci et n'a pas été exécuté par cet outil sur une vraie copie.

---

> **État de la sûreté et de la sécurité :** il remplace des fichiers sur ta machine par les outils de mise à jour qu'il lance, donc il ne fait que ce que fait chacun d'eux, un projet à la fois et après la confirmation que cet outil demande. Il ne lance rien tout seul, ne met jamais à jour « tout à travers les écosystèmes » et ne pilote aucune machine. Chaque outil de mise à jour est épinglé sur un commit relu, jamais sur une branche mobile ; les révisions non signées sont installées avec un avertissement, sauf si cet outil est réglé pour exiger des signatures.

## 📋 En un coup d'œil

| | |
|---|---|
| Version | `0.1.2` |
| Maturité | Fonctionnel |
| Technologie | Python 3.10+ / hydra-umc-updater / urtc-updater / eh3d-updater / armor-updater |
| Cible | Le PC de la personne qui l'utilise |
| Sur matériel réel | Sans objet : rien ici ne s'exécute sur du matériel |

**Aller à :** [Présentation](#-présentation) · [Architecture](#-architecture) · [Sécurité et protection](#-sécurité-et-protection) · [Interfaces](#-interfaces) · [Configuration](#-configuration) · [Démarrage rapide](#-démarrage-rapide) · [Tests](#-tests) · [Dépannage](#-dépannage) · [Structure du dépôt](#-structure-du-dépôt) · [Projets liés](#-projets-liés)

## 🚦 État du projet

Chaque ligne est une partie de ce dépôt et le feu dit où elle en est aujourd'hui. Elle est écrite d'après ce que le dépôt peut montrer (tests, compilations, exécutions), pas d'après ce qui est prévu.

🟢 Fait et vérifié · 🟡 Fonctionne, avec des limites connues · 🟠 À moitié fait ou pas encore vérifié · 🔴 Pas fait ou ne fonctionne pas

| Domaine | État | Ce que cela veut dire ici |
|---|---|---|
| Logiciel | 🟡 | Un répartiteur mince : il n'a aucune logique propre de découverte, d'installation ou de mise à jour et passe `--ecosystem hydra-umc\|urtc\|armor\|eh3d` à l'outil de mise à jour de chaque écosystème, qu'il installe comme dépendances épinglées. |
| Tests | 🟢 | 18 tests réussissent (`pytest`) contre un exécuteur de processus simulé ; un autre est ignoré quand PySide6 n'est pas installé. |
| Usage réel | 🟠 | `status` a tourné sur une vraie copie de trois des écosystèmes et `install` une fois depuis un environnement propre ; `update` n'a pas été exécuté pour de vrai. |
| Fenêtre | 🟡 | La fenêtre (une carte par écosystème, un journal, huit langues) ouvre l'outil de mise à jour propre à chaque écosystème ; ses textes et ses règles de threads sont testés, le reste seulement à la main. |
| Intégration | 🟠 | Le passage à l'outil de mise à jour d'EH3D a été ajouté à partir des tests de celui-ci et n'a pas été exécuté par ce répartiteur sur une vraie copie. |
| Sécurité | 🟡 | Chaque sous-outil est épinglé sur un commit relu, jamais sur une branche mobile ; chaque exécution est son propre processus avec une limite de temps ; les révisions non signées sont installées avec un avertissement et il n'y a pas eu de revue indépendante. |
| Matériel réel | 🟢 | Sans objet : il tourne sur le PC de la personne qui l'utilise. |
| Documentation | 🟢 | README en huit langues, vérifié à chaque changement contre le manifeste et le journal des modifications. |

## 🎯 Présentation

* **Un outil, quatre écosystèmes :** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER), [URTC](https://github.com/JuanenRac/URTC-UPDATER), [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) et [EH3D](https://github.com/JuanenRac/EH3D-UPDATER) ont chacun leur propre outil de mise à jour, testé séparément. Ce projet n'en réimplémente rien : il installe les quatre comme dépendances et passe `--ecosystem hydra-umc|urtc|armor|eh3d` à celui qui convient.
* **La découverte reste dans chaque outil :** chaque écosystème trouve ses projets par le manifeste de chaque dépôt (`hydra-umc.project.json`, `urtc.project.json`, `armor.project.json`, `eh3d.project.json`), donc un nouveau dépôt apparaît dans son écosystème en ayant un manifeste et rien dans cet outil ne liste les projets. Le manifeste de cet outil, `electro-hobby-3d.project.json`, n'appartient à aucun des quatre par conception.
* **Dépendances épinglées et relues :** `pyproject.toml` épingle chaque outil sur un commit relu, jamais sur un `main` mobile. `versions` montre la version installée de chacun et signale ceux qui sont en retard sur GitHub.
* **Un processus séparé à chaque fois :** chaque appel lance `python -m <module de cet écosystème> --cli ...` comme son propre interpréteur ; quatre programmes argparse pouvant chacun appeler `sys.exit()` se gêneraient dans un même processus.
* **`status --ecosystem all` :** lance les quatre contrôles d'état en même temps, imprime chaque rapport en entier dans un ordre fixe et dit lesquels ont échoué sans s'arrêter au premier.
* **`install` et `update` exigent toujours un écosystème et un nom de projet :** il n'y a pas de « tout mettre à jour dans tous les écosystèmes », la même position que chaque outil.
* **Une fenêtre :** sans argument, une fenêtre Qt Quick montre une carte par écosystème et un journal, ouvre l'outil de mise à jour propre à chaque écosystème et lui demande son état, en huit langues.

## 🧩 Rôle dans Electro Hobby 3D

ELECTRO-HOBBY-3D-UPDATER est la cinquième pièce de la famille des outils de mise à jour d'Electro Hobby 3D et se place au-dessus des quatre écosystèmes : il enveloppe les quatre autres au lieu d'en remplacer un. C'est le seul endroit où une personne qui travaille avec plus d'un écosystème peut les voir tous et choisir celui à mettre à jour.

## 🏛️ Architecture

<p align="center">
  <img src="images/architecture.svg" alt="Architecture de ELECTRO-HOBBY-3D-UPDATER : qui l'utilise, ce qu'il contient et de quoi il dépend" width="100%">
</p>

Comment les parties de ce dépôt s'articulent : qui l'utilise, ce qu'il contient et de quoi il dépend. L'image est dessinée à partir de `docs/architecture.json` et vérifiée par rapport au code.

## 🔒 Sécurité et protection

| Menace | Défense |
|---|---|
| Un `main` mobile ou compromis d'un outil de mise à jour qui atteint celui-ci | chaque outil est épinglé dans `pyproject.toml` sur un commit relu, jamais sur une branche ; pour passer à un plus récent, on le relit d'abord et on change l'épinglage ici |
| Un outil qui perturbe un autre | chaque appel lance l'outil comme son propre processus d'interpréteur (`python -m <module> --cli ...`), jamais importé dans celui-ci, donc aucun ne peut changer les arguments, l'état ou la sortie d'un autre |
| Un outil qui se bloque (une invite git qui attend un identifiant, un réseau mort) | une limite de temps à chaque exécution : 900 s pour `status` et 1800 s pour `install` et `update`, modifiable avec `--timeout-seconds` (0 veut dire sans limite) |
| Un changement de masse non désiré | `install` et `update` prennent exactement un écosystème et un nom de projet et refusent `--ecosystem all` ; chaque outil demande sa propre confirmation |
| Regarder le mauvais dossier | l'espace de travail est toujours transmis explicitement (par défaut le dossier parent de cet outil), car sinon un outil installé chercherait sous l'environnement virtuel de celui-ci et ne trouverait rien en silence |
| Un commit d'origine inconnue | laissé à chaque outil : les révisions non signées sont installées avec un avertissement sauf si on dit à cet outil d'exiger des signatures (EH3D-UPDATER et URTC-UPDATER ont cette option) |
| L'échec d'un écosystème qui cache les autres | `status --ecosystem all` lance les quatre, imprime chaque rapport et nomme ceux qui ont échoué |

**Ce qui n'est pas défendu :** cet outil exécute ce que fait chaque outil de mise à jour, avec tes droits, y compris le script de construction du projet que tu installes ; l'outil d'A.R.M.O.R. casse encore sa propre installation quand il se met à jour lui-même, mets donc ARMOR-UPDATER à jour à la main ; et l'outil n'a pas eu de revue indépendante. Signale une vulnérabilité en privé (voir [SECURITY.md](SECURITY.md)).

## 🔌 Interfaces

| Interface | Ce que c'est | Où |
|---|---|---|
| Ligne de commande | `electro-hobby-3d-updater` avec `status`, `install`, `update` et `versions` ; `--version` ; codes de sortie 0, 1 (une exécution a échoué ou dépassé le temps) et 2 (`versions` : un outil est en retard sur GitHub) | `main.py` |
| Fenêtre | sans argument, ouvre une fenêtre Qt Quick (une carte par écosystème et un journal) ; demande l'extra facultatif `PySide6` | `qt_gui.py`, `qml/Main.qml` |
| Vers chaque outil | un processus séparé : `python -m <hydra_umc_updater.main, urtc_updater.main, armor_updater.main ou eh3d_updater.main> --cli <action> [projet] --workspace <dossier>` | `ecosystems.py` |
| GitHub | `versions` lit le `pyproject.toml` du dépôt de chaque outil sur `main` pour comparer les versions ; rien d'autre | `main.py` |

## ⚙️ Configuration

Rien n'est à configurer ; les options de la ligne de commande sont toute la configuration, et tout le reste appartient à chaque outil de mise à jour.

| Option | Défaut | Plage | Ce qu'elle fait |
|---|---|---|---|
| `--ecosystem` | aucun | `hydra-umc`, `urtc`, `armor` ou `eh3d` ; `all` seulement pour `status` | quel outil fait le travail |
| `--workspace` | le dossier parent de cet outil | un dossier | l'espace de travail que chaque outil parcourt (toujours transmis) |
| `--offline` (`status`, `versions`) | désactivé | activé ou désactivé | sauter le contrôle de GitHub |
| `--timeout-seconds` | 900 pour `status`, 1800 pour `install` et `update` | un nombre de secondes ; 0 ou moins veut dire sans limite | arrêter un outil qui n'a pas fini |
| les épinglages | quatre commits dans `pyproject.toml` | un commit relu de chaque outil | quel code d'outil est installé ; changé seulement après relecture d'un plus récent |

Les épinglages de cette version sont HYDRA-UMC-UPDATER 0.4.8, URTC-UPDATER 0.1.7, ARMOR-UPDATER 0.1.4 et EH3D-UPDATER 0.0.1.

## 🚀 Démarrage rapide

Il faut Python 3.10 ou plus récent ; la fenêtre demande aussi PySide6.

```bash
build.bat                                   # ./build.sh on Linux: a venv and an editable install (pulls the four pinned updaters)
pip install -e ".[dev]"                     # the same by hand; add ".[gui]" for the window
python -m pytest tests -q
electro-hobby-3d-updater status --ecosystem all
electro-hobby-3d-updater versions
electro-hobby-3d-updater install --ecosystem urtc URTC-TESTER
electro-hobby-3d-updater update  --ecosystem hydra-umc HYDRA-UMC-SERVER
```

`run.bat` / `run.sh` sans argument ouvrent la fenêtre. `install` et `update` demandent un écosystème et un nom de projet, écrit comme le déclare le manifeste de cet écosystème.

## 🧪 Tests

La suite compte 18 tests qui réussissent (`pytest tests`), et un autre qui est ignoré quand PySide6 n'est pas installé. Ils tournent contre un exécuteur de processus simulé, sans réseau ni vrai sous-processus, et couvrent : le registre a exactement les quatre écosystèmes ; `status` lance le bon module et transmet `--offline` ; `status --ecosystem all` lance chaque écosystème une fois, les imprime dans l'ordre, les lance en même temps et ne s'arrête jamais au premier échec ; `install` et `update` exigent un écosystème et un projet et rejettent `all` ; un outil qui échoue transmet son propre code de sortie ; l'espace de travail est par défaut le dossier parent ; `versions` indique les versions installées, signale un outil en retard et ne contacte jamais GitHub avec `--offline` ; un outil qui se bloque est arrêté avec un message clair et un délai de zéro veut dire sans limite ; et les textes de la fenêtre existent dans les huit langues. La CI exécute `python tools/ci_validate.py` (manifeste, version, journal des modifications et parité des README) puis `python tools/build_test.py`, qui compile chaque source et exécute la suite.

## 🏗️ Compilation et publication

La version se trouve dans `pyproject.toml`, dans `electro-hobby-3d.project.json` et dans le paquet, et chaque version a son entrée dans [CHANGELOG.md](CHANGELOG.md). `build.sh` / `build.bat` créent un environnement virtuel, installent cet outil avec ses quatre outils de mise à jour épinglés et le vérifient par compilation ; `build-test.sh` / `build-test.bat` font de même puis exécutent la suite ; `test.sh` / `test.bat` n'exécutent que les tests, chacun dans un panneau en direct, et aucun ne change la version. Les versions sont publiées sur GitHub (la dernière est la 0.1.1) ; l'outil s'installe depuis ce dépôt et n'est pas sur PyPI.

## 🩺 Dépannage

| Symptôme | Que faire |
|---|---|
| Un écosystème ne signale aucun projet | L'outil de mise à jour parcourt l'espace de travail à la recherche de dossiers voisins avec son manifeste ; passe `--workspace` avec le dossier qui contient les dépôts. |
| `versions` dit qu'un outil est EN RETARD (code de sortie 2) | Les épinglages sont voulus : relis le commit plus récent de cet outil, mets-le dans `pyproject.toml`, monte la version de cet outil et réinstalle. |
| La fenêtre ne s'ouvre pas | Elle demande PySide6 : `pip install -e ".[gui]"` ; la ligne de commande marche sans. |
| Un outil a tourné trop longtemps | Il a été arrêté à la limite (900 s pour `status`, 1800 s pour `install` et `update`) ; relève-la avec `--timeout-seconds`, ou 0 pour aucune limite. |
| ARMOR-UPDATER casse après s'être mis à jour lui-même | Son installation éditable pointe vers son dossier de préparation : mets ARMOR-UPDATER à jour à la main et relance `build.bat` / `build.sh`. |

## 📂 Structure du dépôt

<p align="center">
  <img src="images/repository-structure.svg" alt="Structure du dépôt ELECTRO-HOBBY-3D-UPDATER" width="100%">
</p>

<details>
<summary>Version texte de l'arborescence</summary>

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py                            le seul endroit qui nomme les quatre écosystèmes
│   ├── main.py                                  la ligne de commande, le routage et les versions
│   ├── qt_gui.py qml/                           la fenêtre Qt Quick et son QML
│   ├── i18n.py                                  les mots de la fenêtre en huit langues
│   └── assets/                                  l'icône du programme
├── tests/                                       le routage contre un exécuteur de processus simulé
├── docs/                                        les données des images d'Architecture et de Structure
├── tools/                                       CI, construction, README et images
├── images/                                      bannière et images d'Architecture et de Structure du dépôt
├── .github/                                     workflows de CI et de publication, modèles d'issues et de pull requests
├── build.sh build.bat                           venv, installation éditable et contrôle dans un panneau en direct
├── build-test.sh build-test.bat                 pareil, puis la vraie suite de tests
├── run.sh run.bat                               ouvre la fenêtre, ou la ligne de commande avec arguments
├── bump*.py                                     les scripts qui montent la version
├── electro-hobby-3d.project.json                le manifeste : version, rôle et maturité
├── pyproject.toml                               le paquet et les quatre outils épinglés
├── CHANGELOG.md                                 ce qui a changé dans chaque version
├── SECURITY.md SUPPORT.md                       signaler une vulnérabilité et poser des questions
└── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   contribuer, code de conduite et licence
```

</details>

## 🗺️ Feuille de route et limites connues

**Limites connues aujourd'hui**

* `update` n'a pas été exécuté pour de vrai, et `install` une seule fois ; `status` a tourné sur une vraie copie de trois écosystèmes.
* Le passage à EH3D-UPDATER n'a pas été exécuté par cet outil sur une vraie copie.
* Il n'y a pas de « tout mettre à jour dans tous les écosystèmes », par conception.
* Savoir si un commit doit être signé relève de chaque outil, et l'outil d'A.R.M.O.R. casse sa propre installation quand il se met à jour lui-même.
* L'outil n'a pas eu de revue indépendante et n'est pas sur PyPI.

**Ensuite**

* Exécuter `status`, `install` et `update` des projets EH3D par cet outil sur une vraie copie.
* Déplacer les épinglages vers des commits relus plus récents des quatre outils au fil de leurs versions.
* Exécuter `update` pour de vrai sur un écosystème et noter ce qui apparaît.

## 🌍 Langues

Le README et les textes existent en anglais, espagnol, français, italien, allemand, chinois, japonais et portugais européen.

## 🔗 Projets liés

Cet outil est la cinquième pièce de la famille des outils de mise à jour de JuanenRac (Electro Hobby 3D) ; il enveloppe les quatre autres au lieu d'en remplacer un :

* [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) : détecte, installe et met à jour les dépôts de HYDRA-UMC
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) : détecte, installe et met à jour les dépôts d'URTC
* [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) : détecte, installe et met à jour les dépôts d'A.R.M.O.R.
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) : détecte, installe et met à jour les dépôts d'EH3D
* [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC), [URTC](https://github.com/JuanenRac/URTC), [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-COMMON) et [EH3D](https://github.com/JuanenRac/EH3D-DOCS) : les quatre écosystèmes eux-mêmes

## 📚 Documentation

* [Journal des modifications](CHANGELOG.md) : chaque version, ce qui a changé et ce qui a été trouvé.
* [Contribuer](CONTRIBUTING.md), [Politique de sécurité](SECURITY.md) et [Assistance](SUPPORT.md).
* La documentation de l'outil de mise à jour propre à chaque écosystème vit dans son dépôt (voir Projets liés).

## 🤝 Contribuer et communauté

* Avant une pull request, exécute `python -m pytest tests -q` et `python tools/ci_validate.py` : les deux doivent réussir. Voir [CONTRIBUTING.md](CONTRIBUTING.md) et le [code de conduite](CODE_OF_CONDUCT.md).
* Le README existe en huit langues : une modification du texte se fait dans les huit fichiers, et les deux images sont dessinées à partir de `docs/architecture.json` et `docs/structure.json` par `tools/make_architecture.py` et `tools/make_structure.py`.
* Cet outil doit rester un répartiteur : la logique qui découvre, installe ou met à jour appartient à l'outil de l'écosystème, pas à celui-ci, et un nouvel écosystème est un changement d'une ligne dans `ecosystems.py`.
* Signalez une vulnérabilité en privé : [SECURITY.md](SECURITY.md). Questions, idées et rapports : electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTEUR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCE

Logiciel : GPL-3.0-or-later. Voir [LICENSE](LICENSE). Les conceptions matérielles de la suite utilisent la CERN OHL-S.
