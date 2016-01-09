
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
        self.alertExecutorsPool.executorFinished.connect(self.executorFinished)
        self.__resultsComparisonDone.connect(self.__updateNbResultsSummary_slot)

        self.alertsListModel = AlertsListModel()
        self.alertsListWidget = AlertsListWidget()

        self.alertsListModel.alertAppended.connect(self.alertAppended)
        self.alertsListWidget.alertClicked.connect(self.__alertClicked_slot)
        self.alertsListWidget.alertDeleted.connect(self.__deleteAlert_slot)

        self.alertsListModel.loadSavedAlerts()

    def appendNewAlert(self, alert):
        print("[AlertsController] appendNewAlert()")
        self.alertsListModel.appendAlert(alert)

    def alertAppended(self, alert):
        print("[AlertsController] alertAppended()")
        self.alertsListWidget.appendAlert(alert)
        # TODO: factory executor
        executor = EbayFindItemsExecutor(alert)
        self.alertExecutorsPool.addExecutor(executor)

    def __deleteAlert_slot(self, alert):
        print("[AlertsController] __deleteAlert_slot()")
        self.alertsListModel.deleteAlert(alert)

    def cacheResult_callback(self, executor):
        print("[AlertsController] cacheResult_callback()")
        if executor.result:
            ResultsDiskIO().saveSerializedResultsToDisk(executor.alert, executor.result)

    def executorFinished(self, executor):
        print("[AlertsController] executorFinished()")
        print("Execution finished for {}".format(executor.alert.keywords))
        previousResultFilepath = ResultsDiskIO().getPreviousResultFilepath()
        print("Gonna compare current results with {}".format(previousResultFilepath))
        if previousResultFilepath:
            currentResultFilepath = ResultsDiskIO().cacheDirectory
            alertUID = executor.alert.uid
            previousResults = ResultsDiskIO().getResultsFromDisk(previousResultFilepath, alertUID)
            currentResults = ResultsDiskIO().getCurrentResultsFromDisk(alertUID)
            (nbAddedResults, nbRemovedResults) = ResultsComparator().getNbDifferences(previousResults, currentResults)
            self.__resultsComparisonDone.emit(executor.alert, nbAddedResults, nbRemovedResults)
        self.alertsListWidget.activateAlertWidget(executor.alert)

    def __alertClicked_slot(self, alertWidget, alert):
        print("[AlertsController] __alertClicked_slot()")
        self.alertRequested.emit(alert)

    def __updateNbResultsSummary_slot(self, alert, nbAddedResults, nbRemovedResults):
        print("[AlertsController] __updateNbResultsSummary_slot()")        
        self.alertsListWidget.updateNbResultsSummary(alert, nbAddedResults, nbRemovedResults)
