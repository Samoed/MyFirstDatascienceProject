import sys

from PySide6.QtWidgets import QApplication

from src.args_parser import get_device
from src.main_window import MainWindow

if __name__ == "__main__":
    device = get_device()
    app = QApplication()

    window = MainWindow("keymap.json", device)
    window.show()

    try:
        sys.exit(app.exec())
    except Exception as e:
        print(e)
