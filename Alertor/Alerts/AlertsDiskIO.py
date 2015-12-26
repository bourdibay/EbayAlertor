
import json
import os
import uuid
import pickle

from Alerts.Alert import Alert
from AlertsParameters.Categories.Category import Category

class AlertsDiskIO(object):
    def __init__(self):
        super().__init__()
        self.alertsDirectory = "../Saves/"
        self.alertPrefix = "alert_"
        self.resultPrefix = "result_"
        if not os.path.exists(self.alertsDirectory):
            os.makedirs(self.alertsDirectory)

    def getAlertsFromDisk(self):
        alerts = []
        for file in os.listdir(self.alertsDirectory):
            fullFilename = os.path.join(self.alertsDirectory, file)
            if os.path.isfile(fullFilename) and file.startswith(self.alertPrefix):
                with open(fullFilename, "r") as fd:
                    alert = self.__tryCreateAlertFromFile(file, fd)
                    if alert:
                        alerts.append(alert)
        return alerts

    def __tryCreateAlertFromFile(self, filename, fd):
        uid = uuid.UUID(filename[len(self.alertPrefix):])
        try:
            jsonContent = json.load(fd)
        except:
            print("Invalid alert file format ({})".format(filename))
            return None

        keywords = jsonContent["keywords"]
        categoriesJson = jsonContent["categories"]
        location = jsonContent["location"]
        sortOrder = jsonContent["sortOrder"]
        categoriesList = []
        for categoryJson in categoriesJson:
            category = Category(categoryJson["name"],
                                categoryJson["id"],
                                categoryJson["level"])
            categoriesList.append(category)
        alert = Alert(keywords, categoriesList, location=location, uid=uid,
                      sortOrder=sortOrder)
        return alert

    def saveAlertToDisk(self, alert):
        categoriesDict = []
        for category in alert.categories:
            d = {
                "name": category.name,
                "id": category.ID,
                "level": category.level
                }
            categoriesDict.append(d)
        dict = {
            "keywords": alert.keywords,
            "location": alert.location,
            "categories": categoriesDict,
            "location": alert.location,
            "sortOrder": alert.sortOrder
            }
        jsonContent = json.dumps(dict)

        filename = os.path.join(self.alertsDirectory, self.alertPrefix + str(alert.uid))
        with open(filename, "w+") as fd:
            fd.writelines(jsonContent)
