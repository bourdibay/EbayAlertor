﻿
from PyQt5.QtWidgets import QWidget, QGridLayout, QScrollArea, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QEvent, pyqtSignal

from Alerts.Alert import Alert
from Alerts.AlertWidget import AlertWidget

class AlertsListWidget(QWidget):

    alertClicked = pyqtSignal(AlertWidget, Alert)
    alertDeleted = pyqtSignal(Alert)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.alertsWidgetList = {} # Alert - AlertWidget

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidget = QWidget()
        self.scrollAreaLayout = QVBoxLayout()
        self.scrollAreaLayout.setContentsMargins(5, 5, 5, 5)
        self.scrollAreaWidget.setLayout(self.scrollAreaLayout)
        self.scrollArea.setWidget(self.scrollAreaWidget)

        self.scrollArea.setAlignment(Qt.AlignTop)
        self.scrollAreaLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.mainLayout.addWidget(self.scrollArea)

        self.setMaximumWidth(AlertWidget.MAX_WIDTH + 10)

    def appendAlert(self, alert):
        alertWidget = AlertWidget(alert)
        alertWidget.setDisabled(True)
        alertWidget.clicked.connect(lambda: self.alertClicked.emit(alertWidget, alertWidget.alert))
        alertWidget.closed.connect(lambda: self.alertWidgetClose(alertWidget))
        self.alertsWidgetList[alert] = alertWidget
        self.appendAlertWidget(alertWidget)

    def appendAlertWidget(self, alertWidget):
        self.scrollAreaLayout.addWidget(alertWidget)

    def updateNbResultsSummary(self, alert, nbAddedResults, nbRemovedResults):
         if alert in self.alertsWidgetList:
            self.alertsWidgetList[alert].updateResultsSummary(nbAddedResults, nbRemovedResults)

    def activateAlertWidget(self, alert):
        if alert in self.alertsWidgetList:
            self.alertsWidgetList[alert].setDisabled(False)

    def alertWidgetClose(self, alertWidget):
        alert = alertWidget.alert
        reply = QMessageBox.question(self, "Confirmation",
                                     "Are you sure to delete alert \"{}\" ?".format(alert.keywords),
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.scrollAreaLayout.removeWidget(alertWidget)
            alertWidget.deleteLater()
            del self.alertsWidgetList[alert]
            self.alertDeleted.emit(alert)
