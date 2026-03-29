import QtQuick

Window {
    width: 1440; height: 810; visible: true
    title: "PuzzleArchitect"

    FontLoader {
        id: materialFont
        source: "fonts/MaterialIconsOutlined-Regular.otf"
    }

    Screen01 { anchors.fill: parent }
}
