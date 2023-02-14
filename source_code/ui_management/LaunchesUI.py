from layout_data import *
from PyQt6.QtWidgets import QMessageBox
from core import *
from PyQt6.QtCore import pyqtSignal as Signal
from ui_management.UI import *


class LaunchesUI(UI):
    changeSignal = Signal()

    def __init__(self, parent):
        super(LaunchesUI, self).__init__(LAUNCHES_SCREEN_UI, parent=parent)

    def initialize(self):
        self.closeButton.clicked.connect(self.close)
        self.createLaunchButton.clicked.connect(self.createEvent)
        self.editLaunchButton.clicked.connect(self.editEvent)
        self.deleteLaunchButton.clicked.connect(self.deleteEvent)
        self.populate()

    def populate(self):
        launchesUnassignedCount = getCountLaunches(assigned=False)
        launchesAassignedCount = getCountLaunches(assigned=True)
        rocketCount = getCountAllRockets()
        self.launchesUnassignedLabel.setText(str(launchesUnassignedCount))
        self.launchesAssignedLabel.setText(str(launchesAassignedCount))
        self.rocketsLabel.setText(str(rocketCount))
        if rocketCount:
            self.createLaunchButton.setEnabled(True)
        else:
            self.createLaunchButton.setEnabled(False)
        if launchesUnassignedCount:
            self.editLaunchButton.setEnabled(True)
            self.deleteLaunchButton.setEnabled(True)
        else:
            self.editLaunchButton.setEnabled(False)
            self.deleteLaunchButton.setEnabled(False)

    def createEvent(self):
        self.createUI = LaunchNewUI(self)
        self.createUI.newSignal.connect(self.populate)
        self.createUI.newSignal.connect(self.changeSignal.emit)

    def editEvent(self):
        LaunchEditUI(self)

    def deleteEvent(self):
        self.deleteUI = LaunchDeleteUI(self)
        self.deleteUI.deleteSignal.connect(self.populate)
        self.deleteUI.deleteSignal.connect(self.changeSignal.emit)


class LaunchNewUI(UI):
    newSignal = Signal()

    def __init__(self, parent):
        super(LaunchNewUI, self).__init__(LAUNCH_NEW_UI, parent=parent)

    def initialize(self):
        self.createButton.clicked.connect(self.createEvent)
        self.rocketsChoice.currentTextChanged.connect(self.rocketsChoiceChange)
        self.idField.textChanged.connect(self.idFieldEvent)
        self.descField.textChanged.connect(self.descFieldEvent)
        self.daysField.textChanged.connect(self.daysFieldEvent)
        self.rocketActive = 0
        self.countRockets = getCountAllRockets()
        self.rockets = getAllRockets()
        for item in self.rockets:
            self.rocketsChoice.addItem(
                "Nombre: "+str(item[1])+"\tPeso Máx.: "+str(item[2]))

        # Enable flags
        self.hasIdField = False
        self.hasDaysField = False
        self.hasDescField = False

        self.populate()

    def populate(self):
        if self.countRockets and self.hasIdField and self.hasDaysField and self.hasDescField:
            self.createButton.setEnabled(True)
        else:
            self.createButton.setEnabled(False)
        if self.countRockets:
            self.rocketsChoice.setEnabled(True)
        else:
            self.rocketsChoice.setEnabled(False)

    def createEvent(self):
        result = addLaunch(self.rockets[self.rocketActive][0], self.idField.text(
        ), self.daysField.text(), self.descField.text())
        if not result:
            self.newSignal.emit()
            QMessageBox.information(self, "ProjectGamma - Lanzamiento creado",
                                    "Lanzamiento creado con éxito",
                                    buttons=QMessageBox.StandardButton.Ok)
            self.close()
        else:
            QMessageBox.critical(self, "ProjectGamma - Error",
                                 result, buttons=QMessageBox.StandardButton.Ok)

    def rocketsChoiceChange(self):
        self.rocketActive = self.rocketsChoice.currentIndex()

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


