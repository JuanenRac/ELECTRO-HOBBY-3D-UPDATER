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
  <a href="README_jpn.md">🇯🇵 日本語</a>
</p>

### Un'unica riga di comando per tutti e tre gli ecosistemi Electro Hobby 3D - scegli un sistema, scarica e aggiorna i suoi pacchetti

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-3776ab.svg" alt="Language">
  <img src="https://img.shields.io/badge/Dependencies-3%20real%20sub--updaters-2ea44f.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/Tests-10-00E5FF.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-ff9800.svg" alt="Maturity">
</p>

---

**Controllo di onesta - cosa funziona oggi:** **Maturita: impalcatura.** E' un dispatcher sottile, non una quarta implementazione della scoperta dell'ecosistema: non ha logica propria di analisi del manifesto, installazione o aggiornamento. `dispatch()` e la costruzione dei suoi comandi (10 test, tutti contro un esecutore di sottoprocessi simulato) sono reali e testati; `status --ecosystem all` e stato eseguito davvero contro un checkout reale dei tre ecosistemi (trovati correttamente 55 repository HYDRA-UMC, 7 URTC e 15 A.R.M.O.R.) - `install`/`update` non ancora. Un vero bug e stato trovato e corretto durante quella prima esecuzione reale: vedi la voce `--workspace` in `CHANGELOG.md`.

---

## 🎯 Panoramica

* **Uno strumento, tre ecosistemi reali:** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER), [URTC](https://github.com/JuanenRac/URTC-UPDATER) e [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) hanno gia ciascuno il proprio updater dedicato e testato separatamente. Questo progetto non reimplementa nulla di tutto cio - installa tutti e tre come vere dipendenze (direttamente dai loro repository GitHub) e smista `--ecosystem hydra-umc|urtc|armor` verso quello giusto.
* **Un vero sottoprocesso separato ogni volta.** Ogni chiamata esegue `python -m <modulo di quell'ecosistema> --cli ...` come proprio processo interprete - non importa mai il `main()` di un'altra CLI in questo stesso processo. Tre programmi argparse indipendenti, ognuno libero di leggere `sys.argv` e chiamare `sys.exit()`, si corromperebbero a vicenda se composti nello stesso processo; un sottoprocesso offre lo stesso isolamento di una persona che digita ogni comando a mano.
* **`status --ecosystem all`:** l'unica cosa che questo strumento fa che nessun singolo updater fa da solo - esegue il controllo di stato dei tre ecosistemi in sequenza e riporta quale/i sono falliti, senza fermarsi al primo.
* **`install`/`update` richiedono sempre un ecosistema e un nome di progetto.** Qui non esiste un "aggiorna tutto in tutti gli ecosistemi", la stessa posizione non negoziabile che la CLI di ogni updater gia adotta per i propri progetti.

## 📂 Struttura del Repository

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py   # L'unico posto che nomina i tre ecosistemi reali e il loro modulo CLI
│   └── main.py         # CLI argparse + dispatch() - costruisce ed esegue il comando di sottoprocesso corretto
├── tests/               # 10 test contro un esecutore di sottoprocessi simulato
├── tools/               # ci_validate.py, build_test.py, _doc_policy.py, _readme_parity.py
├── build.sh / build.bat         # venv + installazione editabile (scarica le 3 dipendenze reali) + controllo di compilazione
├── build-test.sh / build-test.bat  # stessa installazione, poi la vera suite pytest
└── run.sh / run.bat              # punto di ingresso della CLI
```

## 🛠️ Ambiente di Sviluppo

```bash
pip install -e ".[dev]"                 # installa anche hydra-umc-updater, urtc-updater e armor-updater da GitHub
python -m pytest tests -q               # 10 test, senza rete ne sottoprocessi reali
electro-hobby-3d-updater status --ecosystem all               # controlla i tre ecosistemi in sequenza
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
