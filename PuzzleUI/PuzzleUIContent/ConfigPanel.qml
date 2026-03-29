import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    Layout.fillWidth: true
    implicitHeight: 450 // Tăng nhẹ chiều cao để thoải mái hơn
    color: "#eff4ff"
    radius: 16

    // 1. THÊM ALIAS: Để ControlPanel có thể lấy được thuật toán đang chọn
    property alias selectedAlgorithm: strategyCombo.currentText
    // Thêm alias cho Heuristic nếu cần
    property string selectedHeuristic: manhattanBtn.checked ? "Manhattan" : (misplacedBtn.checked ? "Misplaced" : "Euclidean")

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

        // --- SECTION: SEARCH STRATEGY ---
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
                
                // 2. CẬP NHẬT ĐỦ 8 THUẬT TOÁN (Khớp với logic trong bridge.py)
                model: [
                    "A* Search",
                    "Breadth-First Search (BFS)",
                    "Depth-First Search (DFS)",
                    "Uniform Cost Search (UCS)",
                    "Greedy Best-First Search (GBFS)",
                    "Iterative Deepening Search (IDDFS)",
                    "Bidirectional Search",
                    "Iterative Deepening A* (IDA*)"
                ]

                delegate: ItemDelegate {
                    width: strategyCombo.width
                    contentItem: Text {
                        text: modelData
                        color: "#0d1c2f"
                        font.family: "Manrope"
                        font.pixelSize: 14
                        verticalAlignment: Text.AlignVCenter
                    }
                    highlighted: strategyCombo.highlightedIndex === index
                }

                contentItem: Text {
                    leftPadding: 12
                    text: strategyCombo.currentText
                    font.family: "Manrope"
                    font.pixelSize: 14
                    color: "#0d1c2f"
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    implicitHeight: 45
                    radius: 8
                    color: "white"
                    border.color: strategyCombo.visualFocus ? "#005fb8" : "#d5e3fc"
                    border.width: 1
                }
            }
        }

        // --- SECTION: HEURISTIC (Dành cho A*, IDA*, GBFS) ---
        ColumnLayout {
            spacing: 12
            Layout.fillWidth: true
            // Chỉ hiện Heuristic nếu thuật toán được chọn có dùng nó
            visible: strategyCombo.currentText.includes("A*") || strategyCombo.currentText.includes("Greedy")

            Text {
                text: "HEURISTIC FUNCTION"
                font.family: "Manrope"
                font.pixelSize: 11
                font.weight: Font.Bold
                color: "#727783"
                Layout.leftMargin: 2
            }

            component StyledRadioButton : RadioButton {
                id: control
                font.family: "Manrope"
                font.pixelSize: 14
                
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
                        width: 6; height: 6
                        anchors.centerIn: parent
                        radius: 3
                        color: "white"
                        visible: control.checked
                    }
                }
            }

            StyledRadioButton { id: manhattanBtn; text: "Manhattan Distance"; checked: true }
            StyledRadioButton { id: misplacedBtn; text: "Misplaced Tiles" }
            StyledRadioButton { id: euclideanBtn; text: "Euclidean Distance" }
        }

        Item { Layout.fillHeight: true }
    }
}