class LaunchEditUI(UIDialog):
    def __init__(self, parent):
        super(LaunchEditUI, self).__init__(LAUNCH_EDIT_UI, parent=parent)

    def initialize(self):
        self.editButton.clicked.connect(self.editEvent)
        self.launchChoice.currentTextChanged.connect(self.launchChoiceChange)
        self.rocketsChoice.currentTextChanged.connect(self.rocketsChoiceChange)
        self.idField.textChanged.connect(self.idFieldEvent)
        self.descField.textChanged.connect(self.descFieldEvent)
        self.daysField.textChanged.connect(self.daysFieldEvent)
        self.launchActive = 0
        self.oldLaunchIndex = 0
        self.rocketActive = 0
        self.launches = None
        self.getCountLaunches = getCountLaunches(False)

        self.countRockets = getCountAllRockets()
        self.rockets = getAllRockets()
        for item in self.rockets:
            self.rocketsChoice.addItem(
                "Nombre: "+str(item[1])+"\tPeso Máx.: "+str(item[2]))

        # Enable flags
        self.hasIdField = False
        self.hasDaysField = False
        self.hasDescField = False
        self.populate()

    def populate(self):
        self.launchChoice.clear()
        if self.getCountLaunches:
            self.launches = getLaunches(assigned=False)
            # print(self.launches)
            for item in self.launches:
                self.launchChoice.addItem(str(item[2]))
            self.launchChoice.setCurrentIndex(self.oldLaunchIndex)
            self.refresh()

    def findPosInRocketsChoice(self):
        pos = 0
        for rock in self.rockets:
            if self.launches[self.launchActive][1] == rock[0]:
                return pos
            pos = pos+1

    def checkInputs(self):
        if self.hasIdField and self.hasDaysField and self.hasDescField:
            self.editButton.setEnabled(True)
        else:
            self.editButton.setEnabled(False)

    def refresh(self):
        self.rocketsChoice.setCurrentIndex(self.findPosInRocketsChoice())
        self.idField.setText(self.launches[self.launchActive][2])
        self.daysField.setText(str(self.launches[self.launchActive][3]))
        self.descField.setText(self.launches[self.launchActive][4])

    def editEvent(self):
        rocketId = self.rockets[self.rocketActive][0]
        result = editLaunch(self.launches[self.launchActive][0], rocketId, self.idField.text(
        ), self.daysField.text(), self.descField.text())
        if not result:
            QMessageBox.information(self, "ProjectGamma - Lanzamiento editado",
                                    "Lanzamiento editado con éxito",
                                    buttons=QMessageBox.StandardButton.Ok)
            self.oldLaunchIndex = self.launchActive
            self.populate()
        else:
            QMessageBox.critical(self, "ProjectGamma - Error",
                                 result, buttons=QMessageBox.StandardButton.Ok)

    def rocketsChoiceChange(self):
        self.rocketActive = self.rocketsChoice.currentIndex()

    def launchChoiceChange(self):
        self.launchActive = self.launchChoice.currentIndex()
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

    def descFieldEvent(self):
        if self.descField.text():
            self.hasDescField = True
        else:
            self.hasDescField = False
        self.checkInputs()


class LaunchDeleteUI(UI):
    deleteSignal = Signal()

    def __init__(self, parent):
        super(LaunchDeleteUI, self).__init__(LAUNCH_DELETE_UI, parent=parent)

    def initialize(self):
        self.deleteButton.clicked.connect(self.deleteEvent)
        self.launchChoice.currentTextChanged.connect(self.launchChoiceChange)
        self.launchActive = 0
        self.oldIndex = 0
        self.launches = None
        self.populate()

    def populate(self):
        self.launchChoice.clear()
        countLaunches = getLaunches(assigned=False)
        if countLaunches:
            self.launches = getLaunches(assigned=False)
            for item in self.launches:
                self.launchChoice.addItem(
                    "Identificador: "+str(item[2]))
        else:
            self.launchChoice.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def launchChoiceChange(self):
        self.oldIndex = self.launchActive
        self.launchActive = self.launchChoice.currentIndex()

    def deleteEvent(self):
        reply = QMessageBox.warning(self, "ProjectGamma - Borrar Lanzamiento",
                                    "¿Estás seguro?",
                                    buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                    )
        if reply == QMessageBox.StandardButton.Yes:
            launchId = self.launches[self.launchActive][0]
            deleteLaunch(launchId)
            self.deleteSignal.emit()
            self.populate()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Return.value:
            self.deleteEvent()
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()
