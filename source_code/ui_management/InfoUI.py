from layout_data import *
from PyQt6.QtCore import Qt
from core import *
from ui_management.UI import *


class InfoUI(UI):
    def __init__(self, parent):
        super(InfoUI, self).__init__(INFO_SCREEN_UI, parent=parent)

    def initialize(self):
        self.tabText = "&nbsp;&nbsp;&nbsp;&nbsp;"
        self.rocketUnusedCount = getCountRockets(False)
        self.rocketUsedCount = getCountRockets(True)
        self.rocketUnused = getRockets(False)
        self.rocketUsed = getRockets(True)
        self.rocketsActiveOut = ""

        self.petitionsUnassignedCount = getCountPetitions(assigned=False)
        self.petitionsAssignedCount = getCountPetitions(assigned=True)
        self.petitionsUnassigned = getPetitions(assigned=False)
        self.petitionsAssigned = getPetitions(assigned=True)
        self.petitionsActiveOut = ""

        self.launchesUnassignedCount = getCountLaunches(assigned=False)
        self.launchesAassignedCount = getCountLaunches(assigned=True)
        self.launchesDeployedCount = getCountDeployedLaunches(True)
        self.launchesUnassigned = getLaunches(False)
        self.launchesAssigned = getLaunches(True)
        self.launchesDeployed = getDeployedLaunches(True)
        self.launchesActiveOut = ""

        self.petitionsDeliveredCount = countHistoricPetitions(True)
        self.petitionsFailCount = countHistoricPetitions(False)
        self.petitionsDelivered = getHistoricPetitions(True)
        self.petitionsFail = getHistoricPetitions(False)
        self.petitionsHistoricOut = ""

        self.launchesDeliveredCount = countHistoricLaunches(True)
        self.launchesFailCount = countHistoricLaunches(False)
        self.launchesDelivered = getHistoricLaunches(True)
        self.launchesFail = getHistoricLaunches(False)

        self.launchesHistoricOut = ""

        self.populate()

    def populate(self):
        self.dateField.setText("Fecha: "+getDate())
        # Rockets Active
        self.rocketsActiveOut = "Cohetes sin utilizar ("+str(
            self.rocketUnusedCount)+"):"
        for rocket in self.rocketUnused:
            if self.rocketsActiveOut:
                self.rocketsActiveOut = self.rocketsActiveOut + "<br>"
            self.rocketsActiveOut = self.rocketsActiveOut + self.tabText + \
                "Nombre: " + rocket[1]+self.tabText + \
                "Peso: "+str(rocket[2])+" kg"
        self.rocketsActiveOut = self.rocketsActiveOut + \
            "<br>Cohetes utilizados ("+str(self.rocketUsedCount)+"):"
        for rocket in self.rocketUsed:
            if self.rocketsActiveOut:
                self.rocketsActiveOut = self.rocketsActiveOut + "<br>"
            self.rocketsActiveOut = self.rocketsActiveOut + self.tabText + \
                "Nombre: " + rocket[1]+self.tabText + \
                "Peso: "+str(rocket[2])+" kg"
        self.rocketsActiveText.setText(self.rocketsActiveOut)

        # Petitions Active
        self.petitionsActiveOut = "Peticiones sin asignar ("+str(
            self.petitionsUnassignedCount)+"):"
        for petition in self.petitionsUnassigned:
            if self.petitionsActiveOut:
                self.petitionsActiveOut = self.petitionsActiveOut + "<br>"
            self.petitionsActiveOut = self.petitionsActiveOut + self.tabText + "Identificador: " + petition[1]+self.tabText+"Descripción: "+petition[2]+self.tabText+"Peso: "+str(
                petition[3])+" kg"+self.tabText+"Días máximos de llegada: "+str(petition[4])+self.tabText+"Fecha de creación: "+petition[7]
        self.petitionsActiveOut = self.petitionsActiveOut + \
            "<br>Peticiones asignadas ("+str(self.petitionsAssignedCount)+"):"
        for petition in self.petitionsAssigned:
            if self.petitionsActiveOut:
                self.petitionsActiveOut = self.petitionsActiveOut + "<br>"
            self.petitionsActiveOut = self.petitionsActiveOut + self.tabText + "Identificador: " + petition[1]+self.tabText+"Descripción: "+petition[2]+self.tabText+"Peso: "+str(
                petition[3])+" kg"+self.tabText+"Días máximos de llegada: "+str(petition[4])+self.tabText+"Fecha de creación: "+petition[7]+self.tabText+"Lanzamiento asignado: "+getLaunchById(petition[5])[2]
        self.petitionsActiveText.setText(self.petitionsActiveOut)

        # Launches Actives
        self.launchesActiveOut = "Lanzamientos sin asignar ("+str(
            self.launchesUnassignedCount)+"):"
        for launch in self.launchesUnassigned:
            if self.launchesActiveOut:
                self.launchesActiveOut = self.launchesActiveOut + "<br>"
            self.launchesActiveOut = self.launchesActiveOut + self.tabText + "Identificador: " + launch[2]+self.tabText+"Descripción: "+launch[4]+self.tabText+"Cohete utilizado: "+getRocketById(
                launch[1])[1]+self.tabText+"Fecha de creación: "+launch[6]+self.tabText+"Días de llegada: "+str(launch[3])+self.tabText+"Capacidad restanste: "+str(getLaunchCapacity(launch[0])-getLaunchLoad(launch[0]))+" kg"
        self.launchesActiveOut = self.launchesActiveOut + \
            "<br>Lanzamientos asignados (" + \
            str(self.launchesAassignedCount)+"):"
        for launch in self.launchesAssigned:
            if self.launchesActiveOut:
                self.launchesActiveOut = self.launchesActiveOut + "<br>"
            self.launchesActiveOut = self.launchesActiveOut + self.tabText + "Identificador: " + launch[2]+self.tabText+"Descripción: "+launch[4]+self.tabText+"Cohete utilizado: "+getRocketById(
                launch[1])[1]+self.tabText+"Fecha de creación: "+launch[6]+self.tabText+"Días de llegada: "+str(launch[3])+self.tabText+"Carga total: "+str(getLaunchLoad(launch[0]))+" kg"
        self.launchesActiveOut = self.launchesActiveOut + \
            "<br>Lanzamientos desplegados (" + \
            str(self.launchesDeployedCount)+"):"
        for launch in self.launchesDeployed:
            if self.launchesActiveOut:
                self.launchesActiveOut = self.launchesActiveOut + "<br>"
            self.launchesActiveOut = self.launchesActiveOut + self.tabText + "Identificador: " + launch[2]+self.tabText+"Descripción: "+launch[4]+self.tabText+"Cohete utilizado: "+getRocketById(
                launch[1])[1]+self.tabText+"Fecha de creación: "+launch[6]+self.tabText+"Días de llegada: "+str(launch[3])+self.tabText+"Carga total: "+str(getLaunchLoad(launch[0]))+" kg"
        self.launchesActiveText.setText(self.launchesActiveOut)

        # Petitions historic
        self.petitionsHistoricOut = "Peticiones entregadas ("+str(
            self.petitionsDeliveredCount)+"):"
        for petition in self.petitionsDelivered:
            if self.petitionsHistoricOut:
                self.petitionsHistoricOut = self.petitionsHistoricOut + "<br>"
            self.petitionsHistoricOut = self.petitionsHistoricOut + self.tabText + "Identificador: " + petition[1]+self.tabText+"Descripción: "+petition[2]+self.tabText+"Peso: "+str(
                petition[3])+" kg"+self.tabText+"Fecha de creación: "+petition[7]+self.tabText+"Fecha de llegada: "+petition[8]+self.tabText+"Lanzamiento asignado: "+getLaunchById(petition[5])[2]
        self.petitionsHistoricOut = self.petitionsHistoricOut + \
            "<br>Peticiones fallidas ("+str(self.petitionsFailCount)+"):"
        for petition in self.petitionsFail:
            if self.petitionsHistoricOut:
                self.petitionsHistoricOut = self.petitionsHistoricOut + "<br>"
            self.petitionsHistoricOut = self.petitionsHistoricOut + self.tabText + "Identificador: " + petition[1]+self.tabText+"Descripción: "+petition[2]+self.tabText+"Peso: "+str(
                petition[3])+" kg"+self.tabText+"Fecha de creación: "+petition[7]+self.tabText+"Fecha de caducidad: "+petition[8]
        self.petitionsHistoricText.setText(self.petitionsHistoricOut)

        # Launches Historic
        self.launchesHistoricOut = "Lanzamientos entregados ("+str(
            self.launchesDeliveredCount)+"):"
        for launch in self.launchesDelivered:
            if self.launchesHistoricOut:
                self.launchesHistoricOut = self.launchesHistoricOut + "<br>"
            self.launchesHistoricOut = self.launchesHistoricOut + self.tabText + "Identificador: " + launch[2]+self.tabText+"Descripción: "+launch[4]+self.tabText+"Cohete utilizado: "+getRocketById(
                launch[1])[1]+self.tabText+"Fecha de creación: "+launch[6]+self.tabText+"Fecha de llegada: "+str(launch[7])+self.tabText+"Carga total: "+str(getLaunchLoad(launch[0]))+" kg"
        self.launchesHistoricOut = self.launchesHistoricOut + \
            "<br>Lanzamientos fallidos (" + str(self.launchesFailCount)+"):"
        for launch in self.launchesFail:
            if self.launchesHistoricOut:
                self.launchesHistoricOut = self.launchesHistoricOut + "<br>"
            self.launchesHistoricOut = self.launchesHistoricOut + self.tabText + "Identificador: " + launch[2]+self.tabText+"Descripción: "+launch[4]+self.tabText+"Cohete utilizado: "+getRocketById(
                launch[1])[1]+self.tabText+"Fecha de creación: "+launch[6]+self.tabText+"Fecha caducada: "+str(launch[7])+self.tabText+"Carga total: "+str(getLaunchLoad(launch[0]))+" kg"
        self.launchesHistoricText.setText(self.launchesHistoricOut)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()
