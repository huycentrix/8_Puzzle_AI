import QtQuick

Item {
    id: root
    property var nodeData: []
    property int g: 0
    property int h: 0
    property int f: 0
    property string status: "frontier"
    signal hovered(var state)

    width: 124
    height: 154

    Column {
        anchors.fill: parent
        spacing: 6

        Rectangle {
            width: 124
            height: 124
            radius: 10
            color: status === "path" ? "#fff4c2" : (status === "explored" ? "#d8dee9" : "#ffffff")
            border.width: status === "path" ? 3 : 1
            border.color: status === "path" ? "#b7791f" : "#475569"

            Grid {
                anchors.centerIn: parent
                columns: 3
                spacing: 0

                Repeater {
                    model: root.nodeData ? root.nodeData.length : 0
                    delegate: Rectangle {
                        property int tileValue: root.nodeData[index]
                        width: 34
                        height: 34
                        border.width: 1
                        border.color: "#94a3b8"
                        color: tileValue === 0 ? "#e2e8f0" : "transparent"

                        Text {
                            anchors.centerIn: parent
                            text: tileValue === 0 ? "" : tileValue
                            font.pixelSize: 16
                            font.bold: true
                            color: "#0f172a"
                        }
                    }
                }
            }

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                onEntered: root.hovered(root.nodeData)
            }
        }

        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            text: "f=" + root.f + "  g=" + root.g + "  h=" + root.h
            font.pixelSize: 12
            font.bold: true
            color: "#0f172a"
        }
    }
}
