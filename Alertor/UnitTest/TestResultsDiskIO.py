
import sys
import os
import datetime

# import in ../
sys.path.append(os.path.join(os.path.split(__file__)[0], os.pardir))

import unittest
from Results.ResultsDiskIO import ResultsDiskIO
from Alerts.Alert import Alert
from Results.Result import Result, Interval, Price

class TestResultsDiskIO(unittest.TestCase):

    def buildResultsList(self, nbResults):
        results = [Result("itemId_" + str(i),
                          "title_" + str(i),
                          "galleryURL_" + str(i),
                          "viewItemURL_" + str(i),
                          Price(str(i), "EUR"),
                          Interval(datetime.datetime.now(),
                                   datetime.datetime.now()),
                          "FR")
                   for i in range(0, nbResults)
                   ]
        return results

    def compareResults(self, expected, actual):
        self.assertEqual(expected.title, actual.title)
        self.assertEqual(expected.imgURL, actual.imgURL)
        self.assertEqual(expected.itemURL, actual.itemURL)
        self.assertEqual(expected.price.value, actual.price.value)
        self.assertEqual(expected.price.currency, actual.price.currency)
        self.assertEqual(expected.interval.start, actual.interval.start)
        self.assertEqual(expected.interval.end, actual.interval.end)

    def test_saveResultsToDisk_fileCorrectlyCreated(self):
        alert = Alert("test", [])
        results = self.buildResultsList(10)

        diskIO = ResultsDiskIO()
        filePath = diskIO.saveResultsToDisk(alert, results)

        self.assertTrue(os.path.exists(filePath))
        # Test we use the alert's uid in the filename to guarantee its uniqueness.
        self.assertTrue(str(alert.uid) in os.path.basename(filePath))

    def test_getResultsFromDisk_resultsCorrectlyDeserialized(self):
        alert = Alert("test", [])
        results = self.buildResultsList(10)
        diskIO = ResultsDiskIO()
        filePath = diskIO.saveResultsToDisk(alert, results)

        resultsDeserialized = diskIO.getResultsFromDisk(alert)
        for resExpected, resActual in zip(results, resultsDeserialized):
            self.compareResults(resExpected, resActual)
