
from PyQt5.QtCore import QObject, pyqtSignal

from Results.ResultsListModel import ResultsListModel
from Results.ResultsListWidget import ResultsListWidget

from Alerts.Alert import Alert
from Results.Result import Result

class ResultsController(QObject):

    def __init__(self):
        super().__init__()

        self.resultsListModel = ResultsListModel()
        self.resultsListWidget = ResultsListWidget()

        self.resultsListWidget.setCurrentResults(self.resultsListModel.resultsSorted)

        self.resultsListModel.currentResultsChanged.connect(self.__currentResultsChanged_slot)
        self.resultsListModel.resultImageDownloaded.connect(self.__resultImageDownloaded_slot)
        self.resultsListModel.resultShippingCostUpdated.connect(self.__resultShippingCostUpdated_slot)

    def loadResults(self, results):
        self.resultsListModel.addCurrentResults(results)

    def shutdownAllRequests(self):
        self.resultsListModel.shutdownAllRequests()

    def __currentResultsChanged_slot(self):
        self.resultsListWidget.setCurrentResults(self.resultsListModel.resultsSorted)

    def __resultImageDownloaded_slot(self, result):
        self.resultsListWidget.refreshResultThumbnail(result)

    def __resultShippingCostUpdated_slot(self, result):
        self.resultsListWidget.refreshShippingCost(result)
