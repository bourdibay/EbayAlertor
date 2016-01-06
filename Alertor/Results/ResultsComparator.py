
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
        print("[ResultsComparator] compareNbDifferences()")        
        if not previousResults:
            return (len(currentResults), 0)
        previousSet = set([result.itemID for result in previousResults])
        currentSet = set([result.itemID for result in currentResults])
        removedResults = previousSet - currentSet
        addedResults = currentSet - previousSet
        return (len(addedResults), len(removedResults))
