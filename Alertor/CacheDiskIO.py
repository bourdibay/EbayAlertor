
import os

from PyQt5.QtCore import QDir

class CacheDiskIO(object):

    def __init__(self):
        tempDirectory = QDir.tempPath()
        cacheDirectory = "./AlertorCache/"
        self.cacheDirectory = self.normalizePath(os.path.join(tempDirectory, cacheDirectory))
        if not os.path.exists(self.cacheDirectory):
            os.makedirs(self.cacheDirectory)

    def createFullpath(self, filename):
        return self.normalizePath(os.path.join(self.cacheDirectory, filename))

    def normalizePath(self, path):
        return os.path.normpath(os.path.abspath(path))
