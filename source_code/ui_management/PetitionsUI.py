from venv import create
from layout_data import *
from PyQt6.QtWidgets import QLabel, QPushButton, QMessageBox, QLineEdit, QDialog, QComboBox, QWidget
from PyQt6 import uic, QtCore
from core import *
from PyQt6.QtCore import pyqtSignal as Signal
from ui_management.UI import *


class PetitionsUI(UI):
    changeSignal = Signal()

    def __init__(self, parent):
        super(PetitionsUI, self).__init__(PETITION_SCREEN_UI, parent=parent)

    def initialize(self):
        self.closeButton.clicked.connect(self.close)
        self.createPetitionButton.clicked.connect(self.createEvent)
        self.editPetitionButton.clicked.connect(self.editEvent)
        self.deletePetitionButton.clicked.connect(self.deleteEvent)
        self.populate()

    def populate(self):
        petitionsUnassignedCount = getCountPetitions(assigned=False)
        petitionsAssignedCount = getCountPetitions(assigned=True)
        self.petitionsUnassignedLabel.setText(str(petitionsUnassignedCount))
        self.petitionsAssignedLabel.setText(str(petitionsAssignedCount))
        if petitionsUnassignedCount:
            self.editPetitionButton.setEnabled(True)
            self.deletePetitionButton.setEnabled(True)
        else:
            self.editPetitionButton.setEnabled(False)
            self.deletePetitionButton.setEnabled(False)

    def createEvent(self):
        self.createUI = PetitionNewUI(self)
        self.createUI.newSignal.connect(self.populate)
        self.createUI.newSignal.connect(self.changeSignal.emit)

    def editEvent(self):
        PetitionEditUI(self)

    def deleteEvent(self):
        self.deleteUI = PetitionDeleteUI(self)
        self.deleteUI.deleteSignal.connect(self.populate)
        self.deleteUI.deleteSignal.connect(self.changeSignal.emit)


class PetitionNewUI(UI):
    newSignal = Signal()

    def __init__(self, parent):
        super(PetitionNewUI, self).__init__(PETITION_NEW_UI, parent=parent)

    def initialize(self):
        self.createButton.clicked.connect(self.createEvent)
        self.idField.textChanged.connect(self.idFieldEvent)
        self.descField.textChanged.connect(self.descFieldEvent)
        self.weightField.textChanged.connect(self.weightFieldEvent)
        self.daysField.textChanged.connect(self.daysFieldEvent)

        # Enable flags
        self.hasIdField = False
        self.hasDaysField = False
        self.hasWeightField = False
        self.hasDescField = False

        self.populate()

    def populate(self):
        if self.hasDaysField and self.hasIdField and self.hasDescField and self.hasWeightField:
            self.createButton.setEnabled(True)
        else:
            self.createButton.setEnabled(False)

    def createEvent(self):
        result = addPetition(self.idField.text(), self.descField.text(
        ), self.weightField.text(), self.daysField.text())
        if not result:
            self.newSignal.emit()
            QMessageBox.information(self, "ProjectGamma - Petición creada",
                                    "Petición creada con éxito",
                                    buttons=QMessageBox.StandardButton.Ok)
            self.close()
        else:
            QMessageBox.critical(self, "ProjectGamma - Error",
                                 result, buttons=QMessageBox.StandardButton.Ok)

    def idFieldEvent(self):
        if self.idField.text():
            self.hasIdField = True
        else:
            self.hasIdField = False
        self.populate()

    def daysFieldEvent(self):
        if self.daysField.text():
            self.hasDaysField = True
        else:
            self.hasDaysField = False
        self.populate()

    def weightFieldEvent(self):
        if self.weightField.text():
            self.hasWeightField = True
        else:
            self.hasWeightField = False
        self.populate()

    def descFieldEvent(self):
        if self.descField.text():
            self.hasDescField = True
        else:
            self.hasDescField = False
        self.populate()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Return.value and self.createButton.isEnabled():
            self.createEvent()
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()


