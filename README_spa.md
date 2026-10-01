<p align="center">
  <img src="images/ELECTRO_HOBBY_3D_BANNER.svg" alt="ELECTRO-HOBBY-3D-UPDATER banner" width="100%">
</p>

# 🧩 ELECTRO-HOBBY-3D-UPDATER

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <b>🇪🇸 Español</b> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a>
</p>

### Una sola linea de comandos para los tres ecosistemas de Electro Hobby 3D - elige un sistema, descarga y actualiza sus paquetes

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-3776ab.svg" alt="Language">
  <img src="https://img.shields.io/badge/Dependencies-3%20real%20sub--updaters-2ea44f.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/Tests-10-00E5FF.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-ff9800.svg" alt="Maturity">
</p>

---

**Comprobacion de honestidad - que funciona hoy:** **Madurez: andamiaje.** Es un despachador delgado, no una cuarta implementacion del descubrimiento de ecosistemas: no tiene logica propia de lectura de manifiestos, instalacion o actualizacion. `dispatch()` y la construccion de sus comandos (10 pruebas, todas contra un ejecutor de subproceso simulado) estan probados de verdad; `status --ecosystem all` se ha ejecutado de verdad contra un checkout real de los tres ecosistemas (encontro correctamente 55 repositorios de HYDRA-UMC, 7 de URTC y 15 de A.R.M.O.R.) - `install`/`update` todavia no. Se encontro y corrigio un bug real durante esa primera ejecucion real: ver la entrada de `--workspace` en `CHANGELOG.md`.

---

## 🎯 Vision general

* **Una herramienta, tres ecosistemas reales:** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER), [URTC](https://github.com/JuanenRac/URTC-UPDATER) y [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) ya tienen cada uno su propio actualizador dedicado y probado por separado. Este proyecto no reimplementa nada de eso - instala los tres como dependencias reales (directamente desde sus propios repositorios de GitHub) y despacha `--ecosystem hydra-umc|urtc|armor` al que corresponda.
* **Un subproceso real y separado cada vez.** Cada llamada ejecuta `python -m <modulo de ese ecosistema> --cli ...` como su propio proceso interprete - nunca importa el `main()` de otra CLI en este mismo proceso. Tres programas argparse independientes, cada uno libre de leer `sys.argv` y llamar a `sys.exit()`, se corromperian entre si si se combinaran en el mismo proceso; un subproceso da el mismo aislamiento que tendria una persona escribiendo cada comando a mano.
* **`status --ecosystem all`:** lo unico que hace esta herramienta que ningun actualizador por si solo hace - ejecuta la comprobacion de estado de los tres ecosistemas en secuencia e informa cual(es) fallaron, sin detenerse en el primero.
* **`install`/`update` siempre necesitan un ecosistema y un nombre de proyecto.** Aqui no existe un "actualizar todo en todos los ecosistemas", la misma postura no negociable que ya toma la propia CLI de cada actualizador para sus propios proyectos.

## 📂 Estructura del Repositorio

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py   # El unico lugar que nombra los tres ecosistemas reales y su modulo CLI
│   ├── main.py         # CLI de argparse + dispatch() - construye y ejecuta el comando de subproceso correcto
│   ├── i18n.py         # Los textos de la ventana en los siete idiomas
│   ├── qt_gui.py       # Ventana Qt Quick (una tarjeta por ecosistema, un registro) - abre el actualizador de cada ecosistema
│   └── qml/Main.qml    # El QML de la ventana
├── tests/               # 12 pruebas contra un ejecutor de subproceso simulado
├── tools/               # ci_validate.py, build_test.py, _doc_policy.py, _readme_parity.py
├── build.sh / build.bat         # venv + instalacion editable (trae las 3 dependencias reales) + comprobacion de compilacion
├── build-test.sh / build-test.bat  # misma instalacion, luego la suite real de pytest
└── run.sh / run.bat              # punto de entrada de la CLI (sin argumentos: la ventana)
```

## 🛠️ Entorno de Desarrollo

```bash
pip install -e ".[dev]"                 # tambien instala hydra-umc-updater, urtc-updater y armor-updater desde GitHub
python -m pytest tests -q               # 10 pruebas, sin red ni subproceso real
electro-hobby-3d-updater status --ecosystem all               # comprueba los tres ecosistemas en secuencia
electro-hobby-3d-updater status --ecosystem armor             # comprueba solo uno
electro-hobby-3d-updater install --ecosystem urtc URTC-TESTER # clona y construye un proyecto que aun no esta instalado
electro-hobby-3d-updater update  --ecosystem hydra-umc HYDRA-UMC-SERVER # actualiza y reconstruye un proyecto ya instalado
```

## 🔗 Proyectos Relacionados

Esta herramienta es la cuarta pieza de la propia familia de actualizadores de JuanenRac (Electro Hobby 3D) - envuelve a las otras tres en vez de reemplazar ninguna:

* **[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)** - detecta, instala y actualiza los propios repositorios del ecosistema HYDRA-UMC
* **[URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)** - detecta, instala y actualiza los propios repositorios del ecosistema URTC
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - detecta, instala y actualiza los propios repositorios del ecosistema A.R.M.O.R.
* **ELECTRO-HOBBY-3D-UPDATER** (este repositorio) - despacha al que el usuario elija de los tres

Y los tres ecosistemas reales en si: **[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)** (control industrial multi-robot), **[URTC](https://github.com/JuanenRac/URTC)** (la plataforma Universal Robot Tool Controller), **[A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-COMMON)** (seguridad perimetral y domotica).

## 📚 Documentacion y Comunidad

* **[Historial de cambios de este repositorio](CHANGELOG.md)**
* Preguntas, ideas e informes: electrohobby3d@gmail.com

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCIA

GPL-3.0-or-later - ver [LICENSE](LICENSE).
