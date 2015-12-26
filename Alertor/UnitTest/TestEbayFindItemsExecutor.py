
import sys
import os

# import in ../
sys.path.append(os.path.join(os.path.split(__file__)[0], os.pardir))

import unittest
from Results.ResultsDiskIO import ResultsDiskIO
from Alerts.Alert import Alert
from Results.Result import Result
from Executors.EbayFindItemsExecutor import EbayFindItemsExecutor
from AlertsParameters.Categories.Category import Category

class TestEbayFindItemsExecutor(unittest.TestCase):

    def test_executeBasicRequest(self):
        alert = Alert("final fantasy",
                      [Category("Video Games & Consoles",
                                1249, 1)])
        executor = EbayFindItemsExecutor(alert)

        executor.execute()

        self.assertIsNotNone(executor.result)
