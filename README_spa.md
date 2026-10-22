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
  <a href="README_jpn.md">🇯🇵 日本語</a> |
  <a href="README_por.md">🇵🇹 Português</a>
</p>

### Una sola linea de comandos para los cuatro ecosistemas de Electro Hobby 3D - elige un sistema, descarga y actualiza sus paquetes

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-3776ab.svg" alt="Language">
  <img src="https://img.shields.io/badge/Dependencies-3%20real%20sub--updaters-2ea44f.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/Tests-13-00E5FF.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-functional-4caf50.svg" alt="Maturity">
</p>

---

**Comprobacion de honestidad - que funciona hoy:** **Madurez: funcional.** Es un despachador delgado, no una quinta implementacion del descubrimiento de ecosistemas: no tiene logica propia de lectura de manifiestos, instalacion o actualizacion. `dispatch()` y la construccion de sus comandos (19 pruebas, todas contra un ejecutor de subproceso simulado) estan probados de verdad; `status --ecosystem all` se ha ejecutado de verdad contra un checkout real de los tres ecosistemas (encontro correctamente 55 repositorios de HYDRA-UMC, 7 de URTC y 17 de A.R.M.O.R.) - `install` tambien se ha ejecutado de verdad, desde un entorno limpio, y ARMOR-COMMON se clono, construyo, probo y promovio con el actualizador de ARMOR (las revisiones sin firmar se instalan con un aviso); `update` todavia no se ha ejecutado de verdad. Se encontro y corrigio un bug real durante esa primera ejecucion real: ver la entrada de `--workspace` en `CHANGELOG.md`. El actualizador de EH3D se añadió a partir de sus propios tests (317, contra un GitHub falso) y todavía no se ha ejecutado a través de este despachador contra una copia real.

---

## 📋 De un vistazo

| | |
|---|---|
| Versión | `0.1.1` |
| Madurez | Funcional |
| Tecnología | Python 3.10+ / hydra-umc-updater / urtc-updater / armor-updater / eh3d-updater |
| Destino | El PC de quien lo usa |
| En hardware real | No aplica: nada de esto se ejecuta en hardware |

## 🎯 Vision general

* **Una herramienta, cuatro ecosistemas reales:** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER), [URTC](https://github.com/JuanenRac/URTC-UPDATER), [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) y [EH3D](https://github.com/JuanenRac/EH3D-UPDATER) ya tienen cada uno su propio actualizador, probado por separado. Este proyecto no reimplementa nada de eso: instala los cuatro como dependencias reales y envía `--ecosystem hydra-umc|urtc|armor|eh3d` al que corresponde.
* **Dependencias fijadas y revisadas:** `pyproject.toml` fija cada sub-actualizador a un commit revisado, nunca a un `main` que se mueve, así que una instalación siempre obtiene exactamente lo revisado. `versions` muestra la versión instalada de cada uno y avisa si alguno va por detrás de GitHub.
* **Un subproceso real y separado cada vez.** Cada llamada ejecuta `python -m <módulo de ese ecosistema> --cli ...` en su propio intérprete; nunca importa el `main()` de otra CLI en este. Cuatro programas argparse independientes, cada uno libre de leer `sys.argv` y llamar a `sys.exit()`, se corromperían entre sí en el mismo proceso.
* **`status --ecosystem all`:** ejecuta a la vez la comprobación de estado de los cuatro ecosistemas, imprime cada informe completo en un orden fijo e indica cuál o cuáles fallaron sin detenerse en el primero.
* **`install`/`update` exigen siempre un ecosistema y un nombre de proyecto.** Aquí no existe "actualizar todo en todos los ecosistemas", la misma postura que ya mantiene la CLI de cada sub-actualizador.
* **Límites heredados:** esta herramienta ejecuta lo que haga cada sub-actualizador. El actualizador de A.R.M.O.R. todavía rompe su propia instalación al actualizarse a sí mismo (la instalación editable apunta a su directorio de staging), así que por ahora actualiza ARMOR-UPDATER a mano. URTC-UPDATER puede exigir commits firmados (`URTC_UPDATER_REQUIRE_SIGNED=1`); los otros dos aún no verifican firmas.

## 📂 Estructura del Repositorio

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py   # El unico lugar que nombra los cuatro ecosistemas reales y su modulo CLI
│   ├── main.py         # CLI de argparse + dispatch() - construye y ejecuta el comando de subproceso correcto
│   ├── i18n.py         # Los textos de la ventana en los ocho idiomas
│   ├── qt_gui.py       # Ventana Qt Quick (una tarjeta por ecosistema, un registro) - abre el actualizador de cada ecosistema
│   └── qml/Main.qml    # El QML de la ventana
├── tests/               # 19 pruebas contra un ejecutor de subproceso simulado
├── tools/               # ci_validate.py, build_test.py, _doc_policy.py, _readme_parity.py
├── build.sh / build.bat         # venv + instalacion editable (trae las 3 dependencias reales) + comprobacion de compilacion
├── build-test.sh / build-test.bat  # misma instalacion, luego la suite real de pytest
└── run.sh / run.bat              # punto de entrada de la CLI (sin argumentos: la ventana)
```

## 🛠️ Entorno de Desarrollo

```bash
pip install -e ".[dev]"                 # tambien instala hydra-umc-updater, urtc-updater, armor-updater y eh3d-updater desde GitHub
python -m pytest tests -q               # 19 pruebas, sin red ni subproceso real
electro-hobby-3d-updater status --ecosystem all               # comprueba todos los ecosistemas (en paralelo)
electro-hobby-3d-updater versions                             # versión instalada de cada actualizador y si va por detrás de GitHub
electro-hobby-3d-updater status --ecosystem armor             # comprueba solo uno
electro-hobby-3d-updater install --ecosystem urtc URTC-TESTER # clona y construye un proyecto que aun no esta instalado
electro-hobby-3d-updater update  --ecosystem hydra-umc HYDRA-UMC-SERVER # actualiza y reconstruye un proyecto ya instalado
```

## 🔗 Proyectos Relacionados

Esta herramienta es la quinta pieza de la propia familia de actualizadores de JuanenRac (Electro Hobby 3D) - envuelve a las otras cuatro en vez de reemplazar ninguna:

* **[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)** - detecta, instala y actualiza los propios repositorios del ecosistema HYDRA-UMC
* **[URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)** - detecta, instala y actualiza los propios repositorios del ecosistema URTC
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - detecta, instala y actualiza los propios repositorios del ecosistema A.R.M.O.R.
* **[EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER)** - detecta, instala y actualiza los propios repositorios del ecosistema EH3D
* **ELECTRO-HOBBY-3D-UPDATER** (este repositorio) - despacha al que el usuario elija de los cuatro

Y los cuatro ecosistemas reales en si: **[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)** (control industrial multi-robot), **[URTC](https://github.com/JuanenRac/URTC)** (la plataforma Universal Robot Tool Controller), **[A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-COMMON)** (seguridad perimetral y domotica), **[EH3D](https://github.com/JuanenRac/EH3D)** (la suite de fabricacion: CAM, CNC y control de maquinas).

## 📚 Documentacion y Comunidad

* **[Historial de cambios de este repositorio](CHANGELOG.md)**
* Preguntas, ideas e informes: electrohobby3d@gmail.com

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCIA

GPL-3.0-or-later - ver [LICENSE](LICENSE).
