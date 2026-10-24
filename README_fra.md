<p align="center">
  <img src="images/ELECTRO_HOBBY_3D_BANNER.svg" alt="ELECTRO-HOBBY-3D-UPDATER banner" width="100%">
</p>

# 🧩 ELECTRO-HOBBY-3D-UPDATER

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <b>🇫🇷 Français</b> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a> |
  <a href="README_por.md">🇵🇹 Português</a>
</p>

### Une seule ligne de commande pour les quatre ecosystemes Electro Hobby 3D - choisissez un systeme, telechargez et mettez a jour ses paquets

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-3776ab.svg" alt="Language">
  <img src="https://img.shields.io/badge/Dependencies-3%20real%20sub--updaters-2ea44f.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/Tests-13-00E5FF.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-functional-4caf50.svg" alt="Maturity">
</p>

---

**Verification d'honnetete - ce qui fonctionne aujourd'hui:** **Maturite : fonctionnel.** C'est un dispatcheur mince, pas une cinquieme implementation de la decouverte d'ecosysteme : il ne contient aucune logique propre d'analyse de manifeste, d'installation ou de mise a jour. `dispatch()` et la construction de ses commandes (19 tests, tous contre un executeur de sous-processus simule) sont reels et testes ; `status --ecosystem all` a ete execute pour de vrai contre un checkout reel des trois ecosystemes (55 depots HYDRA-UMC, 7 URTC et 17 A.R.M.O.R. correctement trouves) - `install` a aussi ete execute pour de vrai, depuis un environnement propre, et ARMOR-COMMON a ete clone, construit, teste et promu par l'actualisateur ARMOR (les revisions non signees sont installees avec un avertissement) ; `update` n'a pas encore ete execute pour de vrai. Un vrai bug a ete trouve et corrige lors de cette premiere execution reelle : voir l'entree `--workspace` dans `CHANGELOG.md`. L'outil de mise à jour d'EH3D a été ajouté à partir de ses propres tests (317, contre un faux GitHub) et n'a pas encore été exécuté via ce dispatcheur sur une vraie copie.

---

## 📋 En un coup d'œil

| | |
|---|---|
| Version | `0.1.1` |
| Maturité | Fonctionnel |
| Technologie | Python 3.10+ / hydra-umc-updater / urtc-updater / eh3d-updater / armor-updater |
| Cible | Le PC de la personne qui l'utilise |
| Sur matériel réel | Sans objet : rien ici ne s'exécute sur du matériel |

## 🚦 État du projet

Chaque ligne est une partie de ce dépôt et le feu dit où elle en est aujourd'hui. Elle est écrite d'après ce que le dépôt peut montrer (tests, compilations, exécutions), pas d'après ce qui est prévu.

🟢 Fait et vérifié · 🟡 Fonctionne, avec des limites connues · 🟠 À moitié fait ou pas encore vérifié · 🔴 Pas fait ou ne fonctionne pas

| Domaine | État | Ce que cela veut dire ici |
|---|---|---|
| Logiciel | 🟡 | Un répartiteur mince : il n'a pas de logique propre de découverte, d'installation ni de mise à jour et passe `--ecosystem hydra-umc\|urtc\|armor\|eh3d` à l'outil de mise à jour de chaque écosystème, qu'il installe comme dépendances épinglées. |
| Tests | 🟢 | 19 tests couvrent la délégation et les commandes qu'il construit, tous contre un lanceur de sous-processus simulé. |
| Usage réel | 🟠 | `status` a tourné sur une vraie copie des trois écosystèmes les plus anciens, et `install` a tourné une fois depuis un environnement propre ; `update` n'a pas été exécuté pour de vrai. |
| Intégration | 🟠 | La délégation à l'outil de mise à jour d'EH3D a été ajoutée d'après les tests de cet outil et n'a pas été exécutée via ce répartiteur sur une vraie copie. |
| Sécurité | 🟡 | Chaque sous-outil de mise à jour est épinglé sur un commit relu, jamais sur une branche mouvante ; les révisions non signées sont installées avec un avertissement, et il n'y a pas eu de revue indépendante. |
| Matériel réel | 🟢 | Sans objet : il tourne sur le PC de la personne qui l'utilise. |
| Documentation | 🟢 | README en huit langues, vérifié par rapport au manifeste et au journal des modifications à chaque changement. |

## 🎯 Apercu

