import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Effects

Item {
    id: controlPanelRoot
    width: 540
    height: 68
    property string strategyName: ""
    property string heuristicName: "Manhattan Distance"

    MultiEffect {
        source: backgroundRect
        anchors.fill: backgroundRect
        shadowEnabled: true
        shadowBlur: 0.75
        shadowColor: "#15000000"
        shadowVerticalOffset: 5
    }

    Rectangle {
        id: backgroundRect
        anchors.fill: parent
        radius: 12
        color: "#CCFFFFFF"
    }

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 23
        anchors.rightMargin: 23
        spacing: 0

        RowLayout {
            spacing: 19

            Rectangle {
                Layout.preferredWidth: 41
                Layout.preferredHeight: 41
                radius: 9
                color: "#005fb8"

                MaterialIcon {
                    anchors.centerIn: parent
                    iconCode: "\ue035"
                    color: "white"
                    font.pixelSize: 21
                }

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor

                    onClicked: {
                        Backend.startSolve(mainGrid.puzzleModel, controlPanelRoot.strategyName, speedSlider.value, controlPanelRoot.heuristicName)
                    }
                    onPressed: parent.opacity = 0.7
                    onReleased: parent.opacity = 1.0
                }
            }

            Rectangle {
                Layout.preferredWidth: 41
                Layout.preferredHeight: 41
                radius: 9
                color: stopMouseArea.containsMouse ? "#e8eefb" : "transparent"
                border.width: 1
                border.color: "#b8c8e6"

                MaterialIcon {
                    anchors.centerIn: parent
                    iconCode: "\ue047"
                    color: "#0d1c2f"
                    font.pixelSize: 20
                    opacity: stopMouseArea.containsMouse ? 1.0 : 0.72
                }

                MouseArea {
                    id: stopMouseArea
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    hoverEnabled: true

                    onClicked: Backend.stopSolve()
                    onPressed: parent.opacity = 0.7
                    onReleased: parent.opacity = 1.0
                }
            }

            Rectangle {
                Layout.preferredWidth: 41
                Layout.preferredHeight: 41
                color: "transparent"

                MaterialIcon {
                    anchors.centerIn: parent
                    iconCode: "\uf053"
                    color: "#0d1c2f"
                    font.pixelSize: 21
                    opacity: shuffleMouseArea.containsMouse ? 1.0 : 0.7
                }

                MouseArea {
                    id: shuffleMouseArea
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    hoverEnabled: true

                    onClicked: Backend.shufflePuzzle()
                    onPressed: parent.opacity = 0.5
                    onReleased: parent.opacity = 1.0
                }
            }
        }

        Item { Layout.fillWidth: true }

        RowLayout {
            spacing: 11

            Text {
                text: "SPEED"
                font.family: "Manrope"
                font.pixelSize: 8
                font.weight: Font.Bold
                color: "#727783"
            }

            Slider {
                id: speedSlider
                from: 0.5
                to: 4.0
                value: 2.0
                stepSize: 0.1
                implicitWidth: 120

                background: Rectangle {
                    implicitHeight: 3
                    width: speedSlider.availableWidth
                    radius: 2
                    color: "#d5e3fc"

                    Rectangle {
                        width: speedSlider.visualPosition * parent.width
                        height: parent.height
                        color: "#005fb8"
                        radius: 2
                    }
                }

                handle: Rectangle {
                    x: speedSlider.leftPadding + speedSlider.visualPosition * (speedSlider.availableWidth - width)
                    y: speedSlider.topPadding + speedSlider.availableHeight / 2 - height / 2
                    implicitWidth: 14
                    implicitHeight: 14
                    radius: 7
                    color: "white"
                    border.color: "#005fb8"
                    border.width: 2
                }
            }

            Text {
                text: speedSlider.value.toFixed(1) + "x"
                font.family: "Space Grotesk"
                font.pixelSize: 11
                font.weight: Font.Bold
                color: "#005fb8"
                Layout.preferredWidth: 30
            }
        }
    }
}
