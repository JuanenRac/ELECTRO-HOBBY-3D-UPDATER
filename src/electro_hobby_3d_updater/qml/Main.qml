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
            Rectangle {
                Layout.preferredWidth: 54; Layout.preferredHeight: 54; radius: 16
                color: "#0e3045"; border.width: 1; border.color: "#2d7695"
                Image {
                    anchors.fill: parent; anchors.margins: 5
                    source: "../assets/ELECTRO_HOBBY_3D_ICON.svg"
                    sourceSize.width: 128; sourceSize.height: 128
                    fillMode: Image.PreserveAspectFit
                    smooth: true
                }
            }
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
                // The text belongs to the check box itself: without one it centres its box over the label.
                text: ui("offline")
                checked: window.offline
                onToggled: window.offline = checked
                contentItem: LabelText { text: offlineBox.text; leftPadding: offlineBox.indicator.width + offlineBox.spacing; verticalAlignment: Text.AlignVCenter }
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
                    Rectangle {
                        id: copyIconButton
                        property bool copied: false
                        Layout.preferredWidth: 36
                        Layout.preferredHeight: 32
                        radius: 8
                        color: copyIconMouse.containsMouse ? "#1b3c52" : "#102a3b"
                        border.width: 1
                        border.color: copyIconButton.copied ? "#5df0c4" : "#264966"
                        // the icon of "copy": two sheets, one in front of the other
                        Item {
                            anchors.centerIn: parent
                            width: 18; height: 18
                            Rectangle { x: 6; y: 0; width: 11; height: 12; radius: 2; color: "transparent"; border.width: 1.6; border.color: copyIconButton.copied ? "#5df0c4" : "#9fd8e3" }
                            Rectangle { x: 1; y: 5; width: 11; height: 12; radius: 2; color: copyIconMouse.containsMouse ? "#1b3c52" : "#102a3b"; border.width: 1.6; border.color: copyIconButton.copied ? "#5df0c4" : "#9fd8e3" }
                        }
                        Timer { id: copiedTimer; interval: 1400; onTriggered: copyIconButton.copied = false }
                        MouseArea {
                            id: copyIconMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: { logArea.selectAll(); logArea.copy(); logArea.deselect(); copyIconButton.copied = true; copiedTimer.restart() }
                        }
                        ToolTip.visible: copyIconMouse.containsMouse && ToolTip.text !== ""
                        ToolTip.text: ""
                    }
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

        RowLayout {
            Layout.fillWidth: true
            spacing: 14
            LabelText { text: ui("about") + "  ·  v" + backend.version; color: window.textMuted; font.pixelSize: 11; Layout.fillWidth: true }
            GameButton { text: ui("menu_about"); accent: "#264966"; implicitHeight: 34; Layout.preferredWidth: 140; onClicked: aboutDialog.open() }
        }
    }

    // A real Version/Author/Email/License row, the same as the About window of the three updaters.
    component AboutInfoRow: Rectangle {
        property string label: ""
        property string value: ""
        property color valueColor: window.textPrimary
        Layout.fillWidth: true
        implicitHeight: 34
        radius: 8
        color: "#07111e"
        border.width: 1
        border.color: window.border
        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 12
            anchors.rightMargin: 12
            LabelText { text: label.toUpperCase(); color: window.textMuted; font.pixelSize: 9; font.bold: true; font.letterSpacing: 1 }
            Item { Layout.fillWidth: true }
            LabelText { text: value; color: valueColor; font.pixelSize: 11 }
        }
    }

    Dialog {
        id: aboutDialog
        modal: true
        anchors.centerIn: parent
        width: 460
        padding: 24
        background: Rectangle { color: window.panel; radius: 16; border.color: window.border; border.width: 1 }
        contentItem: ColumnLayout {
            spacing: 8
            RowLayout {
                Layout.fillWidth: true
                Item { Layout.fillWidth: true }
                Rectangle {
                    Layout.preferredWidth: 88; Layout.preferredHeight: 88; radius: 20
                    color: "#0e3045"; border.width: 1; border.color: "#2d7695"
                    Image {
                        anchors.fill: parent; anchors.margins: 10
                        source: "../assets/ELECTRO_HOBBY_3D_ICON.svg"
                        sourceSize.width: 256; sourceSize.height: 256
                        fillMode: Image.PreserveAspectFit
                        smooth: true
                    }
                }
                Item { Layout.fillWidth: true }
            }
            LabelText { Layout.fillWidth: true; horizontalAlignment: Text.AlignHCenter; text: ui("title"); font.pixelSize: 20; font.bold: true }
            LabelText { Layout.fillWidth: true; horizontalAlignment: Text.AlignHCenter; text: ui("about_tagline"); color: "#38d4e6"; font.pixelSize: 12; font.bold: true }
            LabelText { Layout.fillWidth: true; horizontalAlignment: Text.AlignHCenter; text: ui("about_description"); color: window.textMuted; font.pixelSize: 11 }
            ColumnLayout {
                Layout.fillWidth: true
                Layout.topMargin: 6
                spacing: 4
                AboutInfoRow { label: ui("about_version_label"); value: backend.version }
                AboutInfoRow { label: ui("about_author_label"); value: "JuanenRac (Electro Hobby 3D)" }
                AboutInfoRow {
                    label: ui("about_email_label")
                    valueColor: "#38d4e6"
                    value: "electrohobby3d@gmail.com"
                    MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor; onClicked: Qt.openUrlExternally("mailto:electrohobby3d@gmail.com") }
                }
                AboutInfoRow { label: ui("about_license_label"); value: ui("about_license") }
            }
            RowLayout {
                Layout.fillWidth: true
                Layout.topMargin: 8
                GameButton { text: ui("open_github"); Layout.preferredWidth: 200; accent: "#264966"; onClicked: Qt.openUrlExternally("https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER") }
                Item { Layout.fillWidth: true }
                GameButton { text: ui("close"); Layout.preferredWidth: 140; accent: "#38d4e6"; onClicked: aboutDialog.close() }
            }
        }
    }

    FolderDialog {
        id: folderDialog
        onAccepted: backend.setWorkspace(selectedFolder.toString())
    }
}
