
from PyQt5.QtCore import QObject, pyqtSignal

from Alerts.AlertsListModel import AlertsListModel
from Alerts.AlertsListWidget import AlertsListWidget

from Executors.ExecutorsPool import ExecutorsPool
from Executors.EbayFindItemsExecutor import EbayFindItemsExecutor

from Results.ResultsDiskIO import ResultsDiskIO

from Alerts.Alert import Alert
from Results.Result import Result
from Results.ResultsComparator import ResultsComparator

class AlertsController(QObject):

    alertRequested = pyqtSignal(Alert)
    __resultsComparisonDone = pyqtSignal(Alert, int, int)

    def __init__(self):
        super().__init__()

        self.alertExecutorsPool = ExecutorsPool(name="AlertExecutorsPool",
                                                callbackDone=self.cacheResult_callback)
        self.alertExecutorsPool.executorFinished.connect(self.__executorFinished_slot)
        self.__resultsComparisonDone.connect(self.__updateNbResultsSummary_slot)

        self.alertsListModel = AlertsListModel()
        self.alertsListWidget = AlertsListWidget()

        self.alertsListModel.alertAppended.connect(self.__alertAppended_slot)
        self.alertsListWidget.alertClicked.connect(self.__alertClicked_slot)
        self.alertsListWidget.alertDeleted.connect(self.__deleteAlert_slot)

        self.alertsListModel.loadSavedAlerts()

    def appendNewAlert(self, alert):
        self.alertsListModel.appendAlert(alert)

    def __alertAppended_slot(self, alert):
        self.alertsListWidget.appendAlert(alert)
        # TODO: factory executor
        executor = EbayFindItemsExecutor(alert)
        self.alertExecutorsPool.addExecutor(executor)

    def __deleteAlert_slot(self, alert):
        self.alertsListModel.deleteAlert(alert)

    def cacheResult_callback(self, executor):
        if executor.result:
            ResultsDiskIO().saveSerializedResultsToDisk(executor.alert, executor.result)

    def __executorFinished_slot(self, executor):
        print("Execution finished for {}".format(executor.alert.keywords))
        previousResultFilepath = ResultsDiskIO().getPreviousResultFilepath()
        if previousResultFilepath:
            currentResultFilepath = ResultsDiskIO().cacheDirectory
            alertUID = executor.alert.uid
            previousResults = ResultsDiskIO().getResultsFromDisk(previousResultFilepath, alertUID)
            currentResults = ResultsDiskIO().getCurrentResultsFromDisk(alertUID)
            (nbAddedResults, nbRemovedResults) = ResultsComparator().getNbDifferences(previousResults, currentResults)
            self.__resultsComparisonDone.emit(executor.alert, nbAddedResults, nbRemovedResults)
        self.alertsListWidget.activateAlertWidget(executor.alert)

    def __alertClicked_slot(self, alertWidget, alert):
        self.alertRequested.emit(alert)

    def __updateNbResultsSummary_slot(self, alert, nbAddedResults, nbRemovedResults):
        self.alertsListWidget.updateNbResultsSummary(alert, nbAddedResults, nbRemovedResults)
