
from PyQt5.QtCore import QObject, pyqtSignal

from Alerts.AlertsListModel import AlertsListModel
from Alerts.AlertsListWidget import AlertsListWidget

from Executors.ExecutorsPool import ExecutorsPool
from Executors.EbayFindItemsExecutor import EbayFindItemsExecutor

from Alerts.AlertsDiskIO import AlertsDiskIO
from Results.ResultsDiskIO import ResultsDiskIO

from Alerts.Alert import Alert
from Results.Result import Result

class AlertsController(QObject):

    alertRequested = pyqtSignal(Alert)
    __resultsComparisonDone = pyqtSignal(Alert, int, int)

    def __init__(self):
        super().__init__()

        self.alertExecutorsPool = ExecutorsPool(name="AlertExecutorsPool",
                                                callbackDone=self.cacheResult_callback)
        self.alertExecutorsPool.executorFinished.connect(self.executorFinished)
        self.__resultsComparisonDone.connect(self.updateNbResultsSummary)

        self.alertsListModel = AlertsListModel()
        self.alertsListWidget = AlertsListWidget()

        self.alertsListModel.alertAppended.connect(self.alertAppended)
        self.alertsListWidget.alertClicked.connect(self.alertClicked)

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
            (nbAddedResults, nbRemovedResults) = self.compareResults(previousResultFilepath, currentResultFilepath, executor.alert.uid)
            self.__resultsComparisonDone.emit(executor.alert, nbAddedResults, nbRemovedResults)

    def alertClicked(self, alertWidget, alert):
        print("[AlertsController] alertClicked()")
        self.alertRequested.emit(alert)

    def compareResults(self, previousResultFilepath, currentResultFilepath, alertUID):
        """

        Return:
          tuple of (number of newly added results, number of removed results)
        """
        print("[AlertsController] compareResults()")        
        previousResults = ResultsDiskIO().getResultsFromDisk(previousResultFilepath, alertUID)
        currentResults = ResultsDiskIO().getCurrentResultsFromDisk(alertUID)

        if not previousResults:
            return (len(currentResults), 0)
        previousSet = set([result.itemID for result in previousResults])
        currentSet = set([result.itemID for result in currentResults])
        removedResults = previousSet - currentSet
        addedResults = currentSet - previousSet

        print("There is {} removed items".format(len(removedResults)))
        print("There is {} added items".format(len(addedResults)))
        return (len(addedResults), len(removedResults))                

    def updateNbResultsSummary(self, alert, nbAddedResults, nbRemovedResults):
        print("[AlertsController] updateNbResultsSummary()")        
        self.alertsListWidget.updateNbResultsSummary(alert, nbAddedResults, nbRemovedResults)
