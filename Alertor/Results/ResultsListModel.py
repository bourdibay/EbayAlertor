

from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

from Results.Result import Result
from CacheDiskIO import CacheDiskIO
from Executors.ExecutorsPool import ExecutorsPool
from Executors.ImageDownloadExecutor import ImageDownloadExecutor
from Executors.EbayShippingFeesExecutor import EbayShippingFeesExecutor

class ResultsListModel(QObject):

    currentResultsChanged = pyqtSignal()
    resultImageDownloaded = pyqtSignal(Result)
    resultShippingCostUpdated = pyqtSignal(Result)

    def __init__(self):
        super().__init__()
        self.resultsURL = {}
        self.resultsID = {}
        self.resultsSorted = []
        self.imageDownloaderPool = None
        self.shippingFeesPool = None

    def addCurrentResults(self, results):
        self.shutdownAllRequests()

        self.resultsURL.clear()
        self.resultsID.clear()
        self.resultsSorted.clear()

        self.imageDownloaderPool = ExecutorsPool(name="ImageDownloaderPool",
                                                 callbackDone=self.imageDownloaded_callback,
                                                 max_workers=20)
        self.shippingFeesPool = ExecutorsPool(name="ShippingFeesPool",
                                              callbackDone=self.shippingFeesGotten_callback,
                                              max_workers=20)

        for result in results:
            self.resultsURL[result.imgURL] = result
            self.resultsID[result.itemID] = result
            self.resultsSorted.append(result)
            self.imageDownloaderPool.addExecutor(ImageDownloadExecutor(result.imgURL))
            self.shippingFeesPool.addExecutor(EbayShippingFeesExecutor(result.itemID, result.country))
        self.currentResultsChanged.emit()

    def shutdownAllRequests(self):
        if self.imageDownloaderPool:
            self.imageDownloaderPool.shutdown()
        if self.shippingFeesPool:
            self.shippingFeesPool.shutdown()

    def imageDownloaded_callback(self, executor):
        result = self.resultsURL.get(executor.url, None)
        if result and executor.result:
            result.imageInCache = executor.result
            self.resultImageDownloaded.emit(result)

    def shippingFeesGotten_callback(self, executor):
        result = self.resultsID.get(executor.itemID, None)
        if result and executor.result:
            (result.shippingCost.value, result.shippingCost.currency) = executor.result
            self.resultShippingCostUpdated.emit(result)

