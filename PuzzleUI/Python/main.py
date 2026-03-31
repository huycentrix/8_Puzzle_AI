import os
import sys
from pathlib import Path
from PySide6.QtGui import QGuiApplication, QFontDatabase
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

# --- Bước 1: Fix lỗi Module (algorithms, puzzle, core) ---
# Lùi 3 cấp từ main.py để tìm thư mục gốc 8_Puzzle_AI-1
ROOT_DIR = Path(__file__).parent.parent.parent.absolute()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Sau khi đã thêm ROOT_DIR vào path mới có thể import bridge
from bridge import PuzzleBridge

def main():
    # --- Bước 2: Thiết lập môi trường ---
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_SCALE_FACTOR_ROUNDING_POLICY"] = "PassThrough"
    QQuickStyle.setStyle("Basic")
    
    app = QGuiApplication(sys.argv)
    
    # Thư mục UI (PuzzleUI)
    UI_DIR = Path(__file__).parent.parent.absolute()
    os.environ["QT_QUICK_CONTROLS_CONF"] = str(UI_DIR / "qtquickcontrols2.conf")

    # --- Bước 3: Khởi tạo Bridge và Engine ---
    bridge = PuzzleBridge()
    engine = QQmlApplicationEngine()
    
    # Đăng ký Backend cho QML
    engine.rootContext().setContextProperty("Backend", bridge)
    
    # Load Font
    font_path = UI_DIR / "PuzzleUIContent" / "fonts" / "MaterialIconsOutlined-Regular.otf"
    if font_path.exists():
        QFontDatabase.addApplicationFont(str(font_path))

    # Cung cấp đường dẫn nạp các component QML
    engine.addImportPath(str(UI_DIR))
    engine.addImportPath(str(UI_DIR / "PuzzleUIContent"))

    # --- Bước 4: Load App ---
    main_qml_path = UI_DIR / "PuzzleUIContent" / "App.qml"
    engine.load(str(main_qml_path))

    if not engine.rootObjects():
        sys.exit(-1)
        
    window = engine.rootObjects()[0]
    window.showMaximized()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()