from layout_data import *
from PyQt6.QtWidgets import QPushButton, QMessageBox, QLineEdit, QComboBox
from core import *
from PyQt6.QtCore import pyqtSignal as Signal
from PyQt6.QtCore import pyqtSlot, Qt
from ui_management.UI import *


class RocketsUI(UI):
    changeSignal = Signal()

    def __init__(self, parent):
        super(RocketsUI, self).__init__(ROCKETS_SCREEN_UI, parent=parent)

    def initialize(self):
        self.createRocketButton = self.findChild(
            QPushButton, "createRocketButton")
        self.createRocketButton.clicked.connect(self.createEvent)
        self.closeButton = self.findChild(QPushButton, "closeButton")
        self.closeButton.clicked.connect(self.close)
        self.editRocketButton = self.findChild(QPushButton, "editRocketButton")
        self.editRocketButton.clicked.connect(self.editEvent)
        self.deleteRocketButton = self.findChild(
            QPushButton, "deleteRocketButton")
        self.deleteRocketButton.clicked.connect(self.deleteEvent)
        self.populate()

    def populate(self):
        rocketUnusedCount = getCountRockets(False)
        rocketUsedCount = getCountRockets(True)
        self.rocketsUnusedLabel.setText(str(rocketUnusedCount))
        self.rocketsUsedLabel.setText(str(rocketUsedCount))
        if rocketUnusedCount:
            self.deleteRocketButton.setEnabled(True)
            self.editRocketButton.setEnabled(True)
        else:
            self.editRocketButton.setEnabled(False)
            self.deleteRocketButton.setEnabled(False)

    def createEvent(self):
        self.newUI = RocketNewUI(self)
        self.newUI.newSignal.connect(self.populate)
        self.newUI.newSignal.connect(self.changeSignal.emit)

    def editEvent(self):
        RocketEditUI(self)

    def deleteEvent(self):
        self.deleteUI = RocketDeleteUI(self)
        self.deleteUI.deleteSignal.connect(self.populate)
        self.deleteUI.deleteSignal.connect(self.changeSignal.emit)


class RocketNewUI(UI):
    newSignal = Signal()

    def __init__(self, parent):
        super(RocketNewUI, self).__init__(ROCKET_NEW_UI, parent=parent)

    def initialize(self):
        self.createButton = self.findChild(QPushButton, "createButton")
        self.createButton.clicked.connect(self.createEvent)
        self.nameField = self.findChild(QLineEdit, "nameField")
        self.nameField.textChanged.connect(self.nameFieldEvent)
        self.weightField = self.findChild(QLineEdit, "weightField")
        self.weightField.textChanged.connect(self.weightFieldEvent)

        # Enable flags
        self.hasNameField = False
        self.hasWeightField = False

        self.populate()

    def populate(self):
        if self.hasNameField and self.hasWeightField:
            self.createButton.setEnabled(True)
        else:
            self.createButton.setEnabled(False)

    def nameFieldEvent(self):
        if self.nameField.text():
            self.hasNameField = True
        else:
            self.hasNameField = False
        self.populate()

    def weightFieldEvent(self):
        if self.weightField.text():
            self.hasWeightField = True
        else:
            self.hasWeightField = False
        self.populate()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Return.value and self.hasNameField and self.hasWeightField:
            self.createEvent()
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()

    def createEvent(self):
        result = addRocket(self.nameField.text(), self.weightField.text())
        if result:
            self.newSignal.emit()
            QMessageBox.information(self, "ProjectGamma - Cohete creado",
                                    "Cohete creado con éxito",
                                    buttons=QMessageBox.StandardButton.Ok)
            self.close()
        else:
            QMessageBox.critical(self, "ProjectGamma - Error",
                                 "El peso debe ser un número real positivo",
                                 buttons=QMessageBox.StandardButton.Ok)


class RocketEditUI(UIDialog):
    def __init__(self, parent):
        super(RocketEditUI, self).__init__(ROCKET_EDIT_UI, parent=parent)

    def initialize(self):
        self.editButton = self.findChild(QPushButton, "editButton")
        self.editButton.clicked.connect(self.editEvent)
        self.rocketsChoice = self.findChild(QComboBox, "rocketsChoice")
        self.rocketsChoice.currentTextChanged.connect(self.rocketsChoiceChange)
        self.nameField = self.findChild(QLineEdit, "nameField")
        self.weightField = self.findChild(QLineEdit, "weightField")
        self.rocketActive = 0
        self.oldIndex = 0
        self.rockets = None
        self.populate()

    def populate(self):
        self.rocketsChoice.clear()
        countRockets = getCountRockets(False)
        if countRockets:
            self.rockets = getRockets(False)
            for item in self.rockets:
                self.rocketsChoice.addItem(str(item[1]))
            self.rocketsChoice.setCurrentIndex(self.oldIndex)
            self.refresh()
        else:
            self.rocketsChoice.setEnabled(False)
            self.nameField.setEnabled(False)
            self.weightField.setEnabled(False)
            self.editButton.setEnabled(False)

    def refresh(self):
        self.nameField.setText(self.rockets[self.rocketActive][1])
        self.weightField.setText(str(self.rockets[self.rocketActive][2]))

    def editEvent(self):
        rocketId = self.rockets[self.rocketActive][0]
        result = editRocket(rocketId, self.nameField.text(),
                            self.weightField.text())
        if not result:
            QMessageBox.information(self, "ProjectGamma - Cohete editado",
                                    "Cohete editado con éxito",
                                    buttons=QMessageBox.StandardButton.Ok)
            self.oldIndex = self.rocketActive
            self.populate()
        else:
            QMessageBox.critical(self, "ProjectGamma - Error",
                                 result, buttons=QMessageBox.StandardButton.Ok)

    def rocketsChoiceChange(self):
        self.rocketActive = self.rocketsChoice.currentIndex()
        self.refresh()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Return.value and self.editButton.isEnabled():
            self.editEvent()
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()


class RocketDeleteUI(UI):
    deleteSignal = Signal()

    def __init__(self, parent):
        super(RocketDeleteUI, self).__init__(ROCKET_DELETE_UI, parent=parent)

    def initialize(self):
        self.deleteButton = self.findChild(QPushButton, "deleteButton")
        self.deleteButton.clicked.connect(self.deleteEvent)
        self.rocketsChoice = self.findChild(QComboBox, "rocketsChoice")
        self.rocketsChoice.currentTextChanged.connect(self.rocketsChoiceChange)
        self.rocketActive = 0
        self.oldIndex = 0
        self.rockets = None
        self.populate()

    def populate(self):
        self.rocketsChoice.clear()
        countRockets = getCountRockets(False)
        if countRockets:
            self.rockets = getRockets(False)
            for item in self.rockets:
                self.rocketsChoice.addItem(
                    "Nombre: "+str(item[1])+"\tPeso Máx.: "+str(item[2]))
        else:
            self.rocketsChoice.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def rocketsChoiceChange(self):
        self.oldIndex = self.rocketActive
        self.rocketActive = self.rocketsChoice.currentIndex()

    def deleteEvent(self):
        reply = QMessageBox.warning(self, "ProjectGamma - Borrar cohete",
                                    "¿Estás seguro?",
                                    buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                    )
        if reply == QMessageBox.StandardButton.Yes:
            rocketId = self.rockets[self.rocketActive][0]
            deleteRocket(rocketId)
            self.deleteSignal.emit()
            self.populate()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Return.value:
            self.deleteEvent()
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()
