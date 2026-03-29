import QtQuick
import QtQuick.Controls

Window {
    id: windowRoot
    width: 1440
    height: 810
    visible: true
    title: "PuzzleArchitect - Search Tree Mode"

    property var nodeMap: ({})
    property var edgeMap: ({})
    property var createdNodes: ({})

    function resetVisualization() {
        for (var nodeId in createdNodes) {
            if (createdNodes[nodeId]) {
                createdNodes[nodeId].destroy()
            }
        }

        nodeMap = ({})
        edgeMap = ({})
        createdNodes = ({})
        mainScreen.nodeMap = nodeMap
        mainScreen.edgeMap = edgeMap
        mainScreen.metrics.totalSteps = "0"
        mainScreen.metrics.nodesExpanded = "0"
        mainScreen.metrics.solutionDepth = "0"
        mainScreen.logList.clearLog()
        mainScreen.treeCanvas.requestPaint()
    }

    function syncCanvas() {
        mainScreen.nodeMap = nodeMap
        mainScreen.edgeMap = edgeMap
        mainScreen.treeCanvas.requestPaint()
    }

    function upsertNode(nodeInfo) {
        nodeMap[nodeInfo.id] = {
            "x": nodeInfo.x,
            "y": nodeInfo.y,
            "pid": nodeInfo.parentId
        }

        var nodeObj = createdNodes[nodeInfo.id]
        if (!nodeObj) {
            var component = Qt.createComponent("PuzzleNode.qml")
            if (component.status !== Component.Ready) {
                return null
            }

            nodeObj = component.createObject(mainScreen.treeContainer, {
                "x": nodeInfo.x - 70,
                "y": nodeInfo.y,
                "nodeData": nodeInfo.flatState,
                "f": nodeInfo.f,
                "g": nodeInfo.g,
                "h": nodeInfo.h,
                "status": nodeInfo.status
            })
            createdNodes[nodeInfo.id] = nodeObj

            let previewState = nodeInfo.flatState.slice(0)
            var mouseArea = Qt.createQmlObject(
                'import QtQuick; MouseArea { anchors.fill: parent; hoverEnabled: true }',
                nodeObj,
                "dynamicMouseArea_" + nodeInfo.id
            )
            mouseArea.entered.connect(function() {
                mainScreen.puzzleBoard.puzzleModel = previewState
            })
        } else {
            nodeObj.x = nodeInfo.x - 70
            nodeObj.y = nodeInfo.y
            nodeObj.nodeData = nodeInfo.flatState
            nodeObj.f = nodeInfo.f
            nodeObj.g = nodeInfo.g
            nodeObj.h = nodeInfo.h
            nodeObj.status = nodeInfo.status
        }

        if (nodeInfo.parentId !== "") {
            edgeMap[nodeInfo.parentId + "->" + nodeInfo.id] = {
                "from": nodeInfo.parentId,
                "to": nodeInfo.id
            }
        }

        syncCanvas()
        return nodeObj
    }

    Screen01 {
        id: mainScreen
        anchors.fill: parent
    }

    Connections {
        target: backend

        function onSearchReset() {
            resetVisualization()
        }

        function onStepUpdated(stepData) {
            upsertNode(stepData.currentNode)

            for (var i = 0; i < stepData.children.length; i++) {
                upsertNode(stepData.children[i])
            }

            var current = stepData.currentNode
            var targetY = Math.max(0, current.y - 120)
            var targetX = Math.max(0, current.x - (mainScreen.treeScrollView.width / 2))
            mainScreen.treeScrollView.contentY = Math.min(
                targetY,
                Math.max(0, mainScreen.treeScrollView.contentHeight - mainScreen.treeScrollView.height)
            )
            mainScreen.treeScrollView.contentX = Math.min(
                targetX,
                Math.max(0, mainScreen.treeScrollView.contentWidth - mainScreen.treeScrollView.width)
            )

            mainScreen.logList.appendLog(
                "STEP " + stepData.stepNumber,
                "Expand " + current.id + " -> " + stepData.children.length + " node ke tiep"
            )
        }

        function onSearchFinished(success, pathIds) {
            if (!success || !pathIds) {
                return
            }

            for (var i = 0; i < pathIds.length; i++) {
                var node = createdNodes[pathIds[i]]
                if (node) {
                    node.status = "path"
                }
            }

            mainScreen.metrics.solutionDepth = Math.max(0, pathIds.length - 1).toString()
            mainScreen.logList.appendLog("SUCCESS", "Goal path highlighted")
        }
    }
}
