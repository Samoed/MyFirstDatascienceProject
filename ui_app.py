import sys

from PySide6.QtWidgets import QApplication

from app.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication()

    window = MainWindow("keymap.json")
    window.show()

    try:
        sys.exit(app.exec())
    except Exception as e:
        print(e)
        sys.exit(0)