* **Un outil, quatre écosystèmes réels :** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER), [URTC](https://github.com/JuanenRac/URTC-UPDATER), [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) et [EH3D](https://github.com/JuanenRac/EH3D-UPDATER) ont chacun déjà leur propre outil de mise à jour, testé séparément. Ce projet ne réimplémente rien de cela : il installe les quatre comme vraies dépendances et transmet `--ecosystem hydra-umc|urtc|armor|eh3d` à celui qui correspond.
* **Dépendances épinglées et relues :** `pyproject.toml` épingle chaque sous-outil sur un commit relu, jamais sur un `main` mouvant, donc une installation obtient toujours exactement ce qui a été relu. `versions` affiche la version installée de chacun et signale celui qui est en retard sur GitHub.
* **Un vrai sous-processus séparé à chaque fois.** Chaque appel lance `python -m <module de cet écosystème> --cli ...` dans son propre interpréteur - il n'importe jamais le `main()` d'une autre CLI dans celui-ci. Quatre programmes argparse indépendants, chacun libre de lire `sys.argv` et d'appeler `sys.exit()`, se corrompraient dans un même processus.
* **`status --ecosystem all` :** lance en même temps la vérification d'état des quatre écosystèmes, affiche chaque rapport en entier dans un ordre fixe et indique lequel ou lesquels ont échoué sans s'arrêter au premier.
* **`install`/`update` exigent toujours un écosystème et un nom de projet.** Il n'y a pas de « tout mettre à jour dans tous les écosystèmes » ici, la même position que la CLI de chaque sous-outil.
* **Limites héritées :** cet outil exécute ce que fait chaque sous-outil. L'outil de mise à jour d'A.R.M.O.R. casse encore sa propre installation quand il se met à jour lui-même (l'installation éditable pointe vers son répertoire de staging) ; mettez donc à jour ARMOR-UPDATER à la main pour l'instant. URTC-UPDATER peut exiger des commits signés (`URTC_UPDATER_REQUIRE_SIGNED=1`) ; les deux autres ne vérifient pas encore les signatures.

## 📂 Structure du Depot

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py   # Le seul endroit qui nomme les quatre ecosystemes reels et leur module CLI
│   ├── main.py         # CLI argparse + dispatch() - construit et execute la bonne commande de sous-processus
│   ├── i18n.py         # Les textes de la fenetre dans les huit langues
│   ├── qt_gui.py       # Fenetre Qt Quick (une carte par ecosysteme, un journal) - ouvre l'outil de chaque ecosysteme
│   └── qml/Main.qml    # Le QML de la fenetre
├── tests/               # 19 tests contre un executeur de sous-processus simule
├── tools/               # ci_validate.py, build_test.py, _doc_policy.py, _readme_parity.py
├── build.sh / build.bat         # venv + installation editable (recupere les 3 vraies dependances) + verification de compilation
├── build-test.sh / build-test.bat  # meme installation, puis la vraie suite pytest
└── run.sh / run.bat              # point d'entree de la CLI (sans argument : la fenetre)
```

## 🛠️ Environnement de Developpement

```bash
pip install -e ".[dev]"                 # installe aussi hydra-umc-updater, urtc-updater, armor-updater et eh3d-updater depuis GitHub
python -m pytest tests -q               # 19 tests, sans reseau ni vrai sous-processus
electro-hobby-3d-updater status --ecosystem all               # verifie tous les ecosystemes (en parallele)
electro-hobby-3d-updater versions                             # version installee de chaque outil et s'il est en retard sur GitHub
electro-hobby-3d-updater status --ecosystem armor             # verifie un seul
electro-hobby-3d-updater install --ecosystem urtc URTC-TESTER # clone et construit un projet pas encore installe
electro-hobby-3d-updater update  --ecosystem hydra-umc HYDRA-UMC-SERVER # met a jour et reconstruit un projet deja installe
```

## 🔗 Projets Lies

Cet outil est la cinquieme piece de la propre famille d'updaters de JuanenRac (Electro Hobby 3D) - il enveloppe les quatre autres au lieu d'en remplacer un :

* **[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)** - detecte, installe et met a jour les propres depots de l'ecosysteme HYDRA-UMC
* **[URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)** - detecte, installe et met a jour les propres depots de l'ecosysteme URTC
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - detecte, installe et met a jour les propres depots de l'ecosysteme A.R.M.O.R.
* **[EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER)** - detecte, installe et met a jour les propres depots de l'ecosysteme EH3D
* **ELECTRO-HOBBY-3D-UPDATER** (ce depot) - redirige vers celui des quatre que l'utilisateur choisit

Et les quatre ecosystemes reels eux-memes : **[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)** (controle industriel multi-robots), **[URTC](https://github.com/JuanenRac/URTC)** (la plateforme Universal Robot Tool Controller), **[A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-COMMON)** (securite perimetrique et domotique), **[EH3D](https://github.com/JuanenRac/EH3D)** (la suite de fabrication : FAO, CNC et commande de machines).

## 📚 Documentation et Communaute

* **[Historique des modifications de ce depot](CHANGELOG.md)**
* Questions, idees et rapports: electrohobby3d@gmail.com

## 👤 AUTEUR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCE

GPL-3.0-or-later - voir [LICENSE](LICENSE).
