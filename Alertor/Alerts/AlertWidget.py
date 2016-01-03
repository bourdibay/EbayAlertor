
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QListView, QHBoxLayout
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QColor

from Alerts.Alert import Alert

class AlertWidget(QWidget):

    MAX_WIDTH = 350

    def __init__(self, alert, parent=None):
        super().__init__(parent)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.alert = alert

        self.keywordsLabel = QLabel(self.alert.keywords)

        self.mainLayout.addWidget(self.keywordsLabel)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        categoryNames = [category.name for category in alert.categories]
        self.categoriesModel = QStringListModel(categoryNames)
        self.categoriesView = QListView()
        self.categoriesView.setModel(self.categoriesModel)
        self.categoriesModel.flags = lambda index: Qt.ItemIsEnabled | Qt.ItemNeverHasChildren

        self.categoriesView.setMaximumSize(self.MAX_WIDTH, 55)
        self.mainLayout.addWidget(self.categoriesView)
        self.setMaximumWidth(self.MAX_WIDTH)

        resultSummaryLayout = QHBoxLayout()
        # TODO: add colors, style, ...
        self.addedResultsWidget = QLabel()
        self.removedResultsWidget = QLabel()
        self.updateResultsSummary("N/A", "N/A")
        resultSummaryLayout.addWidget(self.addedResultsWidget)
        resultSummaryLayout.addWidget(self.removedResultsWidget)
        self.mainLayout.addLayout(resultSummaryLayout)

        self.mainLayout.addWidget(QLabel("In store {}".format(self.alert.location)))
        self.mainLayout.addWidget(QLabel("Sort by {}".format(self.alert.sortOrder)))

        self.setAutoFillBackground(True)
        self.setStyleSheetLeave()

    def updateResultsSummary(self, nbAddedResults, nbRemovedResults):
        self.addedResultsWidget.setText("Added: " + str(nbAddedResults))
        self.removedResultsWidget.setText("Removed: " + str(nbRemovedResults))

    def setStyleSheetEnter(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor("#8DF6FC"))
        self.setPalette(p)

    def setStyleSheetLeave(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor("#CED6D6"))
        self.setPalette(p)

    def setStyleSheetMousePress(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor("#C0ECFA"))
        self.setPalette(p)

    def clickOnWidget(self):
        print("Click detected, should perform request to ebay")
        pass
