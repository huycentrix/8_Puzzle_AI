// TreeView.qml
import QtQuick
import QtQuick.Controls

Flickable {
    id: treeView
    anchors.fill: parent
    contentWidth: 2000; contentHeight: 2000 // Không gian rộng để vẽ nhánh
    clip: true

    // Dùng Canvas để vẽ các mũi tên nối các Node
    Canvas {
        id: lineCanvas
        anchors.fill: parent
        onPaint: {
            var ctx = getContext("2d")
            ctx.strokeStyle = "#3b82f6"
            ctx.lineWidth = 2
            // Logic vẽ đường nối từ tọa độ Node cha đến Node con
        }
    }

    // Nơi chứa các Node được sinh ra
    Item {
        id: nodesContainer
        // Các PuzzleNode sẽ được tạo động (Dynamic) tại đây khi có stepUpdated
    }
}