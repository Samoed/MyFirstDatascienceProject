from PySide6.QtWidgets import QDialog

from src.ui.dialog import Ui_Dialog


class DialogWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def get_data(self):
        return self.ui.textEdit.toPlainText()

    def set_data(self, data):
        self.ui.textEdit.setText(data)
