from layout_data import *
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QMessageBox, QLineEdit
from core import *
from model import countDeployedLaunches
from ui_management.LaunchesUI import LaunchesUI
from ui_management.RocketsUI import *
from ui_management.UI import *
from ui_management.PetitionsUI import *
from ui_management.AssignUI import *
from ui_management.DaysUI import *
from ui_management.InfoUI import *


class MainUI(UI):
    def __init__(self, parent):
        super(MainUI, self).__init__(MAIN_SCREEN_UI, parent=parent)

    def initialize(self):
        self.closeButton.clicked.connect(self.close)
        self.rocketsButon.clicked.connect(self.rocketsEvent)
        self.petitionsButton.clicked.connect(self.petitionsEvent)
        self.launchesButton.clicked.connect(self.launchesEvent)
        self.assignButton.clicked.connect(self.assignEvent)
        self.daysButton.clicked.connect(self.daysEvent)
        self.infoButton.clicked.connect(self.infoEvent)
        self.populateButton.clicked.connect(self.populateEvent)
        self.populate()

    def populate(self):
        countUnusedRockets = getCountRockets(False)
        countUsedRockets = getCountRockets(True)
        countPetitionsUnassigned = getCountPetitions(assigned=False)
        countLaunchesNotAssigned = getCountLaunches(False)
        countPetitionsAssigned = getCountPetitions(assigned=True)
        countLaunchesAssigned = getCountLaunches(True)
        countLaunchesDeployed = countDeployedLaunches(True)
        self.dateField.setText("Fecha: "+str(getDate()))
        if countUnusedRockets:
            self.rocketsUnusedLabel.setText(
                "Cohetes (sin usar): "+str(countUnusedRockets))
        else:
            self.rocketsUnusedLabel.setText("No hay cohetes sin usar")
        if countUsedRockets:
            self.rocketsUsedLabel.setText(
                "Cohetes (usados): "+str(countUsedRockets))
        else:
            self.rocketsUsedLabel.setText("No hay cohetes usados")
        if countPetitionsUnassigned:
            self.petitionsUnassignedLabel.setText(
                "Peticiones (sin asignar): "+str(countPetitionsUnassigned))
        else:
            self.petitionsUnassignedLabel.setText(
                "No hay peticiones sin asignar")
        if countLaunchesNotAssigned:
            self.launchesUnassignedLabel.setText(
                "Lanzamientos (sin asignar): "+str(countLaunchesNotAssigned))
        else:
            self.launchesUnassignedLabel.setText(
                "No hay lanzamientos sin asignar")
        if countPetitionsAssigned:
            self.petitionsAssignedLabel.setText(
                "Peticiones (asignadas): "+str(countPetitionsAssigned))
        else:
            self.petitionsAssignedLabel.setText("No hay peticiones asignadas")
        if countLaunchesAssigned:
            self.launchesAssignedLabel.setText(
                "Lanzamientos (asignados): "+str(countLaunchesAssigned))
        else:
            self.launchesAssignedLabel.setText(
                "No hay lanzamientos asignados")
        if countLaunchesDeployed:
            self.launchesDeployedLabel.setText(
                "Lanzamientos (desplegados): "+str(countLaunchesDeployed))
        else:
            self.launchesDeployedLabel.setText(
                "No hay lanzamientos desplegados")

    def rocketsEvent(self):
        self.rocketsUI = RocketsUI(self)
        self.rocketsUI.changeSignal.connect(self.populate)

    def petitionsEvent(self):
        self.petitionsUI = PetitionsUI(self)
        self.petitionsUI.changeSignal.connect(self.populate)

    def launchesEvent(self):
        self.launchesUI = LaunchesUI(self)
        self.launchesUI.changeSignal.connect(self.populate)

    def assignEvent(self):
        self.assignUI = AssignUI(self)
        self.assignUI.changeSignal.connect(self.populate)

    def daysEvent(self):
        self.daysUI = DaysUI(self)
        self.daysUI.changeSignal.connect(self.populate)

    def infoEvent(self):
        self.infoUI = InfoUI(self)

    def populateEvent(self):
        populateDB()
        self.populate()

    # def keyPressEvent(self, e):
    #     if e.key() == Qt.Key.Key_Return.value:


class LoginUI(UI):
    def __init__(self):
        super(LoginUI, self).__init__(LOGIN_SCREEN_UI)

    def initialize(self):
        self.userField = self.findChild(QLineEdit, "userField")
        self.userField.textChanged.connect(self.userFieldEvent)
        self.passwordField = self.findChild(QLineEdit, "passwordField")
        self.passwordField.textChanged.connect(self.passwordFieldEvent)
        self.loginButton = self.findChild(QPushButton, "loginButton")
        self.loginButton.clicked.connect(self.loginEvent)
        self.loginButton.setAutoDefault(True)

        # Enable flags
        self.hasUserField = False
        self.hasPasswordField = False
        self.checkEntries(False)

        self.populate()

    def loginEvent(self):
        userCheck = checkLogin(self.userField.text(),
                               self.passwordField.text())
        if userCheck:
            self.hide()
            self.mainUI = MainUI(self)
        else:
            errorDialog = QMessageBox.critical(self, "ProjectGamma - Error de inicio de sesión",
                                               "Usuario o contraseña incorrectos",
                                               buttons=QMessageBox.StandardButton.Ok,
                                               )

    def populate(self):
        if self.hasUserField and self.hasPasswordField:
            self.loginButton.setEnabled(True)
        else:
            self.loginButton.setEnabled(False)

    def checkEntries(self, notify=True):
        self.userFieldEvent(notify)
        self.passwordFieldEvent(notify)

    def userFieldEvent(self, notify=True):
        if self.userField.text():
            self.hasUserField = True
        else:
            self.hasUserField = False
        if notify:
            self.populate()

    def passwordFieldEvent(self, notify=True):
        if self.userField.text():
            self.hasPasswordField = True
        else:
            self.hasPasswordField = False
        if notify:
            self.populate()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Return.value and self.hasUserField and self.hasPasswordField:
            self.loginEvent()
