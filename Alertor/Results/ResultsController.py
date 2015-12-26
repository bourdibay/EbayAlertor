
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

        self.resultsListModel.currentResultsChanged.connect(self.__currentResultsChangedSlot)
        self.resultsListModel.resultImageDownloaded.connect(self.__resultImageDownloaded)
        self.resultsListModel.resultShippingCostUpdated.connect(self.__resultShippingCostUpdated)

    def loadResults(self, results):
        self.resultsListModel.addCurrentResults(results)

    def __currentResultsChangedSlot(self):
        self.resultsListWidget.setCurrentResults(self.resultsListModel.resultsSorted)

    def __resultImageDownloaded(self, result):
        self.resultsListWidget.refreshResultThumbnail(result)

    def __resultShippingCostUpdated(self, result):
        self.resultsListWidget.refreshShippingCost(result)
