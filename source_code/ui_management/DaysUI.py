from layout_data import *
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox
from core import *
from ui_management.UI import *
from PyQt6.QtCore import pyqtSignal as Signal


class DaysUI(UI):
    changeSignal = Signal()

    def __init__(self, parent):
        super(DaysUI, self).__init__(DAYS_SCREEN_UI, parent=parent)

    def initialize(self):
        self.forwardDaysButton.clicked.connect(self.daysEvent)
        self.launches_out = ""
        self.daysField.textChanged.connect(self.daysFieldEvent)
        self.hasDaysField = False
        self.populate()

    def populate(self):
        if self.hasDaysField:
            self.forwardDaysButton.setEnabled(True)
        else:
            self.forwardDaysButton.setEnabled(False)

        if self.launches_out:
            self.daysText.clear()
            self.daysText.setText(self.launches_out)
            self.daysText.verticalScrollBar().setValue(
                self.daysText.verticalScrollBar().maximum())
        else:
            self.daysText.setText("Esperando al proceso de avanzar días...")

    def daysEvent(self):
        days = self.daysField.text()
        try:
            days = int(days)
            if days <= 0:
                raise Exception()
        except:
            QMessageBox.critical(self, "ProjectGamma - Error",
                                 "Los días deben ser un número entero positivo mayor que 0", buttons=QMessageBox.StandardButton.Ok)
            return
        launches_out = forwardDays(days)
        if launches_out:
            launches_out = sorted(launches_out, key=lambda x: x[2])
            for element in launches_out:
                if self.launches_out:
                    self.launches_out = self.launches_out + "<br>"
                if element[0] == 1:
                    if element[3]:
                        self.launches_out = self.launches_out + "<font color=\"black\">" + \
                            element[2]+"</font><br><font color=\"green\">El lanzamiento " + \
                            element[1]+" ha sido entregado:</font>"
                        for el in element[3]:
                            if self.launches_out:
                                self.launches_out = self.launches_out + "<br>"
                            self.launches_out = self.launches_out + \
                                "<font color=\"blue\">&nbsp;&nbsp;&nbsp;&nbsp;" + el+" ha sido entregada</font>"
                    else:
                        self.launches_out = self.launches_out + "<font color=\"black\">" + \
                            element[2]+"</font><br><font color=\"red\">El lanzamiento " + \
                            element[1]+" ha sido entregado sin ninguna petición asignada</font>"
                elif element[0] == 0:
                    if element[3]:
                        self.launches_out = self.launches_out + "<font color=\"black\">" + \
                            element[2]+"</font><br><font color=\"#E07E00\">El lanzamiento " + \
                            element[1]+" está en tránsito:</font>"
                        for el in element[3]:
                            if self.launches_out:
                                self.launches_out = self.launches_out + "<br>"
                            self.launches_out = self.launches_out + \
                                "<font color=\"#B24105\">&nbsp;&nbsp;&nbsp;&nbsp;" + el+" está en tránsito</font>"
                    else:
                        self.launches_out = self.launches_out + "<font color=\"black\">" + \
                            element[2]+"</font><br><font color=\"#E07E00\">El lanzamiento " + \
                            element[1]+" está en tránsito sin ninguna petición asignada</font>"
                elif element[0] == 2:
                    self.launches_out = self.launches_out + "<font color=\"black\">" + \
                        element[2]+"</font><br><font color=\"red\">La petición " + \
                        element[1]+" ha caducado sin tener ningún lanzamiento asignado</font>"
        if not getCountDeployedLaunches(True) or not launches_out or not getCountPetitions(assigned=True):
            if self.launches_out:
                self.launches_out = self.launches_out + "<br>"
            self.launches_out = self.launches_out + "<font color=\"black\">" + \
                getDate()+"</font><br><font color=\"grey\">No hay más lanzamientos o peticiones que procesar</font>"
        self.changeSignal.emit()
        self.populate()

    def daysFieldEvent(self):
        if self.daysField.text():
            self.hasDaysField = True
        else:
            self.hasDaysField = False
        self.populate()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Return.value and self.hasDaysField:
            self.daysEvent()
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()
