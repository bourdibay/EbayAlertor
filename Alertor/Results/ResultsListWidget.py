
from PyQt5.QtWidgets import QWidget, QGridLayout, QScrollArea, QVBoxLayout
from PyQt5.QtCore import Qt, QEvent

from Results.Result import Result
from Results.ResultWidget import ResultWidget
from PyQt5.QtGui import QPixmap, QColor, QPalette

class ResultsListWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.resultWidgets = {}

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidget = QWidget()
        self.scrollAreaLayout = QVBoxLayout()
        self.scrollAreaWidget.setLayout(self.scrollAreaLayout)
        self.scrollArea.setWidget(self.scrollAreaWidget)

        self.scrollArea.setAlignment(Qt.AlignTop)
        self.scrollAreaLayout.setAlignment(Qt.AlignTop)
        
        self.layout().addWidget(self.scrollArea)

        self.scrollAreaLayout.setContentsMargins(2, 7, 2, 7)
        self.setBackgroundColor(QColor("#8A8A8A"))

    def __clearLayout(self, layout):
        self.resultWidgets.clear()
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().deleteLater()

    def refreshResultThumbnail(self, result):
        widget = self.resultWidgets.get(result, None)
        if widget:
            widget.refreshThumb()
    
    def refreshShippingCost(self, result):
        widget = self.resultWidgets.get(result, None)
        if widget:
            widget.refreshShippingCost()

    def setBackgroundColor(self, color):
        p = self.scrollAreaWidget.palette()
        p.setColor(QPalette.Background, color)
        self.scrollAreaWidget.setAutoFillBackground(True)
        self.scrollAreaWidget.setPalette(p)

    def setCurrentResults(self, results):
        print("[ResultsListWidget]: setCurrentResults()")
        self.__clearLayout(self.scrollAreaLayout)
        for result in results:
            resultWidget = ResultWidget(result)
            self.resultWidgets[result] = resultWidget
            self.scrollAreaLayout.addWidget(resultWidget)

#        resultWidget.installEventFilter(self)
