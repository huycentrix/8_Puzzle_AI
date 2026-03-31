import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: logRoot
    radius: 16
    color: "white"
    border.color: "#e2e8f0"
    border.width: 1

    // 1. Khai báo Model để lưu trữ nhật ký thực tế
    ListModel {
        id: realLogModel
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

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
                iconCode: "\ue8d8"
                color: "#727783"
                font.pixelSize: 20
            }
        }

        ListView {
            id: logListView
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 8
            clip: true

            // 2. Sử dụng model thực tế thay vì con số giả định
            model: realLogModel

            ScrollBar.vertical: ScrollBar {
                policy: ScrollBar.AsNeeded
                active: true
            }

            delegate: Rectangle {
                width: logListView.width
                height: 72
                radius: 12
                // Bước mới nhất (index 0) sẽ có màu nền xanh nhạt
                color: index === 0 ? "#eff6ff" : "transparent"
                border.width: index === 0 ? 1 : 0
                border.color: "#dbeafe"

                Rectangle {
                    width: 4
                    height: parent.height
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
                            // Lấy dữ liệu từ vai trò 'step' của model
                            text: "STEP " + model.step
                            font.family: "Manrope"
                            font.pixelSize: 10
                            font.weight: Font.Bold
                            color: index === 0 ? "#00488d" : "#94a3b8"
                        }
                        Item { Layout.fillWidth: true }
                        Text {
                            // Lấy dữ liệu từ vai trò 'time' của model
                            text: model.time
                            font.family: "Manrope"
                            font.pixelSize: 10
                            color: "#94a3b8"
                        }
                    }

                    Text {
                        // Lấy dữ liệu từ vai trò 'action' của model
                        text: model.action
                        font.family: "Inter"
                        font.pixelSize: 14
                        font.weight: index === 0 ? Font.Bold : Font.Normal
                        color: index === 0 ? "#0f172a" : "#475569"
                    }
                }
            }
        }

        // Button {
        //     Layout.fillWidth: true
        //     height: 40
        //     onClicked: {
        //         // Placeholder cho chức năng xuất log
        //         console.log("Exporting " + realLogModel.count + " log entries...")
        //     }
        //     contentItem: Row {
        //         spacing: 8
        //         anchors.centerIn: parent
        //         MaterialIcon { iconCode: "\uf090"; font.pixelSize: 16; color: "#475569" }
        //         Text { text: "Export Log"; font.family: "Inter"; font.weight: Font.Bold; color: "#475569" }
        //     }
        //     background: Rectangle {
        //         radius: 10
        //         border.color: "#e2e8f0"
        //         color: parent.hovered ? "#f8fafc" : "white"
        //     }
        // }
    }

    // 3. Kết nối với tín hiệu từ Python để cập nhật Log
    Connections {
        target: Backend

        // Khi bắt đầu giải mới, xóa sạch log cũ
        function onPuzzleModelChanged() {
            if (Backend.totalSteps === 0) {
                realLogModel.clear()
            }
        }

        // Tín hiệu mới (cần thêm vào bridge.py) để đẩy log mới vào đầu danh sách
        function onNewLogEntry(step, action, time) {
            realLogModel.insert(0, {
                "step": step,
                "action": action,
                "time": time
            })
        }
    }
}
