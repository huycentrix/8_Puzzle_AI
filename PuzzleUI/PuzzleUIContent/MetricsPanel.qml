import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root; Layout.fillWidth: true; implicitHeight: 285; radius: 12; color: "#eff4ff"

    ColumnLayout {
        anchors.fill: parent; anchors.margins: 18; spacing: 0
        Text {
            text: "Metrics Ledger"; font.family: "Space Grotesk"; font.pixelSize: 17; font.weight: Font.Bold; color: "#0d1c2f"
            Layout.bottomMargin: 18
        }

        // Hàng 1: TOTAL STEPS
        RowLayout {
            Layout.fillWidth: true
            Column {
                spacing: 3
                Text { text: "TOTAL STEPS"; font.family: "Manrope"; font.pixelSize: 8; font.weight: Font.Bold; color: "#727783" }
                Text { text: "124"; font.family: "Space Grotesk"; font.pixelSize: 26; font.weight: Font.Bold; color: "#00488d" }
            }
            Item { Layout.fillWidth: true }
            MaterialIcon { iconCode: "\ueb45"; color: "#00488d"; opacity: 0.4; font.pixelSize: 21 }
        }

        Rectangle { Layout.fillWidth: true; height: 1; color: "#00488d"; opacity: 0.08; Layout.topMargin: 12; Layout.bottomMargin: 12 }

        // Hàng 2: NODES EXPANDED
        RowLayout {
            Layout.fillWidth: true
            Column {
                spacing: 3
                Text { text: "NODES EXPANDED"; font.family: "Manrope"; font.pixelSize: 8; font.weight: Font.Bold; color: "#727783" }
                Text { text: "1,892"; font.family: "Space Grotesk"; font.pixelSize: 26; font.weight: Font.Bold; color: "#00488d" }
            }
            Item { Layout.fillWidth: true }
            MaterialIcon { iconCode: "\ueade"; color: "#00488d"; opacity: 0.4; font.pixelSize: 21 }
        }

        Rectangle { Layout.fillWidth: true; height: 1; color: "#00488d"; opacity: 0.08; Layout.topMargin: 12; Layout.bottomMargin: 12 }

        // Hàng 3: SOLUTION DEPTH
        RowLayout {
            Layout.fillWidth: true
            Column {
                spacing: 3
                Text { text: "SOLUTION DEPTH"; font.family: "Manrope"; font.pixelSize: 8; font.weight: Font.Bold; color: "#727783" }
                Text { text: "18"; font.family: "Space Grotesk"; font.pixelSize: 26; font.weight: Font.Bold; color: "#00488d" }
            }
            Item { Layout.fillWidth: true }
            MaterialIcon { iconCode: "\ue53b"; color: "#00488d"; opacity: 0.4; font.pixelSize: 21 }
        }
        Item { Layout.fillHeight: true }
    }
}
