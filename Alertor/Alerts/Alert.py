
import uuid

class Alert(object):

    def __init__(self, keywords, categories, location="FR", uid=None,
                 sortOrder="StartTimeNewest"):
        """
        keywords = string
        categories = list of Category
        """
        self.keywords = keywords
        self.categories = categories
        self.location = location
        self.sortOrder = sortOrder

        self.uid = uuid.uuid4() if uid is None else uid
