// PuzzleNode.qml
import QtQuick

Column {
    id: nodeRoot
    spacing: 8
    property var nodeData: []
    property int f: 0; property int g: 0; property int h: 0
    property string status: "frontier" 

    Rectangle {
        width: 140; height: 140
        color: status === "explored" ? "#bdbdbd" : (status === "path" ? "#fff9c4" : "white") 
        border.color: "#333333"
        border.width: status === "path" ? 3 : 1

        Grid {
            anchors.centerIn: parent
            columns: 3; spacing: 0 // Khít nhau như hình mẫu
            Repeater {
                model: nodeRoot.nodeData
                Rectangle {
                    width: 40; height: 40
                    color: modelData === 0 ? "#e0e0e0" : "transparent"
                    border.color: "#999999"
                    border.width: 1
                    Text {
                        anchors.centerIn: parent
                        text: modelData === 0 ? "" : modelData
                        font.pixelSize: 18; font.weight: Font.Bold
                    }
                }
            }
        }
    }

    // Công thức f = g + h đúng như hình mẫu
    Text {
        anchors.horizontalCenter: parent.horizontalCenter
        text: f + " = " + g + " + " + h
        font.pixelSize: 14; font.weight: Font.Bold
    }
}