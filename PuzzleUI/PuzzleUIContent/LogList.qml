import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: logRoot
    radius: 16
    color: "white"
    border.color: "#e2e8f0"
    border.width: 1

    ListModel {
        id: logModel
    }

    function appendLog(stepName, message) {
        let currentTime = new Date().toLocaleTimeString(Qt.locale(), "hh:mm:ss")
        logModel.insert(0, {
            "stepTitle": stepName,
            "details": message,
            "timestamp": currentTime
        })
    }

    function clearLog() {
        logModel.clear()
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
            model: logModel

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
                            text: model.stepTitle
                            font.family: "Manrope"
                            font.pixelSize: 10
                            font.weight: Font.Bold
                            color: index === 0 ? "#00488d" : "#94a3b8"
                        }
                        Item { Layout.fillWidth: true }
                        Text {
                            text: model.timestamp
                            font.family: "Manrope"
                            font.pixelSize: 10
                            color: "#94a3b8"
                        }
                    }

                    Text {
                        text: model.details
                        font.family: "Inter"
                        font.pixelSize: 14
                        font.weight: index === 0 ? Font.Bold : Font.Normal
                        color: index === 0 ? "#0f172a" : "#475569"
                        elide: Text.ElideRight
                    }
                }
            }
        }

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
