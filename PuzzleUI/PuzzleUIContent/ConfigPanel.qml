import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    property alias selectedStrategy: strategyCombo.currentText
    property string selectedHeuristic: heuristicGroup.checkedButton ? heuristicGroup.checkedButton.text : "Manhattan Distance"

    Layout.fillWidth: true
    implicitHeight: 340
    color: "#eff4ff"
    radius: 16

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 24
        spacing: 20

        Text {
            text: "Algorithm Configuration"
            font.family: "Space Grotesk"
            font.pixelSize: 22
            font.weight: Font.Bold
            color: "#0d1c2f"
            Layout.bottomMargin: 5
        }

        ColumnLayout {
            spacing: 12
            Layout.fillWidth: true

            Text {
                text: "SEARCH STRATEGY"
                font.family: "Manrope"
                font.pixelSize: 11
                font.weight: Font.Bold
                color: "#727783"
                Layout.leftMargin: 2
            }

            ComboBox {
                id: strategyCombo
                Layout.fillWidth: true
                model: [
                    "A* Search",
                    "Breadth-First Search",
                    "Depth-First Search",
                    "Uniform Cost Search",
                    "Greedy Search",
                    "IDDFS",
                    "IDA* Search",
                    "Bidirectional Search"
                ]

                contentItem: Text {
                    leftPadding: 16
                    text: strategyCombo.displayText
                    font.family: "Inter"
                    font.pixelSize: 16
                    color: "#0d1c2f"
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    implicitHeight: 52
                    color: "white"
                    radius: 8
                }

                popup: Popup {
                    y: strategyCombo.height + 5
                    width: strategyCombo.width
                    implicitHeight: contentItem.implicitHeight
                    padding: 1

                    contentItem: ListView {
                        clip: true
                        implicitHeight: contentHeight
                        model: strategyCombo.popup.visible ? strategyCombo.delegateModel : null
                    }

                    background: Rectangle {
                        color: "white"
                        radius: 8
                        border.color: "#dde9ff"
                    }
                }
            }
        }

        ColumnLayout {
            spacing: 12
            Layout.fillWidth: true

            Text {
                text: "HEURISTIC FUNCTION"
                font.family: "Manrope"
                font.pixelSize: 11
                font.weight: Font.Bold
                color: "#727783"
                Layout.topMargin: 10
            }

            ButtonGroup { id: heuristicGroup }

            component StyledRadioButton : RadioButton {
                id: control
                font.family: "Inter"
                font.pixelSize: 16
                ButtonGroup.group: heuristicGroup

                contentItem: Text {
                    text: control.text
                    font: control.font
                    color: "#0d1c2f"
                    leftPadding: control.indicator.width + control.spacing
                    verticalAlignment: Text.AlignVCenter
                }

                indicator: Rectangle {
                    implicitWidth: 24
                    implicitHeight: 24
                    x: control.leftPadding
                    y: parent.height / 2 - height / 2
                    radius: 12
                    border.color: control.checked ? "#00488d" : "#727783"
                    border.width: control.checked ? 7 : 2
                    color: "transparent"

                    Rectangle {
                        width: 6
                        height: 6
                        anchors.centerIn: parent
                        radius: 3
                        color: "white"
                        visible: control.checked
                    }
                }
            }

            StyledRadioButton { text: "Manhattan Distance"; checked: true }
            StyledRadioButton { text: "Misplaced Tiles" }
            StyledRadioButton { text: "Euclidean Distance" }
        }

        Item { Layout.fillHeight: true }
    }
}
