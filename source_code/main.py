import sys
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtGui
from ui_management.MainUI import LoginUI

# Command to build .exe
# pyinstaller --onefile --windowed --path= .\main.py

# App principal
app = QApplication(sys.argv)  # se crea la aplicación
window = LoginUI()  # se abre la ventana de login
app.setWindowIcon(QtGui.QIcon('icon.png'))  # se setea icono
sys.exit(app.exec())  # se ejecuta la app
