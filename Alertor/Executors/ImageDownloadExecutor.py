
import urllib.request
import os

from Executors.Executor import Executor
from CacheDiskIO import CacheDiskIO

class ImageDownloadExecutor(Executor):
    """Download the image URL specified and store it in CacheDiskIO.cacheDirectory.
    """

    def __init__(self, imgURL):
        super().__init__()
        self.url = imgURL
        if self.url:
            self.filename = self.url.replace("/", "_").replace(":", "_")
        else:
            self.filename = ""

    def execute(self):
        if self.filename:
            self.result = CacheDiskIO().createFullpath(self.filename)
            if not os.path.exists(self.result):
                try:
                    urllib.request.urlretrieve(self.url, self.result)
                except Exception as e:
                    print("[ImageDownloadExecutor] Exception while downloading image URL: {}".format(e))
            #else:
            #    print("[ImageDownloadExecutor] Do not download {}".format(self.result))