class PetitionEditUI(UIDialog):
    def __init__(self, parent):
        super(PetitionEditUI, self).__init__(PETITION_EDIT_UI, parent=parent)

    def initialize(self):
        self.editButton.clicked.connect(self.editEvent)
        self.petitionChoice.currentTextChanged.connect(
            self.petitionChoiceChange)
        self.idField.textChanged.connect(self.idFieldEvent)
        self.descField.textChanged.connect(self.descFieldEvent)
        self.weightField.textChanged.connect(self.weightFieldEvent)
        self.daysField.textChanged.connect(self.daysFieldEvent)
        self.petitionActive = 0
        self.oldPetitionIndex = 0
        self.petitions = None
        self.getCountPetitions = getCountPetitions(assigned=False)

        # Enable flags
        self.hasIdField = False
        self.hasDaysField = False
        self.hasWeightField = False
        self.hasDescField = False
        self.populate()

    def populate(self):
        self.petitionChoice.clear()
        if self.getCountPetitions:
            self.petitions = getPetitions(assigned=False)
            for item in self.petitions:
                self.petitionChoice.addItem(str(item[1]))
            self.petitionChoice.setCurrentIndex(self.oldPetitionIndex)
            self.refresh()

    def checkInputs(self):
        if self.hasIdField and self.hasDaysField and self.hasWeightField and self.hasDescField:
            self.editButton.setEnabled(True)
        else:
            self.editButton.setEnabled(False)

    def refresh(self):
        self.idField.setText(self.petitions[self.petitionActive][1])
        self.descField.setText(self.petitions[self.petitionActive][2])
        self.weightField.setText(str(self.petitions[self.petitionActive][3]))
        self.daysField.setText(str(self.petitions[self.petitionActive][4]))

    def editEvent(self):
        result = editPetition(self.petitions[self.petitionActive][0], self.idField.text(), self.descField.text(
        ), self.weightField.text(), self.daysField.text())
        if not result:
            QMessageBox.information(self, "ProjectGamma - Petición editada",
                                    "Petición editada con éxito",
                                    buttons=QMessageBox.StandardButton.Ok)
            self.oldPetitionIndex = self.petitionActive
            self.populate()
        else:
            QMessageBox.critical(self, "ProjectGamma - Error",
                                 result, buttons=QMessageBox.StandardButton.Ok)

    def petitionChoiceChange(self):
        self.petitionActive = self.petitionChoice.currentIndex()
        self.refresh()

    def idFieldEvent(self):
        if self.idField.text():
            self.hasIdField = True
        else:
            self.hasIdField = False
        self.checkInputs()

    def daysFieldEvent(self):
        if self.daysField.text():
            self.hasDaysField = True
        else:
            self.hasDaysField = False
        self.checkInputs()

    def weightFieldEvent(self):
        if self.weightField.text():
            self.hasWeightField = True
        else:
            self.hasWeightField = False
        self.checkInputs()

    def descFieldEvent(self):
        if self.descField.text():
            self.hasDescField = True
        else:
            self.hasDescField = False
        self.checkInputs()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Return.value and self.editButton.isEnabled():
            self.editEvent()
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()


class PetitionDeleteUI(UI):
    deleteSignal = Signal()

    def __init__(self, parent):
        super(PetitionDeleteUI, self).__init__(
            PETITION_DELETE_UI, parent=parent)

    def initialize(self):
        self.deleteButton.clicked.connect(self.deleteEvent)
        self.petitionChoice.currentTextChanged.connect(
            self.petitionChoiceChange)
        self.petitionActive = 0
        self.oldIndex = 0
        self.petitions = None
        self.populate()

    def populate(self):
        self.petitionChoice.clear()
        countPetitions = getCountPetitions(assigned=False)
        if countPetitions:
            self.petitions = getPetitions(assigned=False)
            for item in self.petitions:
                self.petitionChoice.addItem(
                    "Identificador: "+str(item[1]))
        else:
            self.petitionChoice.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def petitionChoiceChange(self):
        self.oldIndex = self.petitionActive
        self.petitionActive = self.petitionChoice.currentIndex()

    def deleteEvent(self):
        reply = QMessageBox.warning(self, "ProjectGamma - Borrar Petición",
                                    "¿Estás seguro?",
                                    buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                    )
        if reply == QMessageBox.StandardButton.Yes:
            petitionId = self.petitions[self.petitionActive][0]
            deletePetition(petitionId)
            self.deleteSignal.emit()
            self.populate()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Return.value:
            self.deleteEvent()
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()
