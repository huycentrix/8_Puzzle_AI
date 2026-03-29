import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    visible: true
    width: 1600
    height: 940
    minimumWidth: 1280
    minimumHeight: 760
    title: "8 Puzzle Search Visualizer"
    color: "#f4f7fb"

    property var startState: [1, 2, 3, 4, 0, 5, 7, 8, 6]
    property var goalState: [1, 2, 3, 4, 5, 6, 7, 8, 0]
    property var previewState: startState.slice(0)
    property string statusText: "Ready"
    property string processingTimeText: "0 ms"
    property string pathCostText: "0"
    property string exploredCountText: "0"
    property string frontierPeakText: "0"
    property string solutionDepthText: "0"
    property string currentFrontierText: "0"

    function cloneState(state) { return state.slice(0) }
    function stateId(state) { return state.join(",") }

    function nodeIndexById(nodeId) {
        for (let i = 0; i < nodeModel.count; i += 1) {
            if (nodeModel.get(i).nodeId === nodeId) {
                return i
            }
        }
        return -1
    }

    function edgeExists(parentId, childId) {
        for (let i = 0; i < edgeModel.count; i += 1) {
            const edge = edgeModel.get(i)
            if (edge.parentId === parentId && edge.childId === childId) {
                return true
            }
        }
        return false
    }

    function appendLog(kind, text) {
        logModel.insert(0, {
            kind: kind,
            text: text,
            time: new Date().toLocaleTimeString(Qt.locale(), "hh:mm:ss")
        })
    }

    function resetVisualization() {
        nodeModel.clear()
        edgeModel.clear()
        logModel.clear()
        previewState = cloneState(startState)
        statusText = "Ready"
        processingTimeText = "0 ms"
        pathCostText = "0"
        exploredCountText = "0"
        frontierPeakText = "0"
        solutionDepthText = "0"
        currentFrontierText = "0"
        treeCanvas.requestPaint()
    }

    function upsertNode(nodeInfo) {
        const index = nodeIndexById(nodeInfo.id)
        const payload = {
            nodeId: nodeInfo.id,
            parentId: nodeInfo.parentId,
            flatState: nodeInfo.flatState,
            g: nodeInfo.g,
            h: nodeInfo.h,
            f: nodeInfo.f,
            x: nodeInfo.x,
            y: nodeInfo.y,
            status: nodeInfo.status
        }

        if (index === -1) {
            nodeModel.append(payload)
        } else {
            for (const key in payload) {
                nodeModel.setProperty(index, key, payload[key])
            }
        }

        if (nodeInfo.parentId !== "" && !edgeExists(nodeInfo.parentId, nodeInfo.id)) {
            edgeModel.append({ parentId: nodeInfo.parentId, childId: nodeInfo.id })
        }
        treeCanvas.requestPaint()
    }

    function scrollToNode(nodeInfo) {
        const targetX = Math.max(0, nodeInfo.x - treeView.width * 0.5)
        const targetY = Math.max(0, nodeInfo.y - 120)
        treeView.contentX = Math.min(targetX, Math.max(0, treeView.contentWidth - treeView.width))
        treeView.contentY = Math.min(targetY, Math.max(0, treeView.contentHeight - treeView.height))
    }

    function swapWithZero(index) {
        const zeroIndex = startState.indexOf(0)
        const zr = Math.floor(zeroIndex / 3)
        const zc = zeroIndex % 3
        const tr = Math.floor(index / 3)
        const tc = index % 3
        if (Math.abs(zr - tr) + Math.abs(zc - tc) !== 1) {
            return
        }

        const nextState = cloneState(startState)
        nextState[zeroIndex] = nextState[index]
        nextState[index] = 0
        startState = nextState
        previewState = cloneState(nextState)
    }

    component BoardTile : Rectangle {
        property int value: 0
        property bool editable: false
        property int tileIndex: 0

        radius: 10
        color: value === 0 ? "#dbe4f0" : "#2563eb"
        border.width: value === 0 ? 0 : 1
        border.color: "#1d4ed8"

        Text {
            anchors.centerIn: parent
            text: parent.value === 0 ? "" : parent.value
            font.pixelSize: 26
            font.bold: true
            color: parent.value === 0 ? "transparent" : "#ffffff"
        }

        MouseArea {
            anchors.fill: parent
            enabled: parent.editable
            onClicked: root.swapWithZero(parent.tileIndex)
        }
    }

    component BoardView : Rectangle {
        id: boardView
        property var boardState: []
        property bool editable: false

        width: 220
        height: 220
        radius: 20
        color: "#e9f0fb"
        border.color: "#c8d5ea"

        Grid {
            anchors.centerIn: parent
            columns: 3
            spacing: 8

            Repeater {
                model: 9
                delegate: BoardTile {
                    width: 60
                    height: 60
                    tileIndex: index
                    editable: boardView.editable
                    value: boardView.boardState[index]
                }
            }
        }
    }

    ListModel { id: nodeModel }
    ListModel { id: edgeModel }
    ListModel { id: logModel }

    header: ToolBar {
        contentHeight: 56
        background: Rectangle { color: "#ffffff"; border.color: "#dbe4f0" }
        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 20
            anchors.rightMargin: 20
            Text { text: "8 Puzzle Search Visualizer"; font.pixelSize: 24; font.bold: true; color: "#0f172a" }
            Item { Layout.fillWidth: true }
            Text { text: statusText; font.pixelSize: 14; font.bold: true; color: "#2563eb" }
        }
    }

    RowLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 16

        Rectangle {
            Layout.preferredWidth: 340
            Layout.fillHeight: true
            radius: 18
            color: "#ffffff"
            border.color: "#dbe4f0"

            ScrollView {
                anchors.fill: parent
                anchors.margins: 16
                clip: true

                ColumnLayout {
                    width: 292
                    spacing: 18

                    Text { text: "Configuration"; font.pixelSize: 22; font.bold: true; color: "#0f172a" }
                    Text { text: "Start State"; font.pixelSize: 14; font.bold: true; color: "#334155" }
                    BoardView { Layout.alignment: Qt.AlignHCenter; boardState: root.startState; editable: true }

                    RowLayout {
                        Layout.fillWidth: true
                        Button {
                            Layout.fillWidth: true
                            text: "Randomize"
                            onClicked: {
                                startState = backend.randomize_state(goalState, 60)
                                previewState = cloneState(startState)
                            }
                        }
                        Button {
                            Layout.fillWidth: true
                            text: "Reset"
                            onClicked: {
                                startState = [1, 2, 3, 4, 0, 5, 7, 8, 6]
                                previewState = cloneState(startState)
                            }
                        }
                    }

                    Text { text: "Goal State"; font.pixelSize: 14; font.bold: true; color: "#334155" }
                    BoardView { Layout.alignment: Qt.AlignHCenter; boardState: root.goalState; editable: false }
                    Text { text: "Algorithm"; font.pixelSize: 14; font.bold: true; color: "#334155" }

                    ComboBox {
                        id: algorithmBox
                        Layout.fillWidth: true
                        model: [
                            "A* Search",
                            "Breadth-First Search (BFS)",
                            "Depth-First Search (DFS)",
                            "Uniform Cost Search (UCS)",
                            "Greedy Best-First Search (GBFS)",
                            "Iterative Deepening Search (IDDFS)",
                            "Iterative Deepening A* (IDA*)",
                            "Bidirectional Search"
                        ]
                    }

                    Text { text: "Heuristic"; font.pixelSize: 14; font.bold: true; color: "#334155" }
                    ComboBox {
                        id: heuristicBox
                        Layout.fillWidth: true
                        model: ["Manhattan Distance", "Misplaced Tiles", "Euclidean Distance"]
                        enabled: algorithmBox.currentText.indexOf("A*") !== -1 || algorithmBox.currentText.indexOf("Greedy") !== -1
                    }

                    Text { text: "Playback Speed: " + speedSlider.value.toFixed(1) + "x"; font.pixelSize: 14; font.bold: true; color: "#334155" }
                    Slider {
                        id: speedSlider
                        Layout.fillWidth: true
                        from: 0.5
                        to: 4.0
                        value: 1.5
                        stepSize: 0.1
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        Button {
                            Layout.fillWidth: true
                            text: "Run Search"
                            onClicked: {
                                backend.start_search(algorithmBox.currentText, startState, goalState, speedSlider.value, heuristicBox.currentText)
                            }
                        }
                        Button {
                            Layout.fillWidth: true
                            text: "Stop"
                            onClicked: backend.stop_playback()
                        }
                    }

                    Rectangle { Layout.fillWidth: true; height: 1; color: "#e2e8f0" }
                    Text { text: "Current Preview"; font.pixelSize: 14; font.bold: true; color: "#334155" }
                    BoardView { Layout.alignment: Qt.AlignHCenter; boardState: root.previewState; editable: false }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: 18
            color: "#ffffff"
            border.color: "#dbe4f0"

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 12

                Text { text: "Search Tree"; font.pixelSize: 22; font.bold: true; color: "#0f172a" }

                Flickable {
                    id: treeView
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    contentWidth: 3600
                    contentHeight: 12000
                    boundsBehavior: Flickable.StopAtBounds
                    Behavior on contentX { NumberAnimation { duration: 220; easing.type: Easing.OutCubic } }
                    Behavior on contentY { NumberAnimation { duration: 220; easing.type: Easing.OutCubic } }

                    Item {
                        width: treeView.contentWidth
                        height: treeView.contentHeight

                        Canvas {
                            id: treeCanvas
                            anchors.fill: parent
                            z: 0
                            onPaint: {
                                const ctx = getContext("2d")
                                ctx.reset()
                                ctx.strokeStyle = "#3b82f6"
                                ctx.lineWidth = 2
                                ctx.fillStyle = "#3b82f6"

                                function findNode(nodeId) {
                                    for (let i = 0; i < nodeModel.count; i += 1) {
                                        const node = nodeModel.get(i)
                                        if (node.nodeId === nodeId) {
                                            return node
                                        }
                                    }
                                    return null
                                }

                                for (let i = 0; i < edgeModel.count; i += 1) {
                                    const edge = edgeModel.get(i)
                                    const parentNode = findNode(edge.parentId)
                                    const childNode = findNode(edge.childId)
                                    if (!parentNode || !childNode) {
                                        continue
                                    }

                                    const startX = parentNode.x + 74
                                    const startY = parentNode.y + 148
                                    const endX = childNode.x + 74
                                    const endY = childNode.y

                                    ctx.beginPath()
                                    ctx.moveTo(startX, startY)
                                    ctx.lineTo(endX, endY)
                                    ctx.stroke()

                                    const angle = Math.atan2(endY - startY, endX - startX)
                                    const length = 9
                                    ctx.beginPath()
                                    ctx.moveTo(endX, endY)
                                    ctx.lineTo(endX - length * Math.cos(angle - Math.PI / 6), endY - length * Math.sin(angle - Math.PI / 6))
                                    ctx.lineTo(endX - length * Math.cos(angle + Math.PI / 6), endY - length * Math.sin(angle + Math.PI / 6))
                                    ctx.closePath()
                                    ctx.fill()
                                }
                            }
                        }

                        Repeater {
                            model: nodeModel
                            delegate: PuzzleNode {
                                x: model.x
                                y: model.y
                                z: 1
                                nodeData: model.flatState
                                g: model.g
                                h: model.h
                                f: model.f
                                status: model.status
                                onHovered: root.previewState = state
                            }
                        }
                    }

                    ScrollBar.horizontal: ScrollBar { policy: ScrollBar.AsNeeded }
                    ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }
                }
            }
        }

        Rectangle {
            Layout.preferredWidth: 320
            Layout.fillHeight: true
            radius: 18
            color: "#ffffff"
            border.color: "#dbe4f0"

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 12

                Text { text: "Metrics"; font.pixelSize: 22; font.bold: true; color: "#0f172a" }

                GridLayout {
                    Layout.fillWidth: true
                    columns: 2
                    rowSpacing: 10
                    columnSpacing: 12
                    Text { text: "Time"; font.bold: true; color: "#334155" }
                    Text { text: processingTimeText; color: "#0f172a" }
                    Text { text: "Path Cost"; font.bold: true; color: "#334155" }
                    Text { text: pathCostText; color: "#0f172a" }
                    Text { text: "Explored"; font.bold: true; color: "#334155" }
                    Text { text: exploredCountText; color: "#0f172a" }
                    Text { text: "Frontier Peak"; font.bold: true; color: "#334155" }
                    Text { text: frontierPeakText; color: "#0f172a" }
                    Text { text: "Current Frontier"; font.bold: true; color: "#334155" }
                    Text { text: currentFrontierText; color: "#0f172a" }
                    Text { text: "Solution Depth"; font.bold: true; color: "#334155" }
                    Text { text: solutionDepthText; color: "#0f172a" }
                }

                Rectangle { Layout.fillWidth: true; height: 1; color: "#e2e8f0" }
                Text { text: "Execution Log"; font.pixelSize: 20; font.bold: true; color: "#0f172a" }

                ListView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    spacing: 8
                    clip: true
                    model: logModel

                    delegate: Rectangle {
                        width: ListView.view.width
                        height: 74
                        radius: 12
                        color: index === 0 ? "#eff6ff" : "#f8fafc"
                        border.color: "#dbe4f0"

                        Column {
                            anchors.fill: parent
                            anchors.margins: 12
                            spacing: 4
                            Row {
                                width: parent.width
                                spacing: 8
                                Text { text: model.kind; font.bold: true; color: "#2563eb" }
                                Text { text: model.time; color: "#64748b" }
                            }
                            Text {
                                width: parent.width
                                wrapMode: Text.WordWrap
                                text: model.text
                                color: "#0f172a"
                            }
                        }
                    }
                }
            }
        }
    }

    Component.onCompleted: appendLog("INFO", "Ready to run 8-puzzle search.")

    Connections {
        target: backend

        function onSearchReset() {
            resetVisualization()
            appendLog("INFO", "Visualization reset.")
        }

        function onStepUpdated(stepData) {
            upsertNode(stepData.currentNode)
            for (let i = 0; i < stepData.children.length; i += 1) {
                upsertNode(stepData.children[i])
            }

            previewState = cloneState(stepData.currentNode.flatState)
            exploredCountText = stepData.exploredCount.toString()
            currentFrontierText = stepData.frontierCount.toString()
            statusText = stepData.isGoal ? "Goal found" : "Running"
            appendLog("STEP " + stepData.stepNumber, "Expanded " + stepData.currentNode.id + " and generated " + stepData.children.length + " child nodes.")
            scrollToNode(stepData.currentNode)
        }

        function onSearchFinished(summary) {
            statusText = summary.success ? "Completed" : "No solution"
            processingTimeText = summary.processingTimeMs + " ms"
            pathCostText = summary.pathCost.toString()
            exploredCountText = summary.exploredCount.toString()
            frontierPeakText = summary.frontierPeak.toString()
            solutionDepthText = summary.solutionDepth.toString()

            for (let i = 0; i < summary.pathIds.length; i += 1) {
                const idx = nodeIndexById(summary.pathIds[i])
                if (idx !== -1) {
                    nodeModel.setProperty(idx, "status", "path")
                }
            }

            appendLog(summary.success ? "DONE" : "FAIL", summary.algorithm + " finished in " + summary.processingTimeMs + " ms with explored count " + summary.exploredCount + ".")
            treeCanvas.requestPaint()
        }

        function onSearchError(message) {
            statusText = "Error"
            appendLog("ERROR", message)
        }
    }
}
