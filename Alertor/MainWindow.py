
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QMenuBar, QMenu, QAction

from AlertsParameters.Categories.EbayCategoriesList import EbayCategoriesList
from AlertDialog.NewEbayAlertDialog import NewEbayAlertDialog
from AlertsResultsWidget import AlertsResultsWidget

from Alerts.Alert import Alert
from Results.Result import Result

class MainWindow(QMainWindow):
    def __init__(self, title):
        super().__init__()

        self.resize(1280, 800)
        self.setWindowTitle(title)
        self.mainLayout = QVBoxLayout()

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.ebayCategoriesList = EbayCategoriesList.fromCache("EbayCategories.dict")
        self.addNewAlertDialog = NewEbayAlertDialog(self.ebayCategoriesList, self)

        self.alertsResultsWidget = AlertsResultsWidget()
        self.mainLayout.addWidget(self.alertsResultsWidget)

        self.setupMenus()

        self.addNewAlertDialog.alertCreated.connect(self.__newAlertCreated_slot)

    def setupMenus(self):
        self.menuBar().setNativeMenuBar(True)
        menu_alert = self.menuBar().addMenu("Alerts")
        action_addNewAlert = menu_alert.addAction("Add new alert")
        action_addNewAlert.triggered.connect(self.__addNewAlert_slot)

    def __addNewAlert_slot(self):
        self.addNewAlertDialog.show()
        self.addNewAlertDialog.activateWindow()

    def __newAlertCreated_slot(self, alert):
        self.alertsResultsWidget.appendNewAlert(alert)

