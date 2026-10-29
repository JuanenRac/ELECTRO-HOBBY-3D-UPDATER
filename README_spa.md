<p align="center">
  <img src="images/ELECTRO_HOBBY_3D_BANNER.svg" alt="ELECTRO-HOBBY-3D-UPDATER banner" width="100%">
</p>

# 🧩 ELECTRO-HOBBY-3D-UPDATER

<p align="center"><a href="README.md">🇺🇸 English</a> | 🇪🇸 <b>Español</b> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Una línea de comandos y una ventana para los cuatro ecosistemas de Electro Hobby 3D: elige un sistema, descarga y actualiza sus paquetes con el actualizador que ese sistema ya tiene

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Python%203.10%2B-3776AB.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.1.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-4CAF50.svg" alt="Maturity">
</p>

---

**Comprobación de honestidad - lo que se ejecuta hoy:** esto es un despachador delgado, no una quinta implementación del descubrimiento de ecosistemas: no tiene lógica propia de análisis de manifiestos, instalación ni actualización. Cada uno de los cuatro ecosistemas tiene su propio actualizador, que encuentra sus proyectos por el manifiesto `<ecosistema>.project.json` de cada repositorio; esta herramienta instala los cuatro como dependencias fijadas y ejecuta el que eliges como un proceso aparte (`status` para los cuatro a la vez). El despacho y los comandos que construye están probados (pasan 18 pruebas, con un ejecutor de procesos simulado). `status --ecosystem all` se ha ejecutado de verdad contra una copia real de tres de los ecosistemas e `install` una vez desde un entorno limpio (un proyecto clonado, construido, probado y promovido por el actualizador de A.R.M.O.R.); `update` no se ha ejecutado de verdad, y el traspaso al actualizador de EH3D se añadió a partir de las pruebas de ese actualizador y no se ha ejecutado a través de esta herramienta contra una copia real.

---

> **Estado de seguridad (safety) y de seguridad informática:** reemplaza ficheros en tu máquina a través de los actualizadores que ejecuta, así que solo hace lo que hace cada uno de ellos, un proyecto cada vez y tras la confirmación que ese actualizador pide. No ejecuta nada por sí solo, nunca actualiza "todo a través de los ecosistemas" y no controla ninguna máquina. Cada actualizador está fijado a un commit revisado, nunca a una rama que se mueve; las revisiones sin firmar se instalan con un aviso salvo que ese actualizador esté configurado para exigir firmas.

## 📋 De un vistazo

| | |
|---|---|
| Versión | `0.1.1` |
| Madurez | Funcional |
| Pruebas | 18 |
| Pila tecnológica | Python 3.10+ (PySide6 for the window) |
| En hardware real | No aplica: se ejecuta en el PC de la persona que lo usa |

