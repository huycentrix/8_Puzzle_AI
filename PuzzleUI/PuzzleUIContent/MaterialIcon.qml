// MaterialIcon.qml
import QtQuick

Text {
    id: root
    property string iconCode: ""
    text: iconCode

    // Sử dụng tên chính xác của phiên bản Outlined
    font.family: "Material Icons Outlined"

    font.pixelSize: 24
    color: "#0d1c2f"
    horizontalAlignment: Text.AlignHCenter
    verticalAlignment: Text.AlignVCenter
}
