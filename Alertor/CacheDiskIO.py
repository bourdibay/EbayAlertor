
import os

from PyQt5.QtCore import QDir

class CacheDiskIO(object):

    def __init__(self):
        tempDirectory = QDir.tempPath()
        cacheDirectory = "./AlertorCache/"
        self.fullDir = os.path.join(tempDirectory, cacheDirectory)
        if not os.path.exists(self.fullDir):
            os.makedirs(self.fullDir)

    def createFullpath(self, filename):
        return os.path.join(self.fullDir, filename)
