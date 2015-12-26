
import sys
import os

# import in ../
sys.path.append(os.path.join(os.path.split(__file__)[0], os.pardir))

import unittest
from Executors.ImageDownloadExecutor import ImageDownloadExecutor
from CacheDiskIO import CacheDiskIO

class TestImageDownloadExecutor(unittest.TestCase):

    def test_downloadImage(self):
        url = "https://www.python.org/static/img/python-logo.png"
        executor = ImageDownloadExecutor(url)

        destinationFile = CacheDiskIO().createFullpath(executor.filename)
        if os.path.exists(destinationFile):
            os.remove(destinationFile)

        executor.execute()

        # Means I deleted the wrong file, and the rest of the test is not relevant.
        self.assertEqual(executor.result, destinationFile)

        self.assertTrue(os.path.exists(executor.result))
