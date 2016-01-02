
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

        self.resultsDirectory = os.path.join(self.cacheDirectory, "Results")
        thisResultDir = "{year:02d}{month:02d}{day:02d}_{hour:02d}{min:02d}{sec:02d}".format(year=self.startTimestamp.year,
                                                                                             month=self.startTimestamp.month,
                                                                                             day=self.startTimestamp.day,
                                                                                             hour=self.startTimestamp.hour,
                                                                                             min=self.startTimestamp.minute,
                                                                                             sec=self.startTimestamp.second)
        self.cacheDirectory = self.normalizePath(os.path.join(self.resultsDirectory, thisResultDir))
        if not os.path.exists(self.cacheDirectory):
            os.makedirs(self.cacheDirectory)

    def saveSerializedResultsToDisk(self, alert, results):
        filePath = self.createFullpath(self.resultPrefix + str(alert.uid))
        with open(filePath, "wb+") as fd:
            pickle.dump(results, fd)
        return filePath

    def saveResultsToDisk(self, alert, results):
        serializedResults = [result.serialize() for result in results]
        return self.saveSerializedResultsToDisk(alert, serializedResults)

    def getCurrentResultsFromDisk(self, alertUID):
        return self.getResultsFromDisk(self.cacheDirectory, alertUID)

    def getResultsFromDisk(self, resultDir, alertUID):
        results = []
        filename = os.path.join(resultDir, self.resultPrefix + str(alertUID))
        if os.path.exists(filename) and os.path.isfile(filename):
            with open(filename, "rb") as fd:
                data = pickle.load(fd)
                for info in data:
                    result = Result.createFromSerialized(info)
                    results.append(result)
        return results

    def getPreviousResultFilepath(self):
        def __isResultDir(dir):
            # TODO: Add "and isCorrectFormat()" to really get only result dirs.
            return os.path.isdir(os.path.join(self.resultsDirectory, dir))
        filesInResultsDir = [dir for dir in os.listdir(self.resultsDirectory) if __isResultDir(dir)]
        filesInResultsDir.sort()
        if len(filesInResultsDir) <= 1: # 1 because we have created the result dir with the current date
            return None
        return self.normalizePath(os.path.join(self.resultsDirectory, filesInResultsDir[-2]))
