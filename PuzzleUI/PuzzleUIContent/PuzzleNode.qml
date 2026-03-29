import QtQuick

Item {
    id: root
    property var nodeData: []
    property int g: 0
    property int h: 0
    property int f: 0
    property string status: "frontier"
    signal hovered(var state)

    width: 148
    height: 184

    Column {
        anchors.fill: parent
        spacing: 8

        Rectangle {
            width: 148
            height: 148
            radius: 16
            color: status === "path" ? "#fff4c2" : (status === "explored" ? "#e5ebf5" : "#edf4ff")
            border.width: status === "path" ? 4 : 1
            border.color: status === "path" ? "#b7791f" : "#b9c8dd"

            Grid {
                anchors.centerIn: parent
                columns: 3
                spacing: 6

                Repeater {
                    model: root.nodeData ? root.nodeData.length : 0
                    delegate: Rectangle {
                        property int tileValue: (root.nodeData && index < root.nodeData.length) ? root.nodeData[index] : 0
                        width: 38
                        height: 38
                        radius: 8
                        border.width: tileValue === 0 ? 0 : 1
                        border.color: "#1d4ed8"
                        color: tileValue === 0 ? "#dbe4f0" : "#2563eb"

                        Text {
                            anchors.centerIn: parent
                            text: tileValue === 0 ? "" : tileValue
                            font.pixelSize: 18
                            font.bold: true
                            color: "#ffffff"
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
            font.pixelSize: 13
            font.bold: true
            color: "#0f172a"
        }
    }
}
