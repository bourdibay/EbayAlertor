
import sys
import os
import datetime

# import in ../
sys.path.append(os.path.join(os.path.split(__file__)[0], os.pardir))

import unittest
from Results.Result import Result, Interval, Price
from Results.ResultsComparator import ResultsComparator

class TestResultsComparator(unittest.TestCase):

    now = datetime.datetime.now()

    def buildResultsList(self, nbResults, startId=0):
        results = [Result("itemId_" + str(i),
                          "title_" + str(i),
                          "galleryURL_" + str(i),
                          "viewItemURL_" + str(i),
                          Price(str(i), "EUR"),
                          Interval(self.now, self.now),
                          "FR")
                   for i in range(startId, nbResults + startId)
                   ]
        return results

    def compareListResults(self, list1, list2):
        self.assertEqual(len(list1), len(list2))
        for (e1, e2) in zip(list1, list2):
            self.assertEqual(e1.itemID, e2.itemID)

    def test_compareDifferences_SimilarResults(self):
        previousResults = self.buildResultsList(10)
        currentResults = self.buildResultsList(10)

        (nbAdded, nbRemoved) = ResultsComparator().getNbDifferences(previousResults, currentResults)

        # Both results lists should be similar (elements with same itemID)
        self.assertEqual(nbAdded, 0)
        self.assertEqual(nbRemoved, 0)

    def test_compareDifferences_AddedResults(self):
        previousResults = self.buildResultsList(10)
        currentResults = self.buildResultsList(10)
        # 2 removed, thus in current results we have two more results
        del previousResults[2]
        del previousResults[5]

        (nbAdded, nbRemoved) = ResultsComparator().getNbDifferences(previousResults, currentResults)

        self.assertEqual(nbAdded, 2)
        self.assertEqual(nbRemoved, 0)

    def test_compareDifferences_RemovedResults(self):
        previousResults = self.buildResultsList(10)
        currentResults = self.buildResultsList(10)
        # 4 added, thus in current results we have 4 less results
        addedResults = self.buildResultsList(4, 10)
        previousResults += addedResults

        (nbAdded, nbRemoved) = ResultsComparator().getNbDifferences(previousResults, currentResults)

        self.assertEqual(nbAdded, 0)
        self.assertEqual(nbRemoved, 4)

    def test_compareDifferences_RemovedAndAddedResults(self):
        previousResults = self.buildResultsList(10)
        currentResults = self.buildResultsList(10)
        # 4 added, thus in current results we have 4 less results
        addedResults = self.buildResultsList(4, 10)
        previousResults += addedResults
        # and 3 removed
        del previousResults[4]
        del previousResults[8]
        del previousResults[1]

        (nbAdded, nbRemoved) = ResultsComparator().getNbDifferences(previousResults, currentResults)

        self.assertEqual(nbAdded, 3)
        self.assertEqual(nbRemoved, 4)

    def test_extractDifferences_RemovedAndAddedResults(self):
        previousResults = self.buildResultsList(10)
        currentResults = self.buildResultsList(10)
        # 4 added, thus in current results we have 4 less results
        previousResultsAdditional = self.buildResultsList(4, 10)
        previousResults += previousResultsAdditional
        # and 3 removed
        del previousResults[8]
        del previousResults[4]
        del previousResults[1]

        (addedResults, removedResults) = ResultsComparator().extractDifferentResults(previousResults, currentResults)

        self.compareListResults(addedResults, [currentResults[1],
                                               currentResults[4], currentResults[8]])
        self.compareListResults(removedResults, previousResultsAdditional)

    def test_extractDifferences_SimilarResults(self):
        previousResults = self.buildResultsList(10)
        currentResults = self.buildResultsList(10)

        (addedResults, removedResults) = ResultsComparator().extractDifferentResults(previousResults, currentResults)

        self.compareListResults(addedResults, [])
        self.compareListResults(removedResults, [])
