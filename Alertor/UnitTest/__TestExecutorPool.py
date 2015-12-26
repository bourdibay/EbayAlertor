import sys
import os

# import in ../
sys.path.append(os.path.join(os.path.split(__file__)[0], os.pardir))

import unittest
import time
import random

from PyQt5.QtWidgets import QApplication, QMainWindow

from AlertsParameters.Categories.Category import Category
from Alerts.Alert import Alert
from Executors.ExecutorsPool import ExecutorsPool
from Executors.Executor import Executor
from Executors.EbayFindItemsExecutor import EbayFindItemsExecutor

class TestExecutor(EbayFindItemsExecutor):
    def __init__(sel):
        super().__init__(Alert("final fantasy",
                               [Category("Video Games & Consoles",
                                        1249, 1)]))

    def execute(self):
        r = random.randint(1, 10)
        time.sleep(r)
        print("Start {}".format(r))
        super().execute()

class TestExecutorsPool(unittest.TestCase):

    def test_executeSeveralRequests(self):

        executorsPool = ExecutorsPool()
        executorsPool.executorFinished.connect(self.taskExecuted)

        self.addExecutor(executorsPool)
        self.addExecutor(executorsPool)
        self.addExecutor(executorsPool)
        self.addExecutor(executorsPool)
        self.addExecutor(executorsPool)

    def addExecutor(self, executorsPool):
        executor = TestExecutor()
        executorsPool.addExecutor(executor)

    def taskExecuted(self, executor):
        print("Result of executor = {}".format(executor))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.show()

    test = TestExecutorsPool()
    test.test_executeSeveralRequests()

    sys.exit(app.exec_())
