
from PyQt5.QtWidgets import QWidget, QSplitter, QVBoxLayout
from PyQt5.QtCore import QObject

from Alerts.AlertsController import AlertsController
from Results.ResultsController import ResultsController

from Results.ResultsDiskIO import ResultsDiskIO

from Alerts.Alert import Alert
from Results.Result import Result
from Results.ResultsComparator import ResultsComparator

class AlertsResultsWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.alertsController = AlertsController()
        self.resultsController = ResultsController()

        self.alertsController.alertRequested.connect(self.__alertRequested_slot)

        self.splitter = QSplitter()
        self.layout().addWidget(self.splitter)
        self.splitter.addWidget(self.alertsController.alertsListWidget)
        self.splitter.addWidget(self.resultsController.resultsListWidget)

    def __alertRequested_slot(self, alert):
        currentResults = ResultsDiskIO().getCurrentResultsFromDisk(alert.uid)
        # Compare with previous results, in order to flag the newly added results.
        previousResultFilepath = ResultsDiskIO().getPreviousResultFilepath()
        if previousResultFilepath:
            previousResults = ResultsDiskIO().getResultsFromDisk(previousResultFilepath, alert.uid)
            (addedResults, removedResults) = ResultsComparator().extractDifferentResults(previousResults, currentResults)
            for result in addedResults:
                result.isNewResult = True
        self.resultsController.loadResults(currentResults)

    def appendNewAlert(self, alert):
        self.alertsController.appendNewAlert(alert)
