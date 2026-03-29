import os
import sys
from pathlib import Path
from PySide6.QtGui import QGuiApplication, QFontDatabase
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

def main():
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_SCALE_FACTOR_ROUNDING_POLICY"] = "PassThrough"
    
    app = QGuiApplication(sys.argv)
    
    project_root = Path(__file__).parent.parent.absolute()

    os.environ["QT_QUICK_CONTROLS_CONF"] = str(project_root / "qtquickcontrols2.conf")

    engine = QQmlApplicationEngine()
    font_path = project_root / "PuzzleUIContent" / "fonts" / "MaterialIconsOutlined-Regular.otf"
    if font_path.exists():
        QFontDatabase.addApplicationFont(str(font_path))
    engine.addImportPath(str(project_root))
    engine.addImportPath(str(project_root / "PuzzleUIContent"))
    main_qml_path = project_root / "PuzzleUIContent" / "App.qml"
    engine.load(str(main_qml_path))
    root_objects = engine.rootObjects()
    if root_objects:
        window = root_objects[0]
        window.showMaximized()
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()