import QtQuick
import QtQuick.Controls

Button {
    id: control
    property string iconCode: ""
    property bool isActive: false

    implicitWidth: 180; implicitHeight: 48

    contentItem: Row {
        id: contentRow; spacing: 9; anchors.centerIn: parent
        MaterialIcon {
            iconCode: control.iconCode; color: control.isActive ? "#00488d" : "#0d1c2f"
            opacity: control.isActive ? 1.0 : 0.6; anchors.verticalCenter: parent.verticalCenter; font.pixelSize: 18
        }
        Text {
            text: control.text; font.family: "Inter"; font.pixelSize: 11; font.weight: control.isActive ? Font.Bold : Font.Medium
            color: control.isActive ? "#00488d" : "#0d1c2f"; verticalAlignment: Text.AlignVCenter; anchors.verticalCenter: parent.verticalCenter
        }
    }

    background: Rectangle {
        id: bgRect; radius: 5; color: control.isActive ? "#d5e3fd" : (control.hovered ? "#e6eeff" : "transparent")
        Rectangle {
            anchors.left: parent.left; anchors.top: parent.top; anchors.bottom: parent.bottom
            width: parent.radius + 8; color: parent.color; visible: control.isActive || control.hovered
        }
        Rectangle {
            width: 3; height: parent.height; anchors.left: parent.left; color: "#00488d"; visible: control.isActive
        }
    }
}
