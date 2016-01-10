import sys
import os

# import in ../
sys.path.append(os.path.join(os.path.split(__file__)[0], os.pardir))

import unittest
import time
import random
from threading import Lock

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
        print("Start thread which slept {}".format(r))
        super().execute()

class TestExecutorsPool(unittest.TestCase):

    def __init__(self, app):
        super().__init__()
        self.app = app

    def test_executeSeveralRequests(self):

        executorsPool = ExecutorsPool()
        executorsPool.executorFinished.connect(self.taskExecuted)

        self.lock = Lock()
        self.nbExecutors = 5

        self.addExecutor(executorsPool)
        self.addExecutor(executorsPool)
        self.addExecutor(executorsPool)
        self.addExecutor(executorsPool)
        self.addExecutor(executorsPool)

    def addExecutor(self, executorsPool):
        executor = TestExecutor()
        executorsPool.addExecutor(executor)

    def taskExecuted(self, executor):
        with self.lock:
            self.nbExecutors -= 1
            print("Result of executor = {}, remain {} executors to finish".format(executor, self.nbExecutors))
            if self.nbExecutors <= 0:
                print("Success")
                app.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.show()

    test = TestExecutorsPool(app)
    test.test_executeSeveralRequests()

    sys.exit(app.exec_())
