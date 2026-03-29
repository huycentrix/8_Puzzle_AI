import QtQuick

Item {
    id: root
    property var nodeData: []
    property int g: 0
    property int h: 0
    property int f: 0
    property string status: "frontier"
    signal hovered(var state)

    readonly property int boardSize: 112
    readonly property int tileSize: 28
    readonly property int tileGap: 4

    width: 112
    height: 140

    Column {
        anchors.fill: parent
        spacing: 6

        Rectangle {
            width: root.boardSize
            height: root.boardSize
            radius: 12
            color: status === "current"
                ? "#dbeafe"
                : (status === "path"
                    ? "#fff4c2"
                    : (status === "explored" ? "#e5ebf5" : "#edf4ff"))
            border.width: status === "current" ? 3 : (status === "path" ? 3 : 1)
            border.color: status === "current"
                ? "#2563eb"
                : (status === "path" ? "#b7791f" : "#b9c8dd")

            Grid {
                anchors.centerIn: parent
                columns: 3
                spacing: root.tileGap

                Repeater {
                    model: root.nodeData ? root.nodeData.length : 0
                    delegate: Rectangle {
                        property int tileValue: (root.nodeData && index < root.nodeData.length) ? root.nodeData[index] : 0
                        width: root.tileSize
                        height: root.tileSize
                        radius: 6
                        border.width: tileValue === 0 ? 0 : 1
                        border.color: "#1d4ed8"
                        color: tileValue === 0 ? "#dbe4f0" : "#2563eb"

                        Text {
                            anchors.centerIn: parent
                            text: tileValue === 0 ? "" : tileValue
                            font.pixelSize: 14
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
            font.pixelSize: 11
            font.bold: true
            color: "#0f172a"
        }
    }
}
