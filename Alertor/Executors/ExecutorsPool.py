
import concurrent.futures

from threading import Timer, Lock

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

from Executors.Executor import Executor

class ExecutorsPool(QObject):

    executorFinished = pyqtSignal(Executor)

    def __init__(self, name="ExecutorsPool", callbackDone=None, max_workers=20):
        super().__init__()

        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.name = name

        self.executors = {}
        self.lock = Lock()

        self.callbackDone = callbackDone

    def shutdown(self):
        self.pool.shutdown(wait=False)

    def addExecutor(self, executor):
        shouldRunTimer = not self.executors
        futureResult = self.pool.submit(executor.execute)

        self.lock.acquire()
        self.executors[futureResult] = executor
        self.lock.release()

        futureResult.add_done_callback(self.callback_done)

    def callback_done(self, futureResult):
        self.lock.acquire()
        executor = self.executors[futureResult]
        del self.executors[futureResult]
        self.lock.release()

        if self.callbackDone:
            self.callbackDone(executor)

        self.executorFinished.emit(executor)
