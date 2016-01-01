
import json
import os
import uuid
import pickle
import datetime

from Alerts.Alert import Alert
from Results.Result import Result, Interval

from CacheDiskIO import CacheDiskIO

class ResultsDiskIO(CacheDiskIO):

    startTimestamp = datetime.datetime.now()

    def __init__(self):
        super().__init__()
        self.resultPrefix = "result_"

        self.fullDir = os.path.join(self.fullDir, "Results")
        currentDir = "{year:02d}{month:02d}{day:02d}_{hour:02d}{min:02d}{sec:02d}".format(year=self.startTimestamp.year,
                                                                                          month=self.startTimestamp.month,
                                                                                          day=self.startTimestamp.day,
                                                                                          hour=self.startTimestamp.hour,
                                                                                          min=self.startTimestamp.minute,
                                                                                          sec=self.startTimestamp.second)
        self.fullDir = os.path.join(self.fullDir, currentDir)
        if not os.path.exists(self.fullDir):
            os.makedirs(self.fullDir)

    def saveSerializedResultsToDisk(self, alert, results):
        filePath = self.createFullpath(self.resultPrefix + str(alert.uid))
        with open(filePath, "wb+") as fd:
            pickle.dump(results, fd)
        return filePath

    def saveResultsToDisk(self, alert, results):
        serializedResults = [result.serialize() for result in results]
        return self.saveSerializedResultsToDisk(alert, serializedResults)

    def getResultsFromDisk(self, alert):
        results = []
        filename = self.createFullpath(self.resultPrefix + str(alert.uid))
        if os.path.exists(filename) and os.path.isfile(filename):
            with open(filename, "rb") as fd:
                data = pickle.load(fd)
                for info in data:
                    result = Result.createFromSerialized(info)
                    results.append(result)
        return results

