import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    Layout.fillWidth: true
    implicitHeight: 420 // Tăng chiều cao để chứa đủ các tùy chọn
    color: "#eff4ff"
    radius: 16

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 24
        spacing: 20

        // Tiêu đề chính
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
                model: ["A* Search", "Breadth-First Search", "Depth-First Search"]

                // Tùy chỉnh phần hiển thị văn bản khi đóng
                contentItem: Text {
                    leftPadding: 16
                    text: strategyCombo.displayText
                    font.family: "Inter"
                    font.pixelSize: 16
                    color: "#0d1c2f"
                    verticalAlignment: Text.AlignVCenter
                }

                // Tùy chỉnh nền (Hộp trắng bo góc)
                background: Rectangle {
                    implicitHeight: 52
                    color: "white"
                    radius: 8

                    // Icon mũi tên xuống (giống trong ảnh)
                    // Text {
                    //     anchors.right: parent.right
                    //     anchors.rightMargin: 16
                    //     anchors.verticalCenter: parent.verticalCenter
                    //     text: "\ue5cf" // expand_more
                    //     font.family: "Material Icons"
                    //     font.pixelSize: 24
                    //     color: "#727783"
                    // }
                }

                // Tùy chỉnh danh sách thả xuống (Popup)
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

        // --- SECTION: HEURISTIC FUNCTION ---
        ColumnLayout {
            spacing: 15
            Layout.fillWidth: true

            Text {
                text: "HEURISTIC FUNCTION"
                font.family: "Manrope"
                font.pixelSize: 11
                font.weight: Font.Bold
                color: "#727783"
                Layout.topMargin: 10
            }

            // Group để đảm bảo chỉ chọn được 1 radio button
            ButtonGroup { id: heuristicGroup }

            // Thành phần RadioButton tùy chỉnh
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

                // Vẽ vòng tròn theo phong cách trong ảnh
                indicator: Rectangle {
                    implicitWidth: 24
                    implicitHeight: 24
                    x: control.leftPadding
                    y: parent.height / 2 - height / 2
                    radius: 12
                    border.color: control.checked ? "#00488d" : "#727783"
                    border.width: control.checked ? 7 : 2 // Độ dày viền tạo hiệu ứng vòng tròn xanh
                    color: "transparent"

                    // Chấm trắng nhỏ ở giữa khi được chọn
                    Rectangle {
                        width: 6; height: 6
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

        Item { Layout.fillHeight: true } // Đẩy nội dung lên trên
    }
}
