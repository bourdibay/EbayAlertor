
import TreeModel
from PyQt5.Qt import Qt
from PyQt5.QtCore import QVariant

class CategoryTreeItem(TreeModel.TreeItem):

    def __init__(self, category, parent=None):
        super().__init__(parent)

        self.category = category

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self.category.name
        elif role == Qt.CheckStateRole and index.column() == 0:
            return self.checkedState
        return QVariant()

    def setData(self, index, value, role):
        if role == Qt.CheckStateRole and index.column() == 0:
            self.setState(value)
            return True
        return False

    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsTristate
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled
