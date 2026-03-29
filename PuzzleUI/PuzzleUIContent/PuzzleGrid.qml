// PuzzleGrid.qml
import QtQuick
import QtQuick.Layouts
import QtQuick.Effects

Item {
    id: puzzleWrapper
    // Kích thước tổng thể mới (390 * 1.2)
    width: 468; height: 468

    property var puzzleModel: [1, 2, 3, 4, 0, 5, 7, 8, 6]

    // Các thông số kích thước đã nhân tỉ lệ 1.2
    readonly property int tileSize: 131 // (109 * 1.2)
    readonly property int spacing: 14   // (12 * 1.2)
    readonly property int padding: 24   // (20 * 1.2)

    function getX(index) { return padding + (index % 3) * (tileSize + spacing) }
    function getY(index) { return padding + Math.floor(index / 3) * (tileSize + spacing) }

    MultiEffect {
        source: gridBackground; anchors.fill: gridBackground
        shadowEnabled: true; shadowBlur: 0.75; shadowColor: "#25000000"
        shadowVerticalOffset: 11 // (9 * 1.2)
    }

    Rectangle {
        id: gridBackground; anchors.fill: parent
        color: "#dde9ff"
        radius: 29 // (24 * 1.2) Bo góc lớn hơn cho khung nền

        Grid {
            anchors.centerIn: parent; columns: 3; spacing: puzzleWrapper.spacing
            Repeater {
                model: 9
                Rectangle {
                    width: puzzleWrapper.tileSize; height: puzzleWrapper.tileSize
                    radius: 18; // (15 * 1.2) Bo góc lớn hơn cho ô trống
                    color: "#40ccdbf4"; border.width: 2; border.color: "#20727783"
                }
            }
        }

        Repeater {
            model: [1, 2, 3, 4, 5, 6, 7, 8]
            delegate: Item {
                width: puzzleWrapper.tileSize; height: puzzleWrapper.tileSize
                readonly property int currentIndex: puzzleWrapper.puzzleModel.indexOf(modelData)
                x: puzzleWrapper.getX(currentIndex); y: puzzleWrapper.getY(currentIndex)

                Behavior on x { NumberAnimation { duration: 300; easing.type: Easing.OutCubic } }
                Behavior on y { NumberAnimation { duration: 300; easing.type: Easing.OutCubic } }

                Rectangle {
                    id: tileRect; anchors.fill: parent
                    radius: 18; // (15 * 1.2) Bo góc lớn hơn cho ô số
                    color: "#005fb8"
                    Text {
                        anchors.centerIn: parent; text: modelData; color: "white"
                        font.family: "Space Grotesk"
                        // Phông chữ lớn hơn (39 * 1.2)
                        font.pixelSize: 47
                        font.weight: Font.Bold
                    }
                }
            }
        }
    }
}
