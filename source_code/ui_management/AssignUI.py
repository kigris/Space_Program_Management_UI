from layout_data import *
from PyQt6.QtCore import Qt
from core import *
from model import countPetitions
from ui_management.UI import *
from PyQt6.QtCore import pyqtSignal as Signal


class AssignUI(UI):
    changeSignal = Signal()  # señal para comunicarse con ventana principal

    def __init__(self, parent):
        super(AssignUI, self).__init__(ASSIGN_SCREEN_UI, parent=parent)

    def initialize(self):
        # Inicialización de manejadores de evento
        self.assignButton.clicked.connect(self.assignEvent)
        # Variables de salida
        self.out = ""
        self.countLaunches = getCountDeployedLaunches(False)
        # Se puebla la ventana
        self.populate()

    def populate(self):
        # Si no hay lanzamiento
        if not self.countLaunches:
            self.assignText.setText(
                "No hay lanzamiento sin desplegar a los que poder asignar peticiones")
            # se impide realizar la acción de asignar
            self.assignButton.setEnabled(False)
            return

        # Si hay salida
        if self.out:
            self.assignText.setText(self.out)  # se puebla el cuadro de texto
            self.assignText.verticalScrollBar().setValue(
                self.assignText.verticalScrollBar().maximum())
        else:
            self.assignText.setText(
                "Esperando a comenzar el proceso de asignación...")

    def assignEvent(self):
        # Se obtienen las peticiones éxitosas y fallidas
        petitions_assigned, petitions_failed = assign()
        for el in petitions_assigned:  # se recorren las éxitosas
            if self.out:
                self.out = self.out + "<br>"
            self.out = self.out + "<font color=\"green\">La petición " + \
                el[0]+" ha sido asignada al lanzamiento "+el[1]+"</font>"
        for element in petitions_failed:
            if self.out:
                self.out = self.out + "<br>"
            self.out = self.out + "<font color=\"red\">La petición " + \
                element+" no ha podido ser asignada a ningún lanzamiento</font>"
        if not countPetitions(assigned=False):
            if self.out:
                self.out = self.out + "<br>"
            self.out = self.out + \
                ("<font color=\"grey\">No hay más peticiones que asignar</font>")
        self.changeSignal.emit()
        self.populate()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Return.value:
            self.assignEvent()
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()
