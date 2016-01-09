
class ResultsComparator(object):

    def getNbDifferences(self, previousResults, currentResults):
        """Compare the previous and current results given and return the number of results
        added and removed.
        Two results are equal if they have the same itemID.

        Args:
          previousResults: list of Result
          currentResults: list of Result

        Return:
          tuple of (number of newly added results, number of removed results)
        """
        print("[ResultsComparator] getNbDifferences()")
        (addedResults, removedResults) = self.extractDifferentResults(previousResults, currentResults)
        return (len(addedResults), len(removedResults))

    def extractDifferentResults(self, previousResults, currentResults):
        """Compare the previous and current results given and return 
        a list of added and a list of removed results.
        Two results are equal if they have the same itemID.

        Args:
          previousResults: list of Result
          currentResults: list of Result

        Return:
          tuple of (list of newly added results, list of removed results)
        """
        print("[ResultsComparator] extractDifferentResults()")        
        if not previousResults:
            return ([], [])
        previousSet = set([result.itemID for result in previousResults])
        currentSet = set([result.itemID for result in currentResults])
        removedSet = previousSet - currentSet
        addedSet = currentSet - previousSet

        addedResults = [result for result in currentResults if result.itemID in addedSet]
        removedResults = [result for result in previousResults if result.itemID in removedSet]
        return (addedResults, removedResults)
