import os
import sys
from pathlib import Path

from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

from bridge import PuzzleBridge
from puzzle.puzzle import Puzzle


def print_qml_warnings(warnings):
    for warning in warnings:
        print(warning.toString(), file=sys.stderr)


def main():
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.warnings.connect(print_qml_warnings)

    backend = PuzzleBridge(Puzzle)
    engine.rootContext().setContextProperty("backend", backend)

    project_root = Path(__file__).parent.absolute()
    engine.addImportPath(str(project_root))
    engine.addImportPath(str(project_root / "PuzzleUI"))
    engine.addImportPath(str(project_root / "PuzzleUI" / "PuzzleUIContent"))

    app_qml = project_root / "PuzzleUI" / "PuzzleUIContent" / "App.qml"
    engine.load(str(app_qml))

    if not engine.rootObjects():
        return -1

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
