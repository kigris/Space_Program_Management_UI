from PyQt6.QtWidgets import QDialog, QWidget
from PyQt6.QtCore import Qt
from PyQt6 import uic


class UIDialog(QDialog):
    # Constructor de la interfaz
    def __init__(self, uiFile, parent=None):
        super(UIDialog, self).__init__()
        if parent:
            self.parent = parent

        uic.loadUi(uiFile, self)
        self.initialize()
        self.exec()

    def initialize(self):
        pass


class UI(QWidget):
    # Constructor de la interfaz
    def __init__(self, uiFile, parent=None):
        super(UI, self).__init__()
        if parent:
            self.parent = parent

        uic.loadUi(uiFile, self)
        self.initialize()
        self.show()

    def initialize(self):
        pass

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()
