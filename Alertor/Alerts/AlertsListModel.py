
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

from Alerts.Alert import Alert
from Alerts.AlertsDiskIO import AlertsDiskIO

# TODO: Delete alerts
class AlertsListModel(QObject):

    alertAppended = pyqtSignal(Alert)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.alerts = []

    def loadSavedAlerts(self):
        print("[AlertsListModel] loadSavedAlerts()")
        alertsToLoad = AlertsDiskIO().getAlertsFromDisk()
        for alert in alertsToLoad:
            self.appendAlert(alert, save=False)

    def appendAlert(self, alert, save=True):
        print("[AlertsListModel] appendAlert()")
        self.alerts.append(alert)
        if save:
            AlertsDiskIO().saveAlertToDisk(alert)
        self.alertAppended.emit(alert)
