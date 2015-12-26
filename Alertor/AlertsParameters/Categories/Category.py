
class Category(object):
    def __init__(self, name, ID, level):
        self.name = name
        self.ID = ID
        self.level = level

        self.children = []
        self.parent = None
