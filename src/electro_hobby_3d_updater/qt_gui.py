# =============================================================================
# ELECTRO-HOBBY-3D-UPDATER - Qt Quick window over the dispatcher: qt_gui.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The visual window of this tool, in the same family as the HYDRA-UMC, URTC and A.R.M.O.R. updaters.

It is still only a dispatcher: it shows the three ecosystems, opens the window of the updater each one has, and asks each updater's own command line for its status (the same
`python -m <module> --cli status` that main.py runs). Nothing here discovers, installs or updates anything by itself.

PySide6 is imported only when the window is opened; the command line keeps needing nothing but the standard library.
"""
from __future__ import annotations

import subprocess
import sys
import threading
from importlib.util import find_spec
from pathlib import Path

from PySide6.QtCore import Property, QObject, QUrl, Signal, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

from . import __version__
from .ecosystems import ECOSYSTEMS, ECOSYSTEMS_BY_KEY
from .i18n import LANGUAGES, text

ACCENTS = {"hydra-umc": "#ff8a3d", "urtc": "#43db9b", "armor": "#38d4e6"}


def installed(module: str) -> bool:
    """Is the updater's package importable in this Python? (checked without importing it)"""
    try:
        return find_spec(module.split(".")[0]) is not None
    except (ImportError, ValueError):
        return False


class Bridge(QObject):
    languageChanged = Signal()
    logChanged = Signal()
    busyChanged = Signal()
    workspaceChanged = Signal()

    def __init__(self, workspace: Path) -> None:
        super().__init__()
        self._language = "en"
        self._log: list[str] = []
        self._busy = False
        self._workspace = str(workspace)

    # ---- what the window shows ----
    @Property(str, notify=languageChanged)
    def language(self) -> str:
        return self._language

    @Property(str, constant=True)
    def version(self) -> str:
        return __version__

    @Property("QVariantList", constant=True)
    def languages(self) -> list:
        return [{"code": code, "name": name} for code, name in LANGUAGES]

    @Property("QVariantList", constant=True)
    def ecosystems(self) -> list:
        return [{"key": item.key, "name": item.display_name, "manifest": item.manifest_file, "accent": ACCENTS.get(item.key, "#38d4e6"), "available": installed(item.module)} for item in ECOSYSTEMS]

    @Property(str, notify=logChanged)
    def log(self) -> str:
        return "\n".join(self._log[-400:])

    @Property(bool, notify=busyChanged)
    def busy(self) -> bool:
        return self._busy

    @Property(str, notify=workspaceChanged)
    def workspace(self) -> str:
        return self._workspace

    @Slot(str, str, result=str)
    def tr(self, language: str, key: str) -> str:   # noqa: D102 - the window passes the language so its labels refresh when it changes
        return text(language, key)

    @Slot(str)
    def setLanguage(self, code: str) -> None:
        if code in {item[0] for item in LANGUAGES} and code != self._language:
            self._language = code
            self.languageChanged.emit()

    @Slot(str)
    def setWorkspace(self, path: str) -> None:
        cleaned = QUrl(path).toLocalFile() if path.startswith("file:") else path
        if cleaned and Path(cleaned).is_dir():
            self._workspace = cleaned
            self.workspaceChanged.emit()

    @Slot()
    def clearLog(self) -> None:
        self._log.clear()
        self.logChanged.emit()

    # ---- what it does: only ever run the ecosystem's own updater ----
    @Slot(str)
    def openUpdater(self, key: str) -> None:
        ecosystem = ECOSYSTEMS_BY_KEY.get(key)
        if ecosystem is None:
            return
        if not installed(ecosystem.module):
            self._add(f"{ecosystem.display_name}: {text(self._language, 'missing')}")
            return
        # a separate process with its own window: this one stays usable and the two never share a Qt application
        subprocess.Popen([sys.executable, "-m", ecosystem.module], close_fds=True)   # noqa: S603  (its window remembers its own folder)
        self._add(f"{ecosystem.display_name}: {text(self._language, 'open')}")

    @Slot(str, bool)
    def check(self, key: str, offline: bool) -> None:
        if self._busy:
            return
        keys = [item.key for item in ECOSYSTEMS] if key == "all" else [key]
        threading.Thread(target=self._check, args=(keys, offline), daemon=True).start()

    def _check(self, keys: list[str], offline: bool) -> None:
        self._set_busy(True)
        try:
            for key in keys:
                ecosystem = ECOSYSTEMS_BY_KEY[key]
                self._add(f"=== {ecosystem.display_name} ===")
                if not installed(ecosystem.module):
                    self._add(text(self._language, "missing"))
                    continue
                command = [sys.executable, "-m", ecosystem.module, "--cli", "status", *(["--offline"] if offline else []), "--workspace", self._workspace]
                try:
                    done = subprocess.run(command, capture_output=True, text=True, timeout=300, check=False)   # noqa: S603
                except (OSError, subprocess.TimeoutExpired) as error:
                    self._add(f"{text(self._language, 'failed')}: {error}")
                    continue
                for line in (done.stdout + done.stderr).splitlines():
                    self._add(line)
                self._add(text(self._language, "done") if done.returncode == 0 else f"{text(self._language, 'failed')} ({done.returncode})")
        finally:
            self._set_busy(False)

    def _add(self, line: str) -> None:
        self._log.append(line)
        self.logChanged.emit()

    def _set_busy(self, value: bool) -> None:
        self._busy = value
        self.busyChanged.emit()


def launch_qt_gui(workspace: Path) -> int:
    QQuickStyle.setStyle("Basic")   # the window paints its own buttons; the native style refuses to be customised
    app = QGuiApplication.instance() or QGuiApplication(sys.argv)
    app.setApplicationName("ELECTRO-HOBBY-3D-UPDATER")
    app.setApplicationDisplayName("Electro Hobby 3D Updater")
    engine = QQmlApplicationEngine()
    bridge = Bridge(workspace)
    engine.rootContext().setContextProperty("backend", bridge)
    engine.load(QUrl.fromLocalFile(str(Path(__file__).with_name("qml") / "Main.qml")))
    if not engine.rootObjects():
        return 1
    return app.exec()
