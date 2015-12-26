
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QListView
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QColor

from Alerts.Alert import Alert

class AlertWidget(QWidget):

    MAX_WIDTH = 350

    def __init__(self, alert, parent=None):
        super().__init__(parent)

        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        self.alert = alert

        self.keywordsLabel = QLabel(self.alert.keywords)

        self.mainLayout.addWidget(self.keywordsLabel, 0, 0, 1, 1)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        categoryNames = [category.name for category in alert.categories]
        self.categoriesModel = QStringListModel(categoryNames)
        self.categoriesView = QListView()
        self.categoriesView.setModel(self.categoriesModel)
        self.categoriesModel.flags = lambda index: Qt.ItemIsEnabled | Qt.ItemNeverHasChildren

        self.categoriesView.setMaximumSize(self.MAX_WIDTH, 55)
        self.mainLayout.addWidget(self.categoriesView, 1, 0, 1, 1)
        self.setMaximumWidth(self.MAX_WIDTH)

        self.mainLayout.addWidget(QLabel("In store {}".format(self.alert.location)), 2, 0, 1, 1)
        self.mainLayout.addWidget(QLabel("Sort by {}".format(self.alert.sortOrder)), 3, 0, 1, 1)

        self.setAutoFillBackground(True)
        self.setStyleSheetLeave()

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
