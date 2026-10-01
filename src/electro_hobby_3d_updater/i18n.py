# =============================================================================
# ELECTRO-HOBBY-3D-UPDATER - Interface texts in the seven languages: i18n.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The words of the window, in English, Spanish, German, French, Italian, Japanese and Chinese.

Every key has all seven; the tests fail when one is missing, so a new text can never ship in only some of the languages.
"""
from __future__ import annotations

LANGUAGES: tuple[tuple[str, str], ...] = (
    ("en", "English"), ("es", "Español"), ("de", "Deutsch"), ("fr", "Français"), ("it", "Italiano"), ("ja", "日本語"), ("zh", "中文"),
)

_ROWS: dict[str, tuple[str, str, str, str, str, str, str]] = {
    "title": ("Electro Hobby 3D Updater", "Actualizador de Electro Hobby 3D", "Electro Hobby 3D Updater", "Mise à jour Electro Hobby 3D", "Aggiornatore Electro Hobby 3D", "Electro Hobby 3D アップデーター", "Electro Hobby 3D 更新器"),
    "subtitle": ("One window for the three ecosystems. Each one is checked, installed and updated by its own updater.", "Una ventana para los tres ecosistemas. Cada uno se comprueba, instala y actualiza con su propio actualizador.", "Ein Fenster für die drei Ökosysteme. Jedes wird von seinem eigenen Updater geprüft, installiert und aktualisiert.", "Une seule fenêtre pour les trois écosystèmes. Chacun est vérifié, installé et mis à jour par son propre outil.", "Una finestra per i tre ecosistemi. Ciascuno viene controllato, installato e aggiornato dal proprio aggiornatore.", "3つのエコシステムを1つの画面で。各エコシステムは専用のアップデーターが確認・インストール・更新します。", "一个窗口管理三个生态系统。各自由其专用更新器检查、安装和更新。"),
    "open": ("Open its updater", "Abrir su actualizador", "Updater öffnen", "Ouvrir son outil", "Apri il suo aggiornatore", "アップデーターを開く", "打开其更新器"),
    "check": ("Check status", "Comprobar estado", "Status prüfen", "Vérifier l'état", "Controlla lo stato", "状態を確認", "检查状态"),
    "check_all": ("Check all three", "Comprobar los tres", "Alle drei prüfen", "Vérifier les trois", "Controlla tutti e tre", "3つすべて確認", "检查全部三个"),
    "offline": ("Without asking GitHub", "Sin consultar GitHub", "Ohne GitHub-Abfrage", "Sans interroger GitHub", "Senza interrogare GitHub", "GitHub に問い合わせない", "不查询 GitHub"),
    "workspace": ("Workspace folder", "Carpeta de trabajo", "Arbeitsordner", "Dossier de travail", "Cartella di lavoro", "作業フォルダー", "工作文件夹"),
    "browse": ("Choose…", "Elegir…", "Wählen…", "Choisir…", "Scegli…", "選択…", "选择…"),
    "log": ("What the updaters answered", "Lo que han respondido los actualizadores", "Antworten der Updater", "Réponses des outils", "Risposte degli aggiornatori", "アップデーターの応答", "更新器的回复"),
    "clear": ("Clear", "Limpiar", "Leeren", "Effacer", "Pulisci", "消去", "清除"),
    "running": ("Working…", "Trabajando…", "Arbeitet…", "En cours…", "In corso…", "処理中…", "处理中…"),
    "done": ("Finished", "Terminado", "Fertig", "Terminé", "Terminato", "完了", "已完成"),
    "failed": ("Failed", "Ha fallado", "Fehlgeschlagen", "Échec", "Non riuscito", "失敗", "失败"),
    "missing": ("This updater is not installed in this Python. Run build once, then try again.", "Este actualizador no está instalado en este Python. Ejecuta build una vez y vuelve a probar.", "Dieser Updater ist in diesem Python nicht installiert. Führen Sie einmal build aus und versuchen Sie es erneut.", "Cet outil n'est pas installé dans ce Python. Lancez build une fois, puis réessayez.", "Questo aggiornatore non è installato in questo Python. Esegui build una volta e riprova.", "このアップデーターはこの Python にインストールされていません。一度 build を実行してから再試行してください。", "此更新器未安装在当前 Python 中。请先运行一次 build 再试。"),
    "language": ("Language", "Idioma", "Sprache", "Langue", "Lingua", "言語", "语言"),
    "about": ("A thin dispatcher: it holds no discovery or installation logic of its own.", "Un simple despachador: no tiene lógica propia de detección ni de instalación.", "Ein dünner Verteiler: keine eigene Erkennungs- oder Installationslogik.", "Un simple répartiteur : aucune logique propre de détection ou d'installation.", "Un semplice smistatore: nessuna logica propria di rilevamento o installazione.", "薄いディスパッチャーです。検出やインストールの独自ロジックは持ちません。", "仅作分发：自身不含检测或安装逻辑。"),
    "tag_hydra-umc": ("Robots, machines and their control", "Robots, máquinas y su control", "Roboter, Maschinen und ihre Steuerung", "Robots, machines et leur commande", "Robot, macchine e il loro controllo", "ロボット・機械とその制御", "机器人、机器及其控制"),
    "tag_urtc": ("Tools, firmware and the Smart Rack", "Herramientas, firmware y Smart Rack", "Werkzeuge, Firmware und Smart Rack", "Outils, firmware et Smart Rack", "Strumenti, firmware e Smart Rack", "ツール、ファームウェア、スマートラック", "工具、固件与智能机架"),
    "tag_armor": ("Perimeter security, solar and electrical", "Seguridad perimetral, solar y eléctrica", "Perimeterschutz, Solar und Elektrik", "Sécurité périmétrique, solaire et électrique", "Sicurezza perimetrale, solare ed elettrica", "境界警備・太陽光・電気", "周界安防、太阳能与电气"),
}
MISSING_LANGUAGE = "en"


def keys() -> tuple[str, ...]:
    return tuple(_ROWS)


def text(language: str, key: str) -> str:
    """The text for a key in a language; English when the language is unknown, and the key itself when nothing matches."""
    row = _ROWS.get(key)
    if row is None:
        return key
    index = {code: position for position, (code, _name) in enumerate(LANGUAGES)}.get(language, 0)
    return row[index]
