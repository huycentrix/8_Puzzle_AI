import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: logRoot
    radius: 16
    color: "white" // Nền trắng để nổi bật trên nền xám nhẹ của app
    border.color: "#e2e8f0"
    border.width: 1

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

        // Header: Tiêu đề và Icon
        RowLayout {
            Layout.fillWidth: true
            Text {
                text: "Execution Log"
                font.family: "Space Grotesk"
                font.pixelSize: 18
                font.weight: Font.Bold
                color: "#0d1c2f"
            }
            Item { Layout.fillWidth: true }
            MaterialIcon {
                iconCode: "\ue8d8" // terminal icon
                color: "#727783"
                font.pixelSize: 20
            }
        }

        // Danh sách Nhật ký (ListView)
        ListView {
            id: logListView
            Layout.fillWidth: true
            Layout.fillHeight: true // QUAN TRỌNG: Để ListView chiếm hết chiều cao còn lại
            spacing: 8
            clip: true // Chống tràn nội dung ra ngoài Rectangle
            model: 10 // Giả định có nhiều bước để test cuộn

            ScrollBar.vertical: ScrollBar {
                policy: ScrollBar.AsNeeded
                active: true
            }

            delegate: Rectangle {
                width: logListView.width
                height: 72
                radius: 12
                color: index === 0 ? "#eff6ff" : "transparent"
                border.width: index === 0 ? 1 : 0
                border.color: "#dbeafe"

                // Thanh chỉ báo bên trái cho bước hiện tại
                Rectangle {
                    width: 4; height: parent.height
                    anchors.left: parent.left
                    color: "#00488d"
                    visible: index === 0
                    radius: 2
                }

                ColumnLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 16
                    anchors.rightMargin: 16
                    spacing: 2

                    RowLayout {
                        Layout.fillWidth: true
                        Text {
                            text: "STEP " + (index + 1)
                            font.family: "Manrope"
                            font.pixelSize: 10
                            font.weight: Font.Bold
                            color: index === 0 ? "#00488d" : "#94a3b8"
                        }
                        Item { Layout.fillWidth: true }
                        Text {
                            text: "10:42:0" + index
                            font.family: "Manrope"
                            font.pixelSize: 10
                            color: "#94a3b8"
                        }
                    }

                    Text {
                        text: index === 0 ? "Shift Tile 4 Right" : "Previous Movement"
                        font.family: "Inter"
                        font.pixelSize: 14
                        font.weight: index === 0 ? Font.Bold : Font.Normal
                        color: index === 0 ? "#0f172a" : "#475569"
                    }
                }
            }
        }

        // Nút Export (Luôn nằm ở dưới cùng)
        Button {
            Layout.fillWidth: true
            height: 40
            contentItem: Row {
                spacing: 8
                anchors.centerIn: parent
                MaterialIcon { iconCode: "\uf090"; font.pixelSize: 16; color: "#475569" }
                Text { text: "Export Log"; font.family: "Inter"; font.weight: Font.Bold; color: "#475569" }
            }
            background: Rectangle {
                radius: 10
                border.color: "#e2e8f0"
                color: parent.hovered ? "#f8fafc" : "white"
            }
        }
    }
}