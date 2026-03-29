import os
import sys
from pathlib import Path
from PySide6.QtGui import QGuiApplication, QFontDatabase
from PySide6.QtQml import QQmlApplicationEngine
from bridge import PuzzleBridge 
from puzzle.puzzle import Puzzle

def main():
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    app = QGuiApplication(sys.argv)
    
    # THÊM DÒNG NÀY ĐỂ FIX LỖI CUSTOMIZATION
    from PySide6.QtQuickControls2 import QQuickStyle
    QQuickStyle.setStyle("Basic") # Hoặc "Material", "Fusion"
    
    # Khởi tạo cầu nối
    py_bridge = PuzzleBridge(Puzzle)

    engine = QQmlApplicationEngine()
    
    # Đăng ký backend cho QML
    engine.rootContext().setContextProperty("backend", py_bridge)
    
    project_root = Path(__file__).parent.absolute()
    engine.addImportPath(str(project_root))
    engine.addImportPath(str(project_root / "PuzzleUIContent"))
    
    main_qml_path = project_root / "PuzzleUI" / "PuzzleUIContent" / "App.qml"
    engine.load(str(main_qml_path))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()