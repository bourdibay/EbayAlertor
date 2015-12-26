
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

    def __init__(self):
        super().__init__()

        self.alertExecutorsPool = ExecutorsPool(name="AlertExecutorsPool",
                                                callbackDone=self.cacheResult_callback)
        self.alertExecutorsPool.executorFinished.connect(self.executorFinished)

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
        # TODO: check if new results
        # TODO: change new field of Alert and emit signal for widget
        print("Execution finished for {}".format(executor.alert.keywords))
#        results = AlertsDiskIO().getResultsFromDisk(executor.alert)

    def alertClicked(self, alertWidget, alert):
        print("[AlertsController] alertClicked()")
        self.alertRequested.emit(alert)
