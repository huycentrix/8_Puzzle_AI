import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Rectangle {
    id: screen
    property string currentMode: "animation"
    signal requestModeChange(string mode)
    readonly property real boardScale: Math.max(0.78, Math.min(1.0, (height - 180) / 620))
    readonly property var defaultStartState: [1, 2, 3, 4, 0, 5, 7, 8, 6]
    property real setupPanelWidth: width < 1500 ? 250 : 280
    property real executionLogWidth: width < 1500 ? 280 : 310
    width: 1440
    height: 810
    color: "#f8f9ff"

    RowLayout {
        id: mainLayout
        anchors.fill: parent
        spacing: 0

        Rectangle {
            id: sideBar
            Layout.preferredWidth: 210
            Layout.minimumWidth: 210
            Layout.fillHeight: true
            color: "#eff4ff"

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 19
                spacing: 8

                SideButton {
                    Layout.fillWidth: true
                    text: "Puzzle Setup"
                    iconCode: "\uf1b4"
                    isActive: screen.currentMode === "animation"
                    onClicked: screen.requestModeChange("animation")
                }

                SideButton {
                    Layout.fillWidth: true
                    text: "Search Tree"
                    iconCode: "\ue037"
                    isActive: screen.currentMode === "tree"
                    onClicked: screen.requestModeChange("tree")
                }

                Item { Layout.fillHeight: true }
            }
        }

        Item {
            Layout.leftMargin: 20
            Layout.preferredWidth: screen.setupPanelWidth
            Layout.minimumWidth: 230
            Layout.maximumWidth: 420
            Layout.fillHeight: true
            Layout.topMargin: 20
            Layout.bottomMargin: 20

            ScrollView {
                id: leftPanelScroll
                anchors.fill: parent
                anchors.rightMargin: 12
                clip: true

                ColumnLayout {
                    width: Math.max(0, leftPanelScroll.availableWidth - 4)
                    spacing: 20

                    ConfigPanel {
                        id: configPanel
                        Layout.fillWidth: true
                    }

                    Button {
                        Layout.fillWidth: true
                        text: "Edit Start State"
                        onClicked: {
                            startStateDialog.currentState = mainGrid.puzzleModel.slice(0)
                            startStateDialog.open()
                        }
                    }

                    MetricsPanel {
                        Layout.fillWidth: true
                    }
                }
            }

            Rectangle {
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.right: parent.right
                width: 14
                color: setupResizeArea.containsMouse || setupResizeArea.pressed ? "#dbeafe" : "transparent"
                z: 2

                MouseArea {
                    id: setupResizeArea
                    anchors.fill: parent
                    hoverEnabled: true
                    preventStealing: true
                    cursorShape: Qt.SizeHorCursor
                    property real startScreenX: 0
                    property real startWidth: 0

                    onPressed: function(mouse) {
                        startScreenX = setupResizeArea.mapToItem(screen, mouse.x, mouse.y).x
                        startWidth = screen.setupPanelWidth
                    }

                    onPositionChanged: function(mouse) {
                        if (!pressed) return
                        const currentX = setupResizeArea.mapToItem(screen, mouse.x, mouse.y).x
                        const delta = currentX - startScreenX
                        screen.setupPanelWidth = Math.max(230, Math.min(420, startWidth + delta))
                    }
                }
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.topMargin: 20
            Layout.bottomMargin: 20
            Layout.leftMargin: 24
            Layout.rightMargin: 24
            spacing: 12

            Item { Layout.fillHeight: true }

            PuzzleGrid {
                id: mainGrid
                implicitWidth: 468
                implicitHeight: 468
                Layout.alignment: Qt.AlignHCenter
                scale: screen.boardScale
            }

            ControlPanel {
                id: ctrlPanel
                strategyName: configPanel.selectedStrategy
                heuristicName: configPanel.selectedHeuristic
                implicitWidth: 540
                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 8
            }

            Item { Layout.fillHeight: true }
        }

        Item {
            Layout.preferredWidth: screen.executionLogWidth
            Layout.minimumWidth: 250
            Layout.maximumWidth: 380
            Layout.fillHeight: true
            Layout.rightMargin: 16
            Layout.topMargin: 20
            Layout.bottomMargin: 20

            Rectangle {
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                width: 14
                color: logResizeArea.containsMouse || logResizeArea.pressed ? "#dbeafe" : "transparent"
                z: 2

                MouseArea {
                    id: logResizeArea
                    anchors.fill: parent
                    hoverEnabled: true
                    preventStealing: true
                    cursorShape: Qt.SizeHorCursor
                    property real startScreenX: 0
                    property real startWidth: 0

                    onPressed: function(mouse) {
                        startScreenX = logResizeArea.mapToItem(screen, mouse.x, mouse.y).x
                        startWidth = screen.executionLogWidth
                    }

                    onPositionChanged: function(mouse) {
                        if (!pressed) return
                        const currentX = logResizeArea.mapToItem(screen, mouse.x, mouse.y).x
                        const delta = startScreenX - currentX
                        screen.executionLogWidth = Math.max(250, Math.min(420, startWidth + delta))
                    }
                }
            }

            LogList {
                id: executionLog
                anchors.fill: parent
            }
        }
    }

    StartStateDialog {
        id: startStateDialog
        parent: Overlay.overlay
        anchors.centerIn: parent
        titleText: "Edit Start State"
        defaultState: screen.defaultStartState
        goalState: [1, 2, 3, 4, 5, 6, 7, 8, 0]

        onApplied: function(state) {
            Backend.set_start_state(state)
        }
    }
}
