import QtQuick

Window {
    id: root
    width: 1600
    height: 940
    visible: true
    minimumWidth: 1280
    minimumHeight: 760
    title: "PuzzleArchitect"

    FontLoader {
        id: materialFont
        source: "fonts/MaterialIconsOutlined-Regular.otf"
    }

    property string currentMode: "animation"

    Loader {
        anchors.fill: parent
        sourceComponent: root.currentMode === "tree" ? treeMode : animationMode
    }

    Component {
        id: animationMode
        AnimationScreen {
            anchors.fill: parent
            currentMode: root.currentMode
            onRequestModeChange: function(mode) { root.currentMode = mode }
        }
    }

    Component {
        id: treeMode
        SearchTreeScreen {
            anchors.fill: parent
            currentMode: root.currentMode
            onRequestModeChange: function(mode) { root.currentMode = mode }
        }
    }
}
