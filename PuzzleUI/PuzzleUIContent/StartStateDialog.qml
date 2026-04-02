import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: dialogRoot
    modal: true
    focus: true
    width: 420
    padding: 0

    property string titleText: "Edit Start State"
    property var currentState: [1, 2, 3, 4, 0, 5, 7, 8, 6]
    property var defaultState: [1, 2, 3, 4, 0, 5, 7, 8, 6]
    property var goalState: [1, 2, 3, 4, 5, 6, 7, 8, 0]
    property var cellTexts: []
    property var cellErrors: []
    property bool formValid: false
    property string helperText: ""
    signal applied(var state)

    function fillFromState(state) {
        const nextTexts = []
        for (let i = 0; i < 9; i += 1) nextTexts.push(String(state[i]))
        cellTexts = nextTexts
        validateForm()
    }

    function updateCell(index, value) {
        const nextTexts = cellTexts.slice(0)
        nextTexts[index] = value
        cellTexts = nextTexts
        validateForm()
    }

    function validateForm() {
        const nextErrors = [false, false, false, false, false, false, false, false, false]
        const buckets = ({})
        let hasRawError = false

        for (let i = 0; i < 9; i += 1) {
            const raw = (cellTexts[i] || "").trim()
            if (!/^\d$/.test(raw)) {
                nextErrors[i] = true
                hasRawError = true
                continue
            }

            const value = parseInt(raw, 10)
            if (value < 0 || value > 8) {
                nextErrors[i] = true
                hasRawError = true
                continue
            }

            if (!buckets[value]) buckets[value] = []
            buckets[value].push(i)
        }

        let duplicateError = false
        for (const value in buckets) {
            if (buckets[value].length > 1) {
                duplicateError = true
                for (let i = 0; i < buckets[value].length; i += 1) nextErrors[buckets[value][i]] = true
            }
        }

        const uniqueCount = Object.keys(buckets).length
        cellErrors = nextErrors
        formValid = !hasRawError && !duplicateError && uniqueCount === 9

        if (formValid) {
            helperText = "State is valid and ready to apply."
        } else if (duplicateError) {
            helperText = "Each value from 0 to 8 must appear exactly once."
        } else {
            helperText = "Enter digits 0 to 8 with no blanks."
        }
    }

    function applyState() {
        if (!formValid) return
        const parsed = []
        for (let i = 0; i < 9; i += 1) parsed.push(parseInt(cellTexts[i], 10))
        applied(parsed)
        close()
    }

    onOpened: fillFromState(currentState)

    background: Rectangle {
        radius: 18
        color: "#ffffff"
        border.color: "#dbe4f0"
    }

    contentItem: ColumnLayout {
        spacing: 18

        Rectangle {
            Layout.fillWidth: true
            implicitHeight: 72
            radius: 18
            color: "#eff4ff"

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 20
                anchors.rightMargin: 14
                Text {
                    text: dialogRoot.titleText
                    font.pixelSize: 22
                    font.bold: true
                    color: "#0f172a"
                }
                Item { Layout.fillWidth: true }
                ToolButton {
                    text: "x"
                    onClicked: dialogRoot.close()
                }
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            Layout.leftMargin: 20
            Layout.rightMargin: 20
            Layout.bottomMargin: 20
            spacing: 14

            Text {
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
                text: "Enter the 9 values of the board in row-major order. Use 0 for the blank tile."
                color: "#475569"
            }

            GridLayout {
                Layout.alignment: Qt.AlignHCenter
                columns: 3
                rowSpacing: 10
                columnSpacing: 10

                Repeater {
                    model: 9

                    TextField {
                        required property int index
                        Layout.preferredWidth: 88
                        Layout.preferredHeight: 54
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        font.pixelSize: 22
                        font.bold: true
                        text: dialogRoot.cellTexts[index] || ""
                        color: "#0f172a"
                        selectByMouse: true

                        onTextEdited: dialogRoot.updateCell(index, text)

                        background: Rectangle {
                            radius: 12
                            color: dialogRoot.cellErrors[index] ? "#fff1f2" : "#f8fafc"
                            border.width: 2
                            border.color: dialogRoot.cellErrors[index] ? "#ef4444" : "#cbd5e1"
                        }
                    }
                }
            }

            Text {
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
                text: dialogRoot.helperText
                color: dialogRoot.formValid ? "#047857" : "#b91c1c"
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                Button {
                    Layout.fillWidth: true
                    text: "Reset"
                    onClicked: dialogRoot.fillFromState(dialogRoot.defaultState)
                }

                Button {
                    Layout.fillWidth: true
                    text: "Use Goal"
                    onClicked: dialogRoot.fillFromState(dialogRoot.goalState)
                }

                Button {
                    Layout.fillWidth: true
                    text: "Apply"
                    enabled: dialogRoot.formValid
                    onClicked: dialogRoot.applyState()
                }
            }
        }
    }
}
