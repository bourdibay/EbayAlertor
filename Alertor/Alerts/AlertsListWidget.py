
from PyQt5.QtWidgets import QWidget, QGridLayout, QScrollArea, QVBoxLayout
from PyQt5.QtCore import Qt, QEvent, pyqtSignal

from Alerts.Alert import Alert
from Alerts.AlertWidget import AlertWidget

class AlertsListWidget(QWidget):

    alertClicked = pyqtSignal(AlertWidget, Alert)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.alertsWidgetList = {}

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidget = QWidget()
        self.scrollAreaLayout = QVBoxLayout()
        self.scrollAreaWidget.setLayout(self.scrollAreaLayout)
        self.scrollArea.setWidget(self.scrollAreaWidget)

        self.scrollArea.setAlignment(Qt.AlignTop)
        self.scrollAreaLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.layout().addWidget(self.scrollArea)

        self.setMaximumWidth(AlertWidget.MAX_WIDTH + 10)

    def appendAlert(self, alert):
        print("[AlertsListWidget] appendAlert()")
        alertWidget = AlertWidget(alert)
        alertWidget.installEventFilter(self)
        self.alertsWidgetList[alert] = alertWidget
        self.appendAlertWidget(alertWidget)

    def appendAlertWidget(self, alertWidget):
        print("[AlertsListWidget] appendAlertWidget()")
        self.scrollAreaLayout.addWidget(alertWidget)

    def updateNbResultsSummary(self, alert, nbAddedResults, nbRemovedResults):
        print("[AlertsListWidget] updateNbResultsSummary()")
        if alert in self.alertsWidgetList:
            self.alertsWidgetList[alert].updateResultsSummary(nbAddedResults, nbRemovedResults)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            if isinstance(obj, AlertWidget):
                obj.setStyleSheetEnter()
        elif event.type() == QEvent.Leave:
            if isinstance(obj, AlertWidget):
                obj.setStyleSheetLeave()
        elif event.type() == QEvent.MouseButtonRelease:
            if isinstance(obj, AlertWidget):
                obj.setStyleSheetEnter()
                obj.clickOnWidget()

                self.alertClicked.emit(obj, obj.alert)

        elif event.type() == QEvent.MouseButtonPress:
            if isinstance(obj, AlertWidget):
                obj.setStyleSheetMousePress()
        return super().eventFilter(obj, event)
