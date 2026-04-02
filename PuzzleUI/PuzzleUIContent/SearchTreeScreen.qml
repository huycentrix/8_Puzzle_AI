import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    property string currentMode: "tree"
    signal requestModeChange(string mode)

    color: "#f4f7fb"
    property var startState: [1, 2, 3, 4, 0, 6, 7, 5, 8]
    property var goalState: [1, 2, 3, 4, 5, 6, 7, 8, 0]
    property var previewState: startState.slice(0)
    property string statusText: "Ready"
    property string processingTimeText: "0 ms"
    property string pathCostText: "0"
    property string exploredCountText: "0"
    property string frontierPeakText: "0"
    property string solutionDepthText: "0"
    property string currentFrontierText: "0"
    property string currentNodeId: ""
    property int lastIdaIteration: -1
    property real lastIdaFLimit: -1
    property int lastTreeIteration: -1
    property bool showUnsolvableBanner: false
    property string unsolvableMessage: ""
    property bool currentStateSolvable: true
    property bool leftPanelCollapsed: false
    property bool rightPanelCollapsed: false
    property real leftPanelWidth: 320
    property var nodeLookup: ({})
    property real treeMinX: 1e9
    property real treeMaxX: -1e9
    property real treeMinY: 1e9
    property real treeMaxY: -1e9
    property real treeContentWidth: 5200
    property real treeContentHeight: 12000
    readonly property real treeNodeWidth: 84
    readonly property real treeNodeHeight: 106

    function cloneState(state) { return state.slice(0) }
    function refreshSolvableStatus() { currentStateSolvable = Backend.is_solvable_state(startState, goalState) }
    function nodeIndexById(nodeId) {
        for (let i = 0; i < nodeModel.count; i += 1) {
            if (nodeModel.get(i).nodeId === nodeId) return i
        }
        return -1
    }
    function edgeExists(parentId, childId) {
        for (let i = 0; i < edgeModel.count; i += 1) {
            const edge = edgeModel.get(i)
            if (edge.parentId === parentId && edge.childId === childId) return true
        }
        return false
    }
    function appendLog(kind, text) {
        logModel.insert(0, { kind: kind, text: text, time: new Date().toLocaleTimeString(Qt.locale(), "hh:mm:ss") })
    }
    function resetVisualization() {
        resetTreeScene()
        logModel.clear()
        showUnsolvableBanner = false
        unsolvableMessage = ""
        previewState = cloneState(startState)
        refreshSolvableStatus()
        statusText = "Ready"
        processingTimeText = "0 ms"
        pathCostText = "0"
        exploredCountText = "0"
        frontierPeakText = "0"
        solutionDepthText = "0"
        currentFrontierText = "0"
    }
    function resetTreeScene() {
        nodeModel.clear()
        edgeModel.clear()
        nodeLookup = ({})
        treeMinX = 1e9
        treeMaxX = -1e9
        treeMinY = 1e9
        treeMaxY = -1e9
        treeContentWidth = 5200
        treeContentHeight = 12000
        currentNodeId = ""
        lastIdaIteration = -1
        lastIdaFLimit = -1
        lastTreeIteration = -1
        treeCanvas.requestPaint()
    }
    function updateTreeBounds(nodeInfo) {
        treeMinX = Math.min(treeMinX, nodeInfo.x)
        treeMaxX = Math.max(treeMaxX, nodeInfo.x + treeNodeWidth)
        treeMinY = Math.min(treeMinY, nodeInfo.y)
        treeMaxY = Math.max(treeMaxY, nodeInfo.y + treeNodeHeight)
        treeContentWidth = Math.max(5200, treeMaxX + 220)
        treeContentHeight = Math.max(2200, treeMaxY + 220)
    }
    function upsertNode(nodeInfo) {
        const index = nodeIndexById(nodeInfo.id)
        const parentId = index === -1 ? nodeInfo.parentId : nodeModel.get(index).parentId
        const payload = {
            nodeId: nodeInfo.id,
            parentId: parentId,
            stateKey: nodeInfo.stateKey,
            flatStateJson: JSON.stringify(nodeInfo.flatState),
            nodeG: nodeInfo.g,
            nodeH: nodeInfo.h,
            nodeF: nodeInfo.f,
            nodeX: nodeInfo.x,
            nodeY: nodeInfo.y,
            nodeStatus: nodeInfo.status
        }
        nodeLookup[nodeInfo.id] = payload
        updateTreeBounds(nodeInfo)
        if (index === -1) nodeModel.append(payload)
        else for (const key in payload) nodeModel.setProperty(index, key, payload[key])
        if (nodeInfo.parentId !== "" && !edgeExists(nodeInfo.parentId, nodeInfo.id)) edgeModel.append({ parentId: nodeInfo.parentId, childId: nodeInfo.id })
    }
    function fitTreeToViewport() {
        if (treeMaxX < treeMinX || treeMaxY < treeMinY) return
        const contentMaxX = Math.max(0, treeContentWidth - treeView.width)
        const contentMaxY = Math.max(0, treeContentHeight - treeView.height)
        const rootNode = nodeModel.count > 0 ? nodeModel.get(0) : null
        const focusX = rootNode ? rootNode.nodeX + treeNodeWidth / 2 : (treeMinX + treeMaxX) * 0.5
        const targetX = Math.max(0, Math.min(focusX - treeView.width * 0.5, contentMaxX))
        const targetY = 0
        treeView.contentX = targetX
        treeView.contentY = targetY
    }
    function swapWithZero(index) {
        const zeroIndex = startState.indexOf(0)
        const zr = Math.floor(zeroIndex / 3)
        const zc = zeroIndex % 3
        const tr = Math.floor(index / 3)
        const tc = index % 3
        if (Math.abs(zr - tr) + Math.abs(zc - tc) !== 1) return
        const nextState = cloneState(startState)
        nextState[zeroIndex] = nextState[index]
        nextState[index] = 0
        startState = nextState
        previewState = cloneState(nextState)
        refreshSolvableStatus()
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

    RowLayout {
        anchors.fill: parent
        spacing: 0

        Rectangle {
            Layout.preferredWidth: 210
            Layout.minimumWidth: 210
            Layout.fillHeight: true
            color: "#eff4ff"

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 19
                spacing: 8

                SideButton {
                    Layout.fillWidth: true
                    text: "Puzzle Setup"
                    iconCode: "\uf1b4"
                    isActive: root.currentMode === "animation"
                    onClicked: root.requestModeChange("animation")
                }

                SideButton {
                    Layout.fillWidth: true
                    text: "Search Tree"
                    iconCode: "\ue037"
                    isActive: root.currentMode === "tree"
                    onClicked: root.requestModeChange("tree")
                }

                Item { Layout.fillHeight: true }
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.margins: 16
            spacing: 16

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 56
                radius: 18
                color: "#ffffff"
                border.color: "#dbe4f0"

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
                Layout.fillWidth: true
                Layout.fillHeight: true
                spacing: 16

                Rectangle {
                    Layout.preferredWidth: root.leftPanelCollapsed ? 44 : root.leftPanelWidth
                    Layout.fillHeight: true
                    radius: 18
                    color: "#ffffff"
                    border.color: "#dbe4f0"
                    Behavior on Layout.preferredWidth { NumberAnimation { duration: 180; easing.type: Easing.OutCubic } }

                    Item {
                        anchors.fill: parent

                        ToolButton {
                            anchors.top: parent.top
                            anchors.right: parent.right
                            anchors.margins: 10
                            text: root.leftPanelCollapsed ? ">" : "<"
                            onClicked: root.leftPanelCollapsed = !root.leftPanelCollapsed
                        }

                        ScrollView {
                            id: leftScroll
                            anchors.fill: parent
                            anchors.margins: 16
                            anchors.topMargin: 42
                            clip: true
                            visible: !root.leftPanelCollapsed

                            ColumnLayout {
                                width: Math.max(0, leftScroll.availableWidth - 8)
                                spacing: 18

                                Text { text: "Configuration"; font.pixelSize: 22; font.bold: true; color: "#0f172a" }

                                Rectangle {
                                    Layout.fillWidth: true
                                    radius: 12
                                    color: currentStateSolvable ? "#ecfdf5" : "#fff1f2"
                                    border.color: currentStateSolvable ? "#10b981" : "#ef4444"
                                    implicitHeight: 54

                                    RowLayout {
                                        anchors.fill: parent
                                        anchors.leftMargin: 12
                                        anchors.rightMargin: 12
                                        spacing: 10
                                        Rectangle { width: 10; height: 10; radius: 5; color: currentStateSolvable ? "#10b981" : "#ef4444" }
                                        ColumnLayout {
                                            spacing: 2
                                            Text { text: currentStateSolvable ? "Solvable" : "Unsolvable"; font.pixelSize: 14; font.bold: true; color: currentStateSolvable ? "#065f46" : "#b91c1c" }
                                            Text { text: currentStateSolvable ? "This initial state can reach the goal." : "This initial state cannot reach the goal."; font.pixelSize: 12; color: currentStateSolvable ? "#047857" : "#7f1d1d" }
                                        }
                                    }
                                }

                                Rectangle {
                                    Layout.fillWidth: true
                                    visible: showUnsolvableBanner
                                    color: "#fff1f2"
                                    border.color: "#ef4444"
                                    radius: 12
                                    implicitHeight: bannerColumn.implicitHeight + 20

                                    ColumnLayout {
                                        id: bannerColumn
                                        anchors.fill: parent
                                        anchors.margins: 10
                                        spacing: 8
                                        Text { text: "Unsolvable Problem"; font.pixelSize: 14; font.bold: true; color: "#b91c1c" }
                                        Text { Layout.fillWidth: true; wrapMode: Text.WordWrap; text: unsolvableMessage; color: "#7f1d1d" }
                                        Button {
                                            text: "Randomize New State"
                                            onClicked: {
                                                startState = Backend.randomize_state(goalState, 60)
                                                previewState = cloneState(startState)
                                                refreshSolvableStatus()
                                                showUnsolvableBanner = false
                                                unsolvableMessage = ""
                                                statusText = "Ready"
                                            }
                                        }
                                    }
                                }

                                Text { text: "Start State"; font.pixelSize: 14; font.bold: true; color: "#334155" }
                                BoardView { Layout.alignment: Qt.AlignHCenter; boardState: root.startState; editable: true }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Button {
                                        Layout.fillWidth: true
                                        text: "Randomize"
                                        onClicked: {
                                            startState = Backend.randomize_state(goalState, 60)
                                            previewState = cloneState(startState)
                                            refreshSolvableStatus()
                                            showUnsolvableBanner = false
                                            unsolvableMessage = ""
                                            statusText = "Ready"
                                        }
                                    }
                                    Button {
                                        Layout.fillWidth: true
                                        text: "Reset"
                                        onClicked: {
                                            startState = [1, 2, 3, 4, 0, 5, 7, 8, 6]
                                            previewState = cloneState(startState)
                                            refreshSolvableStatus()
                                            showUnsolvableBanner = false
                                            unsolvableMessage = ""
                                            statusText = "Ready"
                                        }
                                    }
                                }

                                Text { text: "Goal State"; font.pixelSize: 14; font.bold: true; color: "#334155" }
                                BoardView { Layout.alignment: Qt.AlignHCenter; boardState: root.goalState; editable: false }
                                Text { text: "Algorithm"; font.pixelSize: 14; font.bold: true; color: "#334155" }

                                ComboBox {
                                    id: algorithmBox
                                    Layout.fillWidth: true
                                    model: ["A* Search", "Breadth-First Search", "Depth-First Search", "Uniform Cost Search", "Greedy Search", "IDDFS", "IDA* Search", "Bidirectional Search"]
                                }

                                Text { text: "Heuristic"; font.pixelSize: 14; font.bold: true; color: "#334155" }
                                ComboBox {
                                    id: heuristicBox
                                    Layout.fillWidth: true
                                    model: ["Manhattan Distance", "Misplaced Tiles", "Euclidean Distance"]
                                    enabled: algorithmBox.currentText.indexOf("A*") !== -1 || algorithmBox.currentText.indexOf("Greedy") !== -1
                                }

                                Text { text: "Playback Speed: " + speedSlider.value.toFixed(1) + "x"; font.pixelSize: 14; font.bold: true; color: "#334155" }
                                Slider { id: speedSlider; Layout.fillWidth: true; from: 0.5; to: 4.0; value: 1.5; stepSize: 0.1 }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Button { Layout.fillWidth: true; text: "Run Search"; enabled: currentStateSolvable; onClicked: Backend.start_search(algorithmBox.currentText, startState, goalState, speedSlider.value, heuristicBox.currentText) }
                                    Button { Layout.fillWidth: true; text: "Stop"; onClicked: Backend.stop_playback() }
                                }

                                Rectangle { Layout.fillWidth: true; height: 1; color: "#e2e8f0" }
                                Text { text: "Current Preview"; font.pixelSize: 14; font.bold: true; color: "#334155" }
                                BoardView { Layout.alignment: Qt.AlignHCenter; boardState: root.previewState; editable: false }
                            }
                        }

                        Rectangle {
                            visible: !root.leftPanelCollapsed
                            anchors.top: parent.top
                            anchors.bottom: parent.bottom
                            anchors.right: parent.right
                            width: 10
                            color: dragArea.containsMouse || dragArea.pressed ? "#dbeafe" : "transparent"

                            MouseArea {
                                id: dragArea
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.SizeHorCursor
                                property real startMouseX: 0
                                property real startWidth: 0

                                onPressed: function(mouse) {
                                    startMouseX = mouse.x
                                    startWidth = root.leftPanelWidth
                                }

                                onPositionChanged: function(mouse) {
                                    if (!pressed) return
                                    const delta = mouse.x - startMouseX
                                    root.leftPanelWidth = Math.max(280, Math.min(460, startWidth + delta))
                                }
                            }
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
                            contentWidth: root.treeContentWidth
                            contentHeight: root.treeContentHeight
                            boundsBehavior: Flickable.StopAtBounds

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

                                        for (let i = 0; i < edgeModel.count; i += 1) {
                                            const edge = edgeModel.get(i)
                                            const parentNode = root.nodeLookup[edge.parentId]
                                            const childNode = root.nodeLookup[edge.childId]
                                            if (!parentNode || !childNode) continue
                                            const startX = parentNode.nodeX + root.treeNodeWidth / 2
                                            const startY = parentNode.nodeY + root.treeNodeHeight
                                            const endX = childNode.nodeX + root.treeNodeWidth / 2
                                            const endY = childNode.nodeY

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
                                        x: nodeX
                                        y: nodeY
                                        z: 1
                                        nodeData: JSON.parse(flatStateJson)
                                        g: nodeG
                                        h: nodeH
                                        f: nodeF
                                        status: nodeStatus
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
                    Layout.preferredWidth: root.rightPanelCollapsed ? 44 : 280
                    Layout.fillHeight: true
                    radius: 18
                    color: "#ffffff"
                    border.color: "#dbe4f0"
                    Behavior on Layout.preferredWidth { NumberAnimation { duration: 180; easing.type: Easing.OutCubic } }

                    Item {
                        anchors.fill: parent

                        ToolButton {
                            anchors.top: parent.top
                            anchors.left: parent.left
                            anchors.margins: 10
                            text: root.rightPanelCollapsed ? "<" : ">"
                            onClicked: root.rightPanelCollapsed = !root.rightPanelCollapsed
                        }

                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: 16
                            anchors.topMargin: 42
                            spacing: 12
                            visible: !root.rightPanelCollapsed
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
                                        Row { width: parent.width; spacing: 8
                                            Text { text: model.kind; font.bold: true; color: "#2563eb" }
                                            Text { text: model.time; color: "#64748b" }
                                        }
                                        Text { width: parent.width; wrapMode: Text.WordWrap; text: model.text; color: "#0f172a" }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    Component.onCompleted: {
        appendLog("INFO", "Ready to run 8-puzzle search.")
        refreshSolvableStatus()
    }

    Connections {
        target: Backend

        function onSearchReset() {
            resetVisualization()
            appendLog("INFO", "Visualization reset.")
        }

        function onStepUpdated(stepData) {
            const isIterativeAlgorithm = algorithmBox.currentText === "IDDFS" || algorithmBox.currentText === "IDA* Search"
            if (isIterativeAlgorithm && stepData.meta.iteration !== undefined && stepData.meta.iteration !== root.lastTreeIteration) {
                if (root.lastTreeIteration !== -1) {
                    appendLog("ITERATION", algorithmBox.currentText + " moved to iteration " + stepData.meta.iteration + ".")
                }
                root.resetTreeScene()
                root.lastTreeIteration = stepData.meta.iteration
            }

            if (currentNodeId !== "") {
                const previousIndex = nodeIndexById(currentNodeId)
                if (previousIndex !== -1 && nodeModel.get(previousIndex).nodeStatus === "current") {
                    nodeModel.setProperty(previousIndex, "nodeStatus", "explored")
                }
            }

            stepData.currentNode.status = "current"
            upsertNode(stepData.currentNode)
            for (let i = 0; i < stepData.children.length; i += 1) upsertNode(stepData.children[i])

            currentNodeId = stepData.currentNode.id
            previewState = cloneState(stepData.currentNode.flatState)
            exploredCountText = stepData.exploredCount.toString()
            currentFrontierText = stepData.frontierCount.toString()
            statusText = stepData.isGoal ? "Goal found" : "Running"

            if (algorithmBox.currentText === "IDA* Search") {
                if (stepData.meta.iteration !== lastIdaIteration) {
                    if (lastIdaIteration !== -1) appendLog("IDA*", "Update f_limit: " + lastIdaFLimit + " -> " + stepData.meta.fLimit)
                    lastIdaIteration = stepData.meta.iteration
                    lastIdaFLimit = stepData.meta.fLimit
                    appendLog("IDA* LOOP", "Iteration " + stepData.meta.iteration + " with f_limit = " + stepData.meta.fLimit)
                }
                appendLog("STEP " + stepData.stepNumber, "Expand " + stepData.currentNode.id + " with f=" + stepData.currentNode.f + ", g=" + stepData.currentNode.g + ", h=" + stepData.currentNode.h + ", f_limit=" + stepData.meta.fLimit)
            } else {
                appendLog("STEP " + stepData.stepNumber, "Expanded " + stepData.currentNode.id + " and generated " + stepData.children.length + " child nodes.")
            }
            treeCanvas.requestPaint()
        }

        function onSearchFinished(summary) {
            statusText = summary.success ? "Completed" : "No solution"
            processingTimeText = summary.processingTimeMs + " ms"
            pathCostText = summary.pathCost.toString()
            exploredCountText = summary.exploredCount.toString()
            frontierPeakText = summary.frontierPeak.toString()
            solutionDepthText = summary.solutionDepth.toString()
            const pathStateKeys = ({})
            for (let i = 0; i < summary.pathIds.length; i += 1) pathStateKeys[summary.pathIds[i]] = true
            for (let i = 0; i < summary.pathIds.length; i += 1) {
                const idx = nodeIndexById(summary.pathIds[i])
                if (idx !== -1) nodeModel.setProperty(idx, "nodeStatus", "path")
            }
            for (let i = 0; i < nodeModel.count; i += 1) {
                if (pathStateKeys[nodeModel.get(i).stateKey]) nodeModel.setProperty(i, "nodeStatus", "path")
            }
            appendLog(summary.success ? "DONE" : "FAIL", summary.algorithm + " finished in " + summary.processingTimeMs + " ms with explored count " + summary.exploredCount + ".")
            if (summary.renderTruncated) appendLog("INFO", "Tree view was limited to " + summary.visualizedStepCount + " rendered steps to keep the UI responsive.")
            treeCanvas.requestPaint()
            fitTreeToViewport()
        }

        function onSearchError(message) {
            statusText = "Error"
            showUnsolvableBanner = true
            unsolvableMessage = message + " Please randomize a new initial state or edit the board."
            appendLog("ERROR", message)
        }
    }
}
