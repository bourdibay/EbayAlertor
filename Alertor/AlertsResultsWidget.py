
from PyQt5.QtWidgets import QWidget, QSplitter, QVBoxLayout
from PyQt5.QtCore import QObject

from Alerts.AlertsController import AlertsController
from Results.ResultsController import ResultsController

from Results.ResultsDiskIO import ResultsDiskIO

from Alerts.Alert import Alert
from Results.Result import Result

class AlertsResultsWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.alertsController = AlertsController()
        self.resultsController = ResultsController()

        self.alertsController.alertRequested.connect(self.alertRequested)

        self.splitter = QSplitter()
        self.layout().addWidget(self.splitter)
        self.splitter.addWidget(self.alertsController.alertsListWidget)
        self.splitter.addWidget(self.resultsController.resultsListWidget)

    def alertRequested(self, alert):
        print("[AlertsResultsController] alertRequested()")
        results = ResultsDiskIO().getCurrentResultsFromDisk(alert.uid)
        self.resultsController.loadResults(results)

    def appendNewAlert(self, alert):
        print("[AlertsResultsController] appendNewAlert()")
        self.alertsController.appendNewAlert(alert)
