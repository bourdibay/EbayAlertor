#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Run all the tests located in the current directory.
#

import sys
import unittest
import multiprocessing
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)

    suite = unittest.TestSuite()
    testModules = {
        "TestEbayCategoriesList": True,
        "TestNewEbayAlertDialog": True,
        "TestImageDownloadExecutor": True,
        "TestResultsDiskIO": True,
        "TestEbayFindItemsExecutor": True,
        "TestEbayShippingFeesExecutor": True,
        "TestResultsComparator": True
        }
    for module, enabled in testModules.items():
        if enabled:
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(module))

    res = unittest.TextTestRunner().run(suite)
    if not res.wasSuccessful():
        sys.exit(1)
