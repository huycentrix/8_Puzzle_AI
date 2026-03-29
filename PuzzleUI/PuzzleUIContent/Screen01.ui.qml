import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Rectangle {
    id: screen
    property alias configPanel: configPanelId
    property alias treeContainer: treeContent
    property alias treeScrollView: treeScrollView
    property alias treeCanvas: treeCanvas
    property alias metrics: metricsPanel
    property alias logList: executionLog
    property alias puzzleBoard: puzzleBoardId
    property var nodeMap: ({})
    property var edgeMap: ({})

    width: 1440
    height: 810
    color: "#ffffff"

    RowLayout {
        anchors.fill: parent
        spacing: 0

        ColumnLayout {
            Layout.preferredWidth: 300
            Layout.fillHeight: true
            Layout.margins: 20

            ConfigPanel { id: configPanelId; Layout.fillWidth: true }
            PuzzleGrid {
                id: puzzleBoardId
                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 16
                Layout.bottomMargin: 16
                scale: 0.52
            }
            MetricsPanel { id: metricsPanel; Layout.fillWidth: true }
            Item { Layout.fillHeight: true }
        }

        ScrollView {
            id: treeScrollView
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            ScrollBar.horizontal.policy: ScrollBar.AsNeeded
            ScrollBar.vertical.policy: ScrollBar.AsNeeded

            Item {
                id: treeContent
                width: 8000
                height: 8000

                Canvas {
                    id: treeCanvas
                    anchors.fill: parent
                    z: -1
                    onPaint: {
                        var ctx = getContext("2d")
                        ctx.reset()
                        ctx.strokeStyle = "#2563eb"
                        ctx.lineWidth = 2
                        ctx.fillStyle = "#2563eb"

                        for (var edgeId in screen.edgeMap) {
                            var edge = screen.edgeMap[edgeId]
                            var fromNode = screen.nodeMap[edge.from]
                            var toNode = screen.nodeMap[edge.to]
                            if (!fromNode || !toNode) {
                                continue
                            }

                            var startX = fromNode.x
                            var startY = fromNode.y + 165
                            var endX = toNode.x
                            var endY = toNode.y - 6

                            ctx.beginPath()
                            ctx.moveTo(startX, startY)
                            ctx.lineTo(endX, endY)
                            ctx.stroke()

                            var angle = Math.atan2(endY - startY, endX - startX)
                            var arrowLength = 10
                            ctx.beginPath()
                            ctx.moveTo(endX, endY)
                            ctx.lineTo(
                                endX - arrowLength * Math.cos(angle - Math.PI / 6),
                                endY - arrowLength * Math.sin(angle - Math.PI / 6)
                            )
                            ctx.lineTo(
                                endX - arrowLength * Math.cos(angle + Math.PI / 6),
                                endY - arrowLength * Math.sin(angle + Math.PI / 6)
                            )
                            ctx.closePath()
                            ctx.fill()
                        }
                    }
                }
            }
        }

        LogList {
            id: executionLog
            Layout.preferredWidth: 300
            Layout.fillHeight: true
        }
    }

    ControlPanel {
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 20
        z: 10
    }
}
