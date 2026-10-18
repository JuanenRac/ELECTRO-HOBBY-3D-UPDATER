<p align="center">
  <img src="images/ELECTRO_HOBBY_3D_BANNER.svg" alt="ELECTRO-HOBBY-3D-UPDATER banner" width="100%">
</p>

# 🧩 ELECTRO-HOBBY-3D-UPDATER

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <b>🇮🇹 Italiano</b> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a> |
  <a href="README_por.md">🇵🇹 Português</a>
</p>

### Un'unica riga di comando per tutti e tre gli ecosistemi Electro Hobby 3D - scegli un sistema, scarica e aggiorna i suoi pacchetti

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-3776ab.svg" alt="Language">
  <img src="https://img.shields.io/badge/Dependencies-3%20real%20sub--updaters-2ea44f.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/Tests-13-00E5FF.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-functional-4caf50.svg" alt="Maturity">
</p>

---

**Controllo di onesta - cosa funziona oggi:** **Maturita: funzionale.** E' un dispatcher sottile, non una quarta implementazione della scoperta dell'ecosistema: non ha logica propria di analisi del manifesto, installazione o aggiornamento. `dispatch()` e la costruzione dei suoi comandi (19 test, tutti contro un esecutore di sottoprocessi simulato) sono reali e testati; `status --ecosystem all` e stato eseguito davvero contro un checkout reale dei tre ecosistemi (trovati correttamente 55 repository HYDRA-UMC, 7 URTC e 17 A.R.M.O.R.) - Anche `install` e stato eseguito davvero, da un ambiente pulito, e ARMOR-COMMON e stato clonato, compilato, testato e promosso dall'aggiornatore ARMOR (le revisioni non firmate vengono installate con un avviso); `update` non e ancora stato eseguito davvero. Un vero bug e stato trovato e corretto durante quella prima esecuzione reale: vedi la voce `--workspace` in `CHANGELOG.md`.

---

## 📋 In breve

| | |
|---|---|
| Versione | `0.0.9` |
| Maturità | Funzionale |
| Tecnologia | Python 3.10+ / hydra-umc-updater / urtc-updater / armor-updater |
| Destinazione | Il PC di chi lo usa |
| Su hardware reale | Non applicabile: nulla qui gira su hardware |

## 🎯 Panoramica

* **Uno strumento, tre ecosistemi reali:** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER), [URTC](https://github.com/JuanenRac/URTC-UPDATER) e [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) hanno già ciascuno il proprio updater, testato separatamente. Questo progetto non reimplementa nulla di tutto ciò: installa i tre come dipendenze reali e inoltra `--ecosystem hydra-umc|urtc|armor` a quello corrispondente.
* **Dipendenze fissate e verificate:** `pyproject.toml` fissa ogni sotto-updater a un commit verificato, mai a un `main` che si muove, così un'installazione ottiene sempre esattamente ciò che è stato verificato. `versions` mostra la versione installata di ciascuno e segnala quello rimasto indietro rispetto a GitHub.
* **Ogni volta un vero sottoprocesso separato.** Ogni chiamata esegue `python -m <modulo di quell'ecosistema> --cli ...` nel proprio interprete - non importa mai il `main()` di un'altra CLI in questo. Tre programmi argparse indipendenti, ciascuno libero di leggere `sys.argv` e chiamare `sys.exit()`, si corromperebbero a vicenda nello stesso processo.
* **`status --ecosystem all`:** esegue contemporaneamente il controllo di stato dei tre ecosistemi, stampa ogni rapporto per intero in un ordine fisso e indica quale o quali sono falliti senza fermarsi al primo.
* **`install`/`update` richiedono sempre un ecosistema e un nome di progetto.** Qui non esiste "aggiorna tutto in tutti gli ecosistemi", la stessa posizione della CLI di ogni sotto-updater.
* **Limiti ereditati:** questo strumento esegue ciò che fa ogni sotto-updater. L'updater di A.R.M.O.R. rompe ancora la propria installazione quando aggiorna se stesso (l'installazione modificabile punta alla sua directory di staging), quindi per ora aggiorna ARMOR-UPDATER a mano. URTC-UPDATER può richiedere commit firmati (`URTC_UPDATER_REQUIRE_SIGNED=1`); gli altri due non verificano ancora le firme.

## 📂 Struttura del Repository

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py   # L'unico posto che nomina i tre ecosistemi reali e il loro modulo CLI
│   ├── main.py         # CLI argparse + dispatch() - costruisce ed esegue il comando di sottoprocesso corretto
│   ├── i18n.py         # I testi della finestra nelle otto lingue
│   ├── qt_gui.py       # Finestra Qt Quick (una scheda per ecosistema, un registro) - apre l'aggiornatore di ogni ecosistema
│   └── qml/Main.qml    # Il QML della finestra
├── tests/               # 19 test contro un esecutore di sottoprocessi simulato
├── tools/               # ci_validate.py, build_test.py, _doc_policy.py, _readme_parity.py
├── build.sh / build.bat         # venv + installazione editabile (scarica le 3 dipendenze reali) + controllo di compilazione
├── build-test.sh / build-test.bat  # stessa installazione, poi la vera suite pytest
└── run.sh / run.bat              # punto di ingresso della CLI (senza argomenti: la finestra)
```

## 🛠️ Ambiente di Sviluppo

```bash
pip install -e ".[dev]"                 # installa anche hydra-umc-updater, urtc-updater e armor-updater da GitHub
python -m pytest tests -q               # 19 test, senza rete ne sottoprocessi reali
electro-hobby-3d-updater status --ecosystem all               # controlla tutti gli ecosistemi (in parallelo)
electro-hobby-3d-updater versions                             # versione installata di ogni updater e se e indietro rispetto a GitHub
electro-hobby-3d-updater status --ecosystem armor             # controlla solo uno
electro-hobby-3d-updater install --ecosystem urtc URTC-TESTER # clona e costruisce un progetto non ancora installato
electro-hobby-3d-updater update  --ecosystem hydra-umc HYDRA-UMC-SERVER # aggiorna e ricostruisce un progetto gia installato
```

## 🔗 Progetti Correlati

Questo strumento e il quarto pezzo della famiglia di updater di JuanenRac (Electro Hobby 3D) - avvolge gli altri tre invece di sostituirne uno:

* **[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)** - rileva, installa e aggiorna i repository dell'ecosistema HYDRA-UMC
* **[URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)** - rileva, installa e aggiorna i repository dell'ecosistema URTC
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - rileva, installa e aggiorna i repository dell'ecosistema A.R.M.O.R.
* **ELECTRO-HOBBY-3D-UPDATER** (questo repository) - smista verso quello dei tre scelto dall'utente

E i tre ecosistemi reali stessi: **[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)** (controllo industriale multi-robot), **[URTC](https://github.com/JuanenRac/URTC)** (la piattaforma Universal Robot Tool Controller), **[A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-COMMON)** (sicurezza perimetrale e domotica).

## 📚 Documentazione e Comunita

* **[Changelog di questo repository](CHANGELOG.md)**
* Domande, idee e segnalazioni: electrohobby3d@gmail.com

## 👤 AUTORE

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENZA

GPL-3.0-or-later - vedi [LICENSE](LICENSE).
