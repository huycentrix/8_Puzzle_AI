import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Effects

Item {
    id: controlPanelRoot
    width: 540
    height: 68
    property var configPanelRef
    property var puzzleBoardRef
    property var metricsRef

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
            MaterialIcon {
                iconCode: "\ue045"
                font.pixelSize: 18
                color: "#0d1c2f"
                opacity: 0.8
            }

            Rectangle {
                id: pauseButton
                width: 41
                height: 41
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
                    onClicked: {
                        if (!configPanelRef || !puzzleBoardRef) {
                            return
                        }
                        let method = configPanelRef.selectedAlgorithm
                        let currentStatus = puzzleBoardRef.puzzleModel
                        let goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
                        backend.start_search(method, currentStatus, goal, speedSlider.value)
                    }
                }
            }

            MaterialIcon { iconCode: "\ue044"; font.pixelSize: 18; color: "#0d1c2f"; opacity: 0.8 }
            MaterialIcon { iconCode: "\ue01f"; font.pixelSize: 18; color: "#0d1c2f"; opacity: 0.8 }
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
                    y: speedSlider.topPadding + (speedSlider.availableHeight / 2) - (height / 2)
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
                width: 30
            }
        }
    }

    Connections {
        target: backend

        function onStepUpdated(stepData) {
            if (puzzleBoardRef) {
                puzzleBoardRef.puzzleModel = stepData.currentNode.flatState
            }
            if (metricsRef) {
                metricsRef.totalSteps = stepData.stepNumber.toString()
                metricsRef.nodesExpanded = stepData.nodesExpanded.toLocaleString()
            }
        }

        function onSearchFinished(success, pathIds) {
            if (success && metricsRef) {
                metricsRef.solutionDepth = Math.max(0, pathIds.length - 1).toString()
            }
        }
    }
}