**Ir a:** [Resumen](#-resumen) · [Arquitectura](#-arquitectura) · [Inicio rápido](#-inicio-rápido) · [Pruebas](#-pruebas) · [Estructura](#-estructura-del-repositorio) · [Relacionados](#-proyectos-relacionados)

## 🚦 Estado del proyecto

Cada línea es una parte de este repositorio y la luz dice hasta dónde llega hoy. Se escribe con lo que el repositorio puede demostrar (pruebas, compilaciones, ejecuciones), no con lo previsto.

🟢 Hecho y verificado · 🟡 Funciona, con límites conocidos · 🟠 Hecho a medias o sin verificar · 🔴 Sin hacer o sin funcionar

| Área | Estado | Qué significa aquí |
|---|---|---|
| Software | 🟡 | Un despachador delgado: no tiene lógica propia de descubrimiento, instalación ni actualización y pasa `--ecosystem hydra-umc\|urtc\|armor\|eh3d` al actualizador de cada ecosistema, que instala como dependencias fijadas. |
| Pruebas | 🟢 | Pasan 18 pruebas (`pytest`) con un ejecutor de procesos simulado; otra se omite cuando PySide6 no está instalado. |
| Uso real | 🟠 | `status` se ha ejecutado contra una copia real de tres de los ecosistemas e `install` una vez desde un entorno limpio; `update` no se ha ejecutado de verdad. |
| Ventana | 🟡 | La ventana (una tarjeta por ecosistema, un registro, ocho idiomas) abre el actualizador propio de cada ecosistema; sus textos y sus reglas de hilos están probados, el resto solo a mano. |
| Integración | 🟠 | El traspaso al actualizador de EH3D se añadió a partir de las pruebas de ese actualizador y no se ha ejecutado a través de este despachador contra una copia real. |
| Seguridad | 🟡 | Cada sub-actualizador está fijado a un commit revisado, nunca a una rama que se mueve; cada ejecución es su propio proceso con límite de tiempo; las revisiones sin firmar se instalan con un aviso y no ha habido revisión independiente. |
| Hardware real | 🟢 | No aplica: se ejecuta en el PC de la persona que lo usa. |
| Documentación | 🟢 | README en ocho idiomas, comprobado contra el manifiesto y el registro de cambios en cada cambio. |

## 🎯 Resumen

* **Una herramienta, cuatro ecosistemas:** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER), [URTC](https://github.com/JuanenRac/URTC-UPDATER), [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) y [EH3D](https://github.com/JuanenRac/EH3D-UPDATER) tienen cada uno su propio actualizador, probado por separado. Este proyecto no reimplementa nada de eso: instala los cuatro como dependencias y pasa `--ecosystem hydra-umc|urtc|armor|eh3d` al que corresponde.
* **El descubrimiento sigue en cada actualizador:** cada ecosistema encuentra sus proyectos por el manifiesto de cada repositorio (`hydra-umc.project.json`, `urtc.project.json`, `armor.project.json`, `eh3d.project.json`), así que un repositorio nuevo aparece en su ecosistema por tener un manifiesto y nada en esta herramienta enumera los proyectos. El manifiesto de esta herramienta, `electro-hobby-3d.project.json`, no pertenece a ninguno de los cuatro por diseño.
* **Dependencias fijadas y revisadas:** `pyproject.toml` fija cada actualizador a un commit revisado, nunca a un `main` que se mueve. `versions` muestra la versión instalada de cada uno y marca los que van por detrás de GitHub.
* **Un proceso aparte cada vez:** cada llamada ejecuta `python -m <módulo de ese ecosistema> --cli ...` como su propio intérprete; cuatro programas argparse que pueden llamar a `sys.exit()` se estropearían entre sí si se compusieran en un solo proceso.
* **`status --ecosystem all`:** ejecuta las cuatro comprobaciones de estado a la vez, imprime cada informe entero en un orden fijo y dice cuáles fallaron sin detenerse en la primera.
* **`install` y `update` siempre necesitan un ecosistema y un nombre de proyecto:** no hay «actualizar todo en todos los ecosistemas», la misma postura de cada actualizador.
* **Una ventana:** sin argumentos, una ventana Qt Quick muestra una tarjeta por ecosistema y un registro, abre el actualizador propio de cada ecosistema y le pide su estado, en ocho idiomas.

## 🧩 Papel en Electro Hobby 3D

ELECTRO-HOBBY-3D-UPDATER es la quinta pieza de la familia de actualizadores de Electro Hobby 3D y está por encima de los cuatro ecosistemas: envuelve a los otros cuatro en lugar de sustituir a ninguno. Es el único sitio donde quien trabaja con más de un ecosistema puede verlos todos y elegir el que actualizar.

## 🏛️ Arquitectura

<p align="center">
  <img src="images/architecture.svg" alt="Arquitectura de ELECTRO-HOBBY-3D-UPDATER: quién lo usa, qué contiene y de qué depende" width="100%">
</p>

Cómo encajan las partes de este repositorio: quién lo usa, qué contiene y de qué depende. La imagen se dibuja desde `docs/architecture.json` y se comprueba contra el código.

## 🔒 Seguridad y protección

| Amenaza | Defensa |
|---|---|
| Un `main` de un actualizador que se mueve o está comprometido y llega a esta herramienta | cada actualizador está fijado en `pyproject.toml` a un commit revisado, nunca a una rama; para pasar a uno más nuevo se revisa antes y se cambia aquí la fijación |
| Un actualizador que estropea a otro | cada llamada ejecuta el actualizador como su propio proceso de intérprete (`python -m <módulo> --cli ...`), nunca importado en este, así que ninguno puede cambiar los argumentos, el estado ni la salida de otro |
| Un actualizador que se cuelga (una petición de credenciales de git, una red caída) | un límite de tiempo en cada ejecución: 900 s para `status` y 1800 s para `install` y `update`, cambiable con `--timeout-seconds` (0 significa sin límite) |
| Un cambio masivo no deseado | `install` y `update` reciben exactamente un ecosistema y un nombre de proyecto y rechazan `--ecosystem all`; cada actualizador pide su propia confirmación |
| Mirar la carpeta equivocada | el espacio de trabajo se reenvía siempre de forma explícita (por defecto la carpeta superior de esta herramienta), porque un actualizador instalado buscaría si no bajo el entorno virtual de esta herramienta y no encontraría nada en silencio |
| Un commit de origen desconocido | queda en manos de cada actualizador: las revisiones sin firmar se instalan con un aviso salvo que a ese actualizador se le diga que exija firmas (EH3D-UPDATER y URTC-UPDATER tienen esa opción) |
| El fallo de un ecosistema que oculta a los otros | `status --ecosystem all` ejecuta los cuatro, imprime cada informe y nombra los que fallaron |

**Lo que no se defiende:** esta herramienta ejecuta lo que haga cada actualizador, con tus derechos, incluido el script de compilación del proyecto que instalas; el actualizador de A.R.M.O.R. todavía estropea su propia instalación cuando se actualiza a sí mismo, así que actualiza ARMOR-UPDATER a mano; y la herramienta no ha tenido revisión independiente. Informa de una vulnerabilidad en privado (véase [SECURITY.md](SECURITY.md)).

## 🔌 Interfaces

| Interfaz | Qué es | Dónde |
|---|---|---|
| Línea de comandos | `electro-hobby-3d-updater` con `status`, `install`, `update` y `versions`; `--version`; códigos de salida 0, 1 (una ejecución falló o agotó el tiempo) y 2 (`versions`: un actualizador va por detrás de GitHub) | `main.py` |
| Ventana | sin argumentos abre una ventana Qt Quick (una tarjeta por ecosistema y un registro); necesita el extra opcional `PySide6` | `qt_gui.py`, `qml/Main.qml` |
| Hacia cada actualizador | un proceso aparte: `python -m <hydra_umc_updater.main, urtc_updater.main, armor_updater.main o eh3d_updater.main> --cli <acción> [proyecto] --workspace <carpeta>` | `ecosystems.py` |
| GitHub | `versions` lee el `pyproject.toml` del repositorio de cada actualizador en `main` para comparar versiones; nada más | `main.py` |

## ⚙️ Configuración

No hay que configurar nada; las opciones de la línea de comandos son toda la configuración, y todo lo demás pertenece a cada actualizador.

| Opción | Por defecto | Rango | Qué hace |
|---|---|---|---|
| `--ecosystem` | ninguno | `hydra-umc`, `urtc`, `armor` o `eh3d`; `all` solo para `status` | qué actualizador hace el trabajo |
| `--workspace` | la carpeta superior de esta herramienta | una carpeta | el espacio de trabajo que escanea cada actualizador (siempre se reenvía) |
| `--offline` (`status`, `versions`) | desactivado | activado o desactivado | omitir la comprobación de GitHub |
| `--timeout-seconds` | 900 para `status`, 1800 para `install` y `update` | un número de segundos; 0 o menos significa sin límite | detener un actualizador que no ha terminado |
| las fijaciones | cuatro commits en `pyproject.toml` | un commit revisado de cada actualizador | qué código de actualizador se instala; solo cambia tras revisar uno más nuevo |

Las fijaciones de esta versión son HYDRA-UMC-UPDATER 0.4.8, URTC-UPDATER 0.1.7, ARMOR-UPDATER 0.1.4 y EH3D-UPDATER 0.0.1.

## 🚀 Inicio rápido

Necesitas Python 3.10 o posterior; la ventana necesita además PySide6.

```bash
build.bat                                   # ./build.sh on Linux: a venv and an editable install (pulls the four pinned updaters)
pip install -e ".[dev]"                     # the same by hand; add ".[gui]" for the window
python -m pytest tests -q
electro-hobby-3d-updater status --ecosystem all
electro-hobby-3d-updater versions
electro-hobby-3d-updater install --ecosystem urtc URTC-TESTER
electro-hobby-3d-updater update  --ecosystem hydra-umc HYDRA-UMC-SERVER
```

`run.bat` / `run.sh` sin argumentos abren la ventana. `install` y `update` necesitan un ecosistema y un nombre de proyecto, escrito como lo declara el manifiesto de ese ecosistema.

## 🧪 Pruebas

La suite tiene 18 pruebas que pasan (`pytest tests`), y otra que se omite cuando PySide6 no está instalado. Se ejecutan contra un ejecutor de procesos simulado, sin red ni subprocesos reales, y cubren: que el registro tiene exactamente los cuatro ecosistemas; que `status` ejecuta el módulo correcto y reenvía `--offline`; que `status --ecosystem all` ejecuta cada ecosistema una vez, los imprime en orden, los ejecuta a la vez y nunca se detiene en el primer fallo; que `install` y `update` necesitan un ecosistema y un proyecto y rechazan `all`; que un actualizador que falla pasa su propio código de salida; que el espacio de trabajo es por defecto la carpeta superior; que `versions` informa de las versiones instaladas, señala un actualizador que va por detrás y nunca contacta con GitHub con `--offline`; que un actualizador que se cuelga se detiene con un mensaje claro y un tiempo límite de cero significa sin límite; y que los textos de la ventana existen en los ocho idiomas. El CI ejecuta `python tools/ci_validate.py` (manifiesto, versión, registro de cambios y paridad de los README) y luego `python tools/build_test.py`, que compila cada fuente y ejecuta la suite.

## 🏗️ Compilación y publicación

La versión vive en `pyproject.toml`, en `electro-hobby-3d.project.json` y en el paquete, y cada versión tiene su entrada en [CHANGELOG.md](CHANGELOG.md). `build.sh` / `build.bat` crean un entorno virtual, instalan esta herramienta con sus cuatro actualizadores fijados y la comprueban; `build-test.sh` / `build-test.bat` hacen lo mismo y luego ejecutan la suite; `test.sh` / `test.bat` ejecutan solo las pruebas, cada uno con un panel en vivo, y ninguno cambia la versión. Las versiones se publican en GitHub (la última es la 0.1.1); la herramienta se instala desde este repositorio y no está en PyPI.

## 🩺 Resolución de problemas

| Síntoma | Qué hacer |
|---|---|
| Un ecosistema informa de que no hay proyectos | El actualizador busca en el espacio de trabajo carpetas hermanas con su manifiesto; pasa `--workspace` con la carpeta que contiene los repositorios. |
| `versions` dice que un actualizador va POR DETRÁS (código de salida 2) | Las fijaciones son deliberadas: revisa el commit más nuevo de ese actualizador, ponlo en `pyproject.toml`, sube la versión de esta herramienta y reinstala. |
| La ventana no se abre | Necesita PySide6: `pip install -e ".[gui]"`; la línea de comandos funciona sin él. |
| Un actualizador tardó demasiado | Se detuvo al llegar al límite (900 s para `status`, 1800 s para `install` y `update`); súbelo con `--timeout-seconds`, o 0 para no tener límite. |
| ARMOR-UPDATER se estropea tras actualizarse a sí mismo | Su instalación editable apunta a su carpeta de preparación: actualiza ARMOR-UPDATER a mano y ejecuta de nuevo `build.bat` / `build.sh`. |

## 📂 Estructura del repositorio

<p align="center">
  <img src="images/repository-structure.svg" alt="Estructura del repositorio ELECTRO-HOBBY-3D-UPDATER" width="100%">
</p>

<details>
<summary>Versión en texto del árbol</summary>

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py                            el único sitio que nombra los cuatro ecosistemas
│   ├── main.py                                  la línea de comandos, el despacho y las versiones
│   ├── qt_gui.py qml/                           la ventana Qt Quick y su QML
│   ├── i18n.py                                  las palabras de la ventana en ocho idiomas
│   └── assets/                                  el icono del programa
├── tests/                                       el despacho contra un ejecutor de procesos simulado
├── docs/                                        los datos de las imágenes de Arquitectura y Estructura
├── tools/                                       CI, construcción, README e imágenes
├── images/                                      banner y las imágenes de Arquitectura y Estructura del repositorio
├── .github/                                     flujos de CI y de publicación, plantillas de issues y pull requests
├── build.sh build.bat                           venv, instalación editable y comprobación con un panel en vivo
├── build-test.sh build-test.bat                 lo mismo, y luego la suite real
├── run.sh run.bat                               abre la ventana, o la línea de comandos con argumentos
├── bump*.py                                     los scripts que suben la versión
├── electro-hobby-3d.project.json                el manifiesto: versión, papel y madurez
├── pyproject.toml                               el paquete y los cuatro actualizadores fijados
├── CHANGELOG.md                                 qué cambió en cada versión
├── SECURITY.md SUPPORT.md                       cómo informar de una vulnerabilidad y dónde preguntar
└── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   cómo contribuir, el código de conducta y la licencia
```

</details>

## 🗺️ Hoja de ruta y límites conocidos

**Límites conocidos hoy**

* `update` no se ha ejecutado de verdad, e `install` solo una vez; `status` se ha ejecutado contra una copia real de tres ecosistemas.
* El traspaso a EH3D-UPDATER no se ha ejecutado a través de esta herramienta contra una copia real.
* No hay «actualizar todo en todos los ecosistemas», por diseño.
* Que un commit deba estar firmado queda a cargo de cada actualizador, y el actualizador de A.R.M.O.R. estropea su propia instalación cuando se actualiza a sí mismo.
* La herramienta no ha tenido revisión independiente y no está en PyPI.

**Siguiente**

* Ejecutar `status`, `install` y `update` de los proyectos EH3D a través de esta herramienta en una copia real.
* Mover las fijaciones a commits revisados más nuevos de los cuatro actualizadores según vayan publicando.
* Ejecutar `update` de verdad en un ecosistema y anotar lo que salga.

## 🌍 Idiomas

El README y los textos existen en inglés, español, francés, italiano, alemán, chino, japonés y portugués de Portugal.

## 🔗 Proyectos relacionados

Esta herramienta es la quinta pieza de la familia de actualizadores de JuanenRac (Electro Hobby 3D); envuelve a los otros cuatro en lugar de sustituir a ninguno:

* [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER): detecta, instala y actualiza los repositorios de HYDRA-UMC
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER): detecta, instala y actualiza los repositorios de URTC
* [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER): detecta, instala y actualiza los repositorios de A.R.M.O.R.
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER): detecta, instala y actualiza los repositorios de EH3D
* [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC), [URTC](https://github.com/JuanenRac/URTC), [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-COMMON) y [EH3D](https://github.com/JuanenRac/EH3D-DOCS): los cuatro ecosistemas en sí

## 📚 Documentación

* [Registro de cambios](CHANGELOG.md): cada versión, qué cambió y qué se encontró.
* [Contribuir](CONTRIBUTING.md), [Política de seguridad](SECURITY.md) y [Soporte](SUPPORT.md).
* La documentación del actualizador de cada ecosistema vive en su repositorio (véase Proyectos relacionados).

## 🤝 Contribuir y comunidad

* Antes de una pull request ejecuta `python -m pytest tests -q` y `python tools/ci_validate.py`: ambos deben pasar. Consulta [CONTRIBUTING.md](CONTRIBUTING.md) y el [código de conducta](CODE_OF_CONDUCT.md).
* El README existe en ocho idiomas: un cambio en el texto se hace en los ocho archivos, y las dos imágenes se dibujan a partir de `docs/architecture.json` y `docs/structure.json` con `tools/make_architecture.py` y `tools/make_structure.py`.
* Esta herramienta debe seguir siendo un despachador: la lógica que descubre, instala o actualiza pertenece al actualizador del ecosistema, no a esta, y un ecosistema nuevo es un cambio de una línea en `ecosystems.py`.
* Informa de una vulnerabilidad en privado: [SECURITY.md](SECURITY.md). Preguntas, ideas e informes: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCIA

Software: GPL-3.0-or-later. Véase [LICENSE](LICENSE). Los diseños de hardware de la suite usan CERN OHL-S.
