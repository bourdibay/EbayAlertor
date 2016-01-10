
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

from Alerts.Alert import Alert
from Alerts.AlertsDiskIO import AlertsDiskIO

class AlertsListModel(QObject):

    alertAppended = pyqtSignal(Alert)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.alerts = []

    def loadSavedAlerts(self):
        alertsToLoad = AlertsDiskIO().getAlertsFromDisk()
        for alert in alertsToLoad:
            self.appendAlert(alert, save=False)

    def appendAlert(self, alert, save=True):
        self.alerts.append(alert)
        if save:
            AlertsDiskIO().saveAlertToDisk(alert)
        self.alertAppended.emit(alert)

    def deleteAlert(self, alert):
        try :
            idx = self.alerts.index(alert)
            AlertsDiskIO().deleteAlertInDisk(alert)
            del self.alerts[idx]
        except ValueError:
            pass

