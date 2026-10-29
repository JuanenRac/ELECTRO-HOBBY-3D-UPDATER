<p align="center">
  <img src="images/ELECTRO_HOBBY_3D_BANNER.svg" alt="ELECTRO-HOBBY-3D-UPDATER banner" width="100%">
</p>

# 🧩 ELECTRO-HOBBY-3D-UPDATER

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | 🇮🇹 <b>Italiano</b> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Una riga di comando e una finestra per tutti e quattro gli ecosistemi di Electro Hobby 3D: scegli un sistema, scarica e aggiorna i suoi pacchetti con l'aggiornatore che quel sistema ha già

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Python%203.10%2B-3776AB.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.1.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-4CAF50.svg" alt="Maturity">
</p>

---

**Verifica di onestà - cosa funziona oggi:** questo è un dispatcher sottile, non una quinta implementazione del rilevamento degli ecosistemi: non ha logica propria di analisi dei manifesti, installazione o aggiornamento. Ciascuno dei quattro ecosistemi ha il proprio aggiornatore, che trova i suoi progetti tramite il manifesto `<ecosistema>.project.json` di ogni repository; questo strumento installa i quattro come dipendenze fissate ed esegue quello che scegli come processo separato (`status` per tutti e quattro insieme). Il dispatching e i comandi che costruisce sono provati (passano 18 test, con un esecutore di processi finto). `status --ecosystem all` è stato eseguito davvero su una copia reale di tre degli ecosistemi e `install` una volta da un ambiente pulito (un progetto clonato, costruito, provato e promosso dall'aggiornatore di A.R.M.O.R.); `update` non è stato eseguito davvero, e il passaggio all'aggiornatore di EH3D è stato aggiunto dai test di quell'aggiornatore e non è stato eseguito tramite questo strumento su una copia reale.

---

> **Stato di sicurezza funzionale e informatica:** sostituisce file sulla tua macchina tramite gli aggiornatori che esegue, quindi fa solo ciò che fa ciascuno di essi, un progetto alla volta e dopo la conferma che quell'aggiornatore chiede. Non esegue nulla da solo, non aggiorna mai «tutto attraverso gli ecosistemi» e non controlla alcuna macchina. Ogni aggiornatore è fissato a un commit rivisto, mai a un ramo che si muove; le revisioni non firmate vengono installate con un avviso a meno che quell'aggiornatore sia impostato per richiedere le firme.

## 📋 In breve

| | |
|---|---|
| Versione | `0.1.1` |
| Maturità | Funzionale |
| Tecnologia | Python 3.10+ / hydra-umc-updater / urtc-updater / eh3d-updater / armor-updater |
| Destinazione | Il PC di chi lo usa |
| Su hardware reale | Non applicabile: nulla qui gira su hardware |

**Vai a:** [Panoramica](#-panoramica) · [Architettura](#-architettura) · [Sicurezza e protezione](#-sicurezza-e-protezione) · [Interfacce](#-interfacce) · [Configurazione](#-configurazione) · [Avvio rapido](#-avvio-rapido) · [Test](#-test) · [Risoluzione dei problemi](#-risoluzione-dei-problemi) · [Struttura del repository](#-struttura-del-repository) · [Progetti correlati](#-progetti-correlati)

## 🚦 Stato del progetto

Ogni riga è una parte di questo repository e il semaforo dice a che punto è oggi. È scritta in base a ciò che il repository può mostrare (test, compilazioni, esecuzioni), non a ciò che è previsto.

🟢 Fatto e verificato · 🟡 Funziona, con limiti noti · 🟠 Fatto a metà o non ancora verificato · 🔴 Non fatto o non funzionante

| Area | Stato | Cosa significa qui |
|---|---|---|
| Software | 🟡 | Un dispatcher sottile: non ha logica propria di rilevamento, installazione o aggiornamento e passa `--ecosystem hydra-umc\|urtc\|armor\|eh3d` all'aggiornatore di ciascun ecosistema, che installa come dipendenze fissate. |
| Test | 🟢 | Passano 18 test (`pytest`) contro un esecutore di processi finto; un altro viene saltato quando PySide6 non è installato. |
| Uso reale | 🟠 | `status` è stato eseguito su una copia reale di tre degli ecosistemi e `install` una volta da un ambiente pulito; `update` non è stato eseguito davvero. |
| Finestra | 🟡 | La finestra (una scheda per ecosistema, un registro, otto lingue) apre l'aggiornatore proprio di ogni ecosistema; i suoi testi e le sue regole sui thread sono provati, il resto solo a mano. |
| Integrazione | 🟠 | Il passaggio all'aggiornatore di EH3D è stato aggiunto dai test di quell'aggiornatore e non è stato eseguito tramite questo dispatcher su una copia reale. |
| Sicurezza | 🟡 | Ogni sotto-aggiornatore è fissato a un commit rivisto, mai a un ramo che si muove; ogni esecuzione è un processo a sé con un limite di tempo; le revisioni non firmate sono installate con un avviso e non c'è stata una revisione indipendente. |
| Hardware reale | 🟢 | Non applicabile: gira sul PC della persona che lo usa. |
| Documentazione | 🟢 | README in otto lingue, verificato a ogni modifica contro il manifesto e il registro delle modifiche. |

## 🎯 Panoramica

* **Uno strumento, quattro ecosistemi:** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER), [URTC](https://github.com/JuanenRac/URTC-UPDATER), [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) ed [EH3D](https://github.com/JuanenRac/EH3D-UPDATER) hanno ciascuno il proprio aggiornatore, provato separatamente. Questo progetto non reimplementa nulla di ciò: installa tutti e quattro come dipendenze e passa `--ecosystem hydra-umc|urtc|armor|eh3d` a quello corrispondente.
* **Il rilevamento resta in ogni aggiornatore:** ogni ecosistema trova i suoi progetti tramite il manifesto di ogni repository (`hydra-umc.project.json`, `urtc.project.json`, `armor.project.json`, `eh3d.project.json`), quindi un nuovo repository compare nel suo ecosistema avendo un manifesto e nulla in questo strumento elenca i progetti. Il manifesto di questo strumento, `electro-hobby-3d.project.json`, non appartiene a nessuno dei quattro per progetto.
* **Dipendenze fissate e riviste:** `pyproject.toml` fissa ogni aggiornatore a un commit rivisto, mai a un `main` che si muove. `versions` mostra la versione installata di ciascuno e segnala quelli indietro rispetto a GitHub.
* **Un processo separato ogni volta:** ogni chiamata esegue `python -m <modulo di quell'ecosistema> --cli ...` come interprete a sé; quattro programmi argparse che possono chiamare `sys.exit()` si disturberebbero a vicenda in un solo processo.
* **`status --ecosystem all`:** esegue i quattro controlli di stato insieme, stampa ogni rapporto per intero in un ordine fisso e dice quali sono falliti senza fermarsi al primo.
* **`install` e `update` richiedono sempre un ecosistema e un nome di progetto:** non esiste «aggiorna tutto in tutti gli ecosistemi», la stessa posizione di ogni aggiornatore.
* **Una finestra:** senza argomenti, una finestra Qt Quick mostra una scheda per ecosistema e un registro, apre l'aggiornatore proprio di ogni ecosistema e gli chiede il suo stato, in otto lingue.

## 🧩 Ruolo in Electro Hobby 3D

ELECTRO-HOBBY-3D-UPDATER è il quinto pezzo della famiglia di aggiornatori di Electro Hobby 3D e sta sopra i quattro ecosistemi: avvolge gli altri quattro invece di sostituirne uno. È l'unico posto in cui chi lavora con più di un ecosistema può vederli tutti e scegliere quale aggiornare.

## 🏛️ Architettura

<p align="center">
  <img src="images/architecture.svg" alt="Architettura di ELECTRO-HOBBY-3D-UPDATER: chi lo usa, che cosa contiene e da che cosa dipende" width="100%">
</p>

Come si incastrano le parti di questo repository: chi lo usa, che cosa contiene e da che cosa dipende. L'immagine è disegnata da `docs/architecture.json` e verificata rispetto al codice.

## 🔒 Sicurezza e protezione

| Minaccia | Difesa |
|---|---|
| Un `main` mobile o compromesso di un aggiornatore che raggiunge questo strumento | ogni aggiornatore è fissato in `pyproject.toml` a un commit rivisto, mai a un ramo; per passare a uno più nuovo lo si rivede prima e si cambia qui il blocco |
| Un aggiornatore che disturba un altro | ogni chiamata esegue l'aggiornatore come processo di interprete a sé (`python -m <modulo> --cli ...`), mai importato in questo, così nessuno può cambiare argomenti, stato o uscita di un altro |
| Un aggiornatore che si blocca (una richiesta di credenziali di git, una rete morta) | un limite di tempo a ogni esecuzione: 900 s per `status` e 1800 s per `install` e `update`, modificabile con `--timeout-seconds` (0 significa nessun limite) |
| Una modifica di massa indesiderata | `install` e `update` prendono esattamente un ecosistema e un nome di progetto e rifiutano `--ecosystem all`; ogni aggiornatore chiede la propria conferma |
| Guardare la cartella sbagliata | l'area di lavoro viene sempre inoltrata esplicitamente (per impostazione predefinita la cartella madre di questo strumento), perché altrimenti un aggiornatore installato cercherebbe sotto l'ambiente virtuale di questo e non troverebbe nulla in silenzio |
| Un commit di origine ignota | lasciato a ogni aggiornatore: le revisioni non firmate sono installate con un avviso a meno che a quell'aggiornatore si dica di richiedere le firme (EH3D-UPDATER e URTC-UPDATER hanno questa opzione) |
| Il fallimento di un ecosistema che nasconde gli altri | `status --ecosystem all` esegue tutti e quattro, stampa ogni rapporto e nomina quelli falliti |

**Ciò che non è difeso:** questo strumento esegue ciò che fa ogni aggiornatore, con i tuoi diritti, compreso lo script di build del progetto che installi; l'aggiornatore di A.R.M.O.R. rompe ancora la propria installazione quando aggiorna se stesso, quindi aggiorna ARMOR-UPDATER a mano; e lo strumento non ha avuto una revisione indipendente. Segnala una vulnerabilità in privato (vedi [SECURITY.md](SECURITY.md)).

## 🔌 Interfacce

| Interfaccia | Che cos'è | Dove |
|---|---|---|
| Riga di comando | `electro-hobby-3d-updater` con `status`, `install`, `update` e `versions`; `--version`; codici di uscita 0, 1 (un'esecuzione è fallita o ha superato il tempo) e 2 (`versions`: un aggiornatore è indietro rispetto a GitHub) | `main.py` |
| Finestra | senza argomenti apre una finestra Qt Quick (una scheda per ecosistema e un registro); richiede l'extra facoltativo `PySide6` | `qt_gui.py`, `qml/Main.qml` |
| Verso ogni aggiornatore | un processo separato: `python -m <hydra_umc_updater.main, urtc_updater.main, armor_updater.main o eh3d_updater.main> --cli <azione> [progetto] --workspace <cartella>` | `ecosystems.py` |
| GitHub | `versions` legge il `pyproject.toml` del repository di ogni aggiornatore su `main` per confrontare le versioni; nient'altro | `main.py` |

## ⚙️ Configurazione

Non c'è nulla da configurare; le opzioni della riga di comando sono l'intera configurazione, e tutto il resto appartiene a ciascun aggiornatore.

| Opzione | Predefinito | Intervallo | Cosa fa |
|---|---|---|---|
| `--ecosystem` | nessuno | `hydra-umc`, `urtc`, `armor` o `eh3d`; `all` solo per `status` | quale aggiornatore fa il lavoro |
| `--workspace` | la cartella madre di questo strumento | una cartella | l'area di lavoro che ogni aggiornatore scansiona (sempre inoltrata) |
| `--offline` (`status`, `versions`) | disattivato | attivato o disattivato | saltare il controllo di GitHub |
| `--timeout-seconds` | 900 per `status`, 1800 per `install` e `update` | un numero di secondi; 0 o meno significa nessun limite | fermare un aggiornatore che non ha finito |
| i blocchi | quattro commit in `pyproject.toml` | un commit rivisto di ciascun aggiornatore | quale codice di aggiornatore viene installato; cambia solo dopo aver rivisto uno più nuovo |

I blocchi di questa versione sono HYDRA-UMC-UPDATER 0.4.8, URTC-UPDATER 0.1.7, ARMOR-UPDATER 0.1.4 ed EH3D-UPDATER 0.0.1.

## 🚀 Avvio rapido

Serve Python 3.10 o successivo; la finestra richiede anche PySide6.

```bash
build.bat                                   # ./build.sh on Linux: a venv and an editable install (pulls the four pinned updaters)
pip install -e ".[dev]"                     # the same by hand; add ".[gui]" for the window
python -m pytest tests -q
electro-hobby-3d-updater status --ecosystem all
electro-hobby-3d-updater versions
electro-hobby-3d-updater install --ecosystem urtc URTC-TESTER
electro-hobby-3d-updater update  --ecosystem hydra-umc HYDRA-UMC-SERVER
```

`run.bat` / `run.sh` senza argomenti aprono la finestra. `install` e `update` richiedono un ecosistema e un nome di progetto, scritto come lo dichiara il manifesto di quell'ecosistema.

## 🧪 Test

La suite ha 18 test che passano (`pytest tests`), e uno che viene saltato quando PySide6 non è installato. Girano contro un esecutore di processi finto, senza rete né sottoprocessi reali, e coprono: il registro ha esattamente i quattro ecosistemi; `status` esegue il modulo giusto e inoltra `--offline`; `status --ecosystem all` esegue ogni ecosistema una volta, li stampa in ordine, li esegue insieme e non si ferma mai al primo fallimento; `install` e `update` richiedono un ecosistema e un progetto e rifiutano `all`; un aggiornatore che fallisce passa il proprio codice di uscita; l'area di lavoro è per impostazione predefinita la cartella madre; `versions` riporta le versioni installate, segnala un aggiornatore indietro e non contatta mai GitHub con `--offline`; un aggiornatore che si blocca viene fermato con un messaggio chiaro e un limite di tempo pari a zero significa nessun limite; e i testi della finestra esistono in tutte e otto le lingue. La CI esegue `python tools/ci_validate.py` (manifesto, versione, registro delle modifiche e parità dei README) e poi `python tools/build_test.py`, che compila ogni sorgente ed esegue la suite.

## 🏗️ Compilazione e rilascio

La versione sta in `pyproject.toml`, in `electro-hobby-3d.project.json` e nel pacchetto, e ogni versione ha la sua voce in [CHANGELOG.md](CHANGELOG.md). `build.sh` / `build.bat` creano un ambiente virtuale, installano questo strumento con i suoi quattro aggiornatori fissati e lo verificano per compilazione; `build-test.sh` / `build-test.bat` fanno lo stesso e poi eseguono la suite; `test.sh` / `test.bat` eseguono solo i test, ciascuno in un pannello dal vivo, e nessuno cambia la versione. Le versioni vengono pubblicate su GitHub (l'ultima è la 0.1.1); lo strumento si installa da questo repository e non è su PyPI.

## 🩺 Risoluzione dei problemi

| Sintomo | Cosa fare |
|---|---|
| Un ecosistema non riporta progetti | L'aggiornatore cerca nell'area di lavoro cartelle vicine con il suo manifesto; passa `--workspace` con la cartella che contiene i repository. |
| `versions` dice che un aggiornatore è INDIETRO (codice di uscita 2) | I blocchi sono voluti: rivedi il commit più nuovo di quell'aggiornatore, mettilo in `pyproject.toml`, alza la versione di questo strumento e reinstalla. |
| La finestra non si apre | Richiede PySide6: `pip install -e ".[gui]"`; la riga di comando funziona senza. |
| Un aggiornatore è durato troppo | È stato fermato al limite (900 s per `status`, 1800 s per `install` e `update`); alzalo con `--timeout-seconds`, o 0 per nessun limite. |
| ARMOR-UPDATER si rompe dopo essersi aggiornato da solo | La sua installazione modificabile punta alla sua cartella di staging: aggiorna ARMOR-UPDATER a mano ed esegui di nuovo `build.bat` / `build.sh`. |

## 📂 Struttura del repository

<p align="center">
  <img src="images/repository-structure.svg" alt="Struttura del repository ELECTRO-HOBBY-3D-UPDATER" width="100%">
</p>

<details>
<summary>Versione testuale dell'albero</summary>

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py                            l'unico posto che nomina i quattro ecosistemi
│   ├── main.py                                  la riga di comando, il dispatching e le versioni
│   ├── qt_gui.py qml/                           la finestra Qt Quick e il suo QML
│   ├── i18n.py                                  le parole della finestra in otto lingue
│   └── assets/                                  l'icona del programma
├── tests/                                       il dispatching contro un esecutore di processi finto
├── docs/                                        i dati delle immagini di Architettura e Struttura
├── tools/                                       CI, build, README e immagini
├── images/                                      banner e le immagini di Architettura e Struttura del repository
├── .github/                                     workflow di CI e di rilascio, modelli di issue e pull request
├── build.sh build.bat                           venv, installazione modificabile e controllo in un pannello dal vivo
├── build-test.sh build-test.bat                 lo stesso, poi la suite di test reale
├── run.sh run.bat                               apre la finestra, o la riga di comando con argomenti
├── bump*.py                                     gli script che alzano la versione
├── electro-hobby-3d.project.json                il manifesto: versione, ruolo e maturità
├── pyproject.toml                               il pacchetto e i quattro aggiornatori fissati
├── CHANGELOG.md                                 cosa è cambiato in ogni versione
├── SECURITY.md SUPPORT.md                       come segnalare una vulnerabilità e dove chiedere
└── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   come contribuire, codice di condotta e licenza
```

</details>

## 🗺️ Roadmap e limiti noti

**Limiti noti oggi**

* `update` non è stato eseguito davvero, e `install` solo una volta; `status` è stato eseguito su una copia reale di tre ecosistemi.
* Il passaggio a EH3D-UPDATER non è stato eseguito tramite questo strumento su una copia reale.
* Non esiste «aggiorna tutto in tutti gli ecosistemi», per scelta di progetto.
* Se un commit debba essere firmato spetta a ciascun aggiornatore, e l'aggiornatore di A.R.M.O.R. rompe la propria installazione quando aggiorna se stesso.
* Lo strumento non ha avuto una revisione indipendente e non è su PyPI.

**Prossimi passi**

* Eseguire `status`, `install` e `update` dei progetti EH3D tramite questo strumento su una copia reale.
* Spostare i blocchi su commit rivisti più nuovi dei quattro aggiornatori man mano che pubblicano.
* Eseguire `update` davvero su un ecosistema e annotare ciò che emerge.

## 🌍 Lingue

Il README e i testi esistono in inglese, spagnolo, francese, italiano, tedesco, cinese, giapponese e portoghese europeo.

## 🔗 Progetti correlati

Questo strumento è il quinto pezzo della famiglia di aggiornatori di JuanenRac (Electro Hobby 3D); avvolge gli altri quattro invece di sostituirne uno:

* [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER): rileva, installa e aggiorna i repository di HYDRA-UMC
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER): rileva, installa e aggiorna i repository di URTC
* [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER): rileva, installa e aggiorna i repository di A.R.M.O.R.
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER): rileva, installa e aggiorna i repository di EH3D
* [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC), [URTC](https://github.com/JuanenRac/URTC), [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-COMMON) ed [EH3D](https://github.com/JuanenRac/EH3D-DOCS): i quattro ecosistemi stessi

## 📚 Documentazione

* [Registro delle modifiche](CHANGELOG.md): ogni versione, cosa è cambiato e cosa è stato trovato.
* [Contribuire](CONTRIBUTING.md), [Politica di sicurezza](SECURITY.md) e [Supporto](SUPPORT.md).
* La documentazione dell'aggiornatore proprio di ogni ecosistema vive nel suo repository (vedi Progetti correlati).

## 🤝 Contribuire e comunità

* Prima di una pull request esegui `python -m pytest tests -q` e `python tools/ci_validate.py`: entrambi devono passare. Vedi [CONTRIBUTING.md](CONTRIBUTING.md) e il [codice di condotta](CODE_OF_CONDUCT.md).
* Il README esiste in otto lingue: una modifica al testo si fa in tutti e otto i file, e le due immagini sono disegnate da `docs/architecture.json` e `docs/structure.json` con `tools/make_architecture.py` e `tools/make_structure.py`.
* Questo strumento deve restare un dispatcher: la logica che rileva, installa o aggiorna appartiene all'aggiornatore dell'ecosistema, non a questo, e un nuovo ecosistema è una modifica di una riga in `ecosystems.py`.
* Segnala una vulnerabilità in privato: [SECURITY.md](SECURITY.md). Domande, idee e segnalazioni: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTORE

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENZA

Software: GPL-3.0-or-later. Vedi [LICENSE](LICENSE). I progetti hardware della suite usano la CERN OHL-S.
