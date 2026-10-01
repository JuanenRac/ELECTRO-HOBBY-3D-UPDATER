// =============================================================================
// ELECTRO-HOBBY-3D-UPDATER - Qt Quick window: Main.qml
// Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
// GPL-3.0-or-later - see LICENSE
// =============================================================================
// Three cards, one per ecosystem; each opens that ecosystem's own updater or asks it for its
// status. Everything shown comes from the Python bridge: nothing is decided here.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

ApplicationWindow {
    id: window
    width: 1180
    height: 760
    minimumWidth: 860
    minimumHeight: 600
    visible: true
    title: ui("title")
    color: "#07111e"

    property string languageTick: backend.language
    readonly property color panel: "#101d30"
    readonly property color panelAlt: "#14253b"
    readonly property color border: "#294965"
    readonly property color textPrimary: "#edf7ff"
    readonly property color textMuted: "#91a8bd"
    property bool offline: false

    function ui(key) {
        var ignored = languageTick   // the labels follow the language
        return backend.tr(backend.language, key)
    }

    component LabelText: Text {
        color: window.textPrimary
        font.family: "Bahnschrift"
        font.pixelSize: 13
        wrapMode: Text.WordWrap
        renderType: Text.QtRendering
    }

    component GameButton: Button {
        id: gameButton
        property color accent: "#397dff"
        implicitHeight: 42
        hoverEnabled: true
        font.family: "Bahnschrift"
        font.pixelSize: 13
        font.bold: true
        contentItem: Text {
            text: gameButton.text
            color: gameButton.enabled ? "#f5fbff" : "#6d8294"
            font: gameButton.font
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideRight
        }
        background: Rectangle {
            radius: 10
            color: !gameButton.enabled ? "#17263a" : gameButton.down ? Qt.darker(gameButton.accent, 1.5) : gameButton.hovered ? Qt.lighter(gameButton.accent, 1.15) : Qt.darker(gameButton.accent, 1.2)
            border.width: 1
            border.color: gameButton.enabled ? gameButton.accent : "#294965"
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 22
        spacing: 16

        RowLayout {
            Layout.fillWidth: true
            spacing: 16
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 4
                LabelText { text: ui("title"); font.pixelSize: 28; font.bold: true }
                LabelText { text: ui("subtitle"); color: window.textMuted; Layout.fillWidth: true }
            }
            ColumnLayout {
                spacing: 4
                LabelText { text: ui("language"); color: window.textMuted; font.pixelSize: 11 }
                ComboBox {
                    id: languagePicker
                    model: backend.languages
                    textRole: "name"
                    valueRole: "code"
                    implicitWidth: 150
                    Component.onCompleted: currentIndex = 0
                    onActivated: backend.setLanguage(currentValue)
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: false
            spacing: 16
            Repeater {
                model: backend.ecosystems
                delegate: Rectangle {
                    required property var modelData
                    Layout.fillWidth: true
                    Layout.preferredHeight: 290
                    radius: 16
                    color: window.panel
                    border.width: 1
                    border.color: Qt.rgba(Qt.color(modelData.accent).r, Qt.color(modelData.accent).g, Qt.color(modelData.accent).b, 0.55)
                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 18
                        spacing: 10
                        Rectangle { Layout.preferredWidth: 46; Layout.preferredHeight: 4; radius: 2; color: modelData.accent }
                        LabelText { text: modelData.name; font.pixelSize: 24; font.bold: true; color: modelData.accent }
                        LabelText { text: ui("tag_" + modelData.key); color: window.textMuted; Layout.fillWidth: true }
                        LabelText { text: modelData.manifest; font.family: "Consolas"; font.pixelSize: 11; color: window.textMuted }
                        LabelText { visible: !modelData.available; text: ui("missing"); color: "#f3ba55"; font.pixelSize: 11; Layout.fillWidth: true }
                        Item { Layout.fillHeight: true }
                        GameButton { Layout.fillWidth: true; accent: modelData.accent; text: ui("open"); enabled: modelData.available; onClicked: backend.openUpdater(modelData.key) }
                        GameButton { Layout.fillWidth: true; accent: "#397dff"; text: ui("check"); enabled: modelData.available && !backend.busy; onClicked: backend.check(modelData.key, window.offline) }
                    }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 14
            GameButton { text: ui("check_all"); accent: "#43db9b"; enabled: !backend.busy; onClicked: backend.check("all", window.offline) }
            CheckBox {
                id: offlineBox
                checked: window.offline
                onToggled: window.offline = checked
                contentItem: LabelText { text: ui("offline"); leftPadding: offlineBox.indicator.width + 8; verticalAlignment: Text.AlignVCenter }
            }
            LabelText { text: backend.busy ? ui("running") : ""; color: "#38d4e6" }
            Item { Layout.fillWidth: true }
            LabelText { text: ui("workspace") + ":"; color: window.textMuted }
            LabelText { text: backend.workspace; font.family: "Consolas"; font.pixelSize: 11; elide: Text.ElideMiddle; Layout.maximumWidth: 360 }
            GameButton { text: ui("browse"); accent: "#294965"; implicitHeight: 34; onClicked: folderDialog.open() }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: 16
            color: window.panelAlt
            border.width: 1
            border.color: window.border
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 14
                spacing: 8
                RowLayout {
                    Layout.fillWidth: true
                    LabelText { text: ui("log"); font.bold: true; Layout.fillWidth: true }
                    GameButton { text: ui("clear"); accent: "#294965"; implicitHeight: 30; onClicked: backend.clearLog() }
                }
                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    TextArea {
                        id: logArea
                        readOnly: true
                        text: backend.log
                        color: "#c9e4ff"
                        font.family: "Consolas"
                        font.pixelSize: 12
                        wrapMode: TextEdit.NoWrap
                        background: null
                        onTextChanged: cursorPosition = length
                    }
                }
            }
        }

        LabelText { text: ui("about") + "  ·  v" + backend.version; color: window.textMuted; font.pixelSize: 11; Layout.fillWidth: true }
    }

    FolderDialog {
        id: folderDialog
        onAccepted: backend.setWorkspace(selectedFolder.toString())
    }
}
