
import sys
import os

# import in ../
sys.path.append(os.path.join(os.path.split(__file__)[0], os.pardir))

import unittest
from Results.ResultsDiskIO import ResultsDiskIO
from Alerts.Alert import Alert
from Results.Result import Result
from Executors.EbayFindItemsExecutor import EbayFindItemsExecutor
from Executors.EbayShippingFeesExecutor import EbayShippingFeesExecutor
from AlertsParameters.Categories.Category import Category

class TestEbayShippingFeesExecutor(unittest.TestCase):

    def test_executeBasicRequest(self):
        alert = Alert("final fantasy",
                      [Category("Video Games & Consoles", 1249, 1)])
        findExecutor = EbayFindItemsExecutor(alert)
        findExecutor.execute()
        self.assertIsNotNone(findExecutor.result)
        result = Result.createFromSerialized(findExecutor.result[0])

        costExecutor = EbayShippingFeesExecutor(result.itemID, "FR")
        costExecutor.execute()
        self.assertIsNotNone(costExecutor.result)
        