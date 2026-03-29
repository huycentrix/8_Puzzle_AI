import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Rectangle {
    id: screen
    width: 1440
    height: 810
    color: "#f8f9ff"

    RowLayout {
        id: mainLayout
        anchors.fill: parent
        spacing: 0

        // --- CỘT 0: SideBar (Rộng 210) ---
        Rectangle {
            id: sideBar
            Layout.preferredWidth: 210
            Layout.minimumWidth: 210
            Layout.fillHeight: true
            color: "#eff4ff"
            ColumnLayout {

                anchors.fill: parent

                anchors.margins: 19 // 25 * 0.75

                spacing: 8 // 10 * 0.75

                SideButton {

                    Layout.fillWidth: true

                    text: "Algorithm"

                    iconCode: "\ue871"
                }

                SideButton {

                    Layout.fillWidth: true

                    text: "Puzzle Setup"

                    iconCode: "\uf1b4"

                    isActive: true
                }

                SideButton {

                    Layout.fillWidth: true

                    text: "Execution"

                    iconCode: "\ue037"
                }

                Item {

                    Layout.fillHeight: true
                }
            }
        }

        // --- CỘT 1: Config & Metrics (Đã thu hẹp xuống 210) ---
        ColumnLayout {
            Layout.leftMargin: 30
            Layout.preferredWidth: 210 // Giảm từ 240 xuống 210
            Layout.minimumWidth: 210
            Layout.fillHeight: true
            Layout.topMargin: 30
            Layout.bottomMargin: 30
            spacing: 20

            ConfigPanel {
                Layout.fillWidth: true
            }
            MetricsPanel {
                Layout.fillWidth: true
            }
            Item {
                Layout.fillHeight: true
            }
        }

        // --- CỘT 2: Puzzle Visualization (Tạo thêm khoảng cách) ---
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.topMargin: 30
            Layout.bottomMargin: 30

            // Thêm Margin trái/phải để ép khoảng cách với Control Panel
            Layout.leftMargin: 40
            Layout.rightMargin: 40
            spacing: 15

            Item {
                Layout.fillHeight: true
            }

            PuzzleGrid {
                id: mainGrid
                // Cập nhật kích thước gợi ý mới
                implicitWidth: 468
                implicitHeight: 468
                Layout.alignment: Qt.AlignHCenter
            }

            ControlPanel {
                implicitWidth: 540
                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 15
            }

            Item {
                Layout.fillHeight: true
            }
        }

        // --- CỘT 3: Execution Log (Giữ nguyên hoặc thu hẹp nhẹ) ---
        LogList {
            id: executionLog
            Layout.preferredWidth: 270 // Giảm nhẹ từ 285 xuống 270
            Layout.minimumWidth: 270
            Layout.fillHeight: true
            Layout.rightMargin: 30
            Layout.topMargin: 30
            Layout.bottomMargin: 30
        }
    }
}
