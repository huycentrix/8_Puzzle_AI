// SidebarButton.qml
import QtQuick
import QtQuick.Controls

Button {
    id: control
    // Nhận mã hex của icon, ví dụ: "\ue871"
    property string iconCode: "\ue871"
    // Nhận tên font family đã load từ bên ngoài
    property bool isActive: true
    property string iconFontName: "Material Icons"

    implicitWidth: 240
    implicitHeight: 48

    contentItem: Row {
        spacing: 12
        leftPadding: 16
        anchors.verticalCenter: parent.verticalCenter

        // Icon Text với Font chuyên biệt
        Text {
            text: control.iconCode
            font.pixelSize: 24 // Size cho icon thường lớn hơn chữ
            color: control.isActive ? "#00488d" : "#0d1c2f"
            opacity: control.isActive ? 1.0 : 0.6 // Giảm opacity cho icon không active
            verticalAlignment: Text.AlignVCenter
            font.family: "Material Icons Outlined"
            horizontalAlignment: Text.AlignHCenter
            width: 24 // Cố định chiều rộng icon để chữ bên cạnh thẳng hàng
        }

        Text {
            text: control.text
            font.family: "Inter, sans-serif" // Font chữ thường
            font.pixelSize: 14
            font.weight: control.isActive ? Font.Bold : Font.Medium
            color: control.isActive ? "#00488d" : "#0d1c2f"
            verticalAlignment: Text.AlignVCenter
        }
    }

    background: Rectangle {
        color: control.isActive ? "#d5e3fd" : (control.hovered ? "#e6eeff" : "transparent")
        radius: 10

        // Đường kẻ xanh bên trái cho nút đang hoạt động
        Rectangle {
            width: 4
            height: parent.height
            anchors.left: parent.left + 10
            anchors.leftMargin: 0
            anchors.verticalCenterOffset: 0
            anchors.verticalCenter: parent.verticalCenter
            color: "#00488d"
            visible: control.isActive
        }
    }
}
