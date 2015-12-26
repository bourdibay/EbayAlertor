
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTreeView, QDialog, QLineEdit
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtCore import pyqtSignal, Qt

from AlertsParameters.Categories.CategoryTreeItem import CategoryTreeItem
from TreeModel import TreeModel
from Alerts.Alert import Alert

class CategoriesFilterProxy(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.textFilter = ""

    def setCategoriesFilter(self, text):
        self.textFilter = text

    def filterAcceptsRow(self, row, parent):
        index = self.sourceModel().index(row, 0, parent)
        item = index.internalPointer()
        def filterInChildren(self, item):
            ret = self.filterRegExp().indexIn(item.category.name) != -1
            if ret:
                return True
            for child in item.children:
                ret = filterInChildren(self, child)
                if ret:
                    return True
            return False
        return filterInChildren(self, item)

class CategoriesWidget(QWidget):

    def __init__(self, categoriesTreeItems):
        super().__init__()
        self.setLayout(QGridLayout())

        self.categoriesTreeItems = categoriesTreeItems

        self.categoriesView = QTreeView()
        self.categoriesView.header().hide()
        self.categoriesModel = TreeModel(self.categoriesTreeItems)

        self.categoriesProxyModel = CategoriesFilterProxy()
        self.categoriesProxyModel.setSourceModel(self.categoriesModel)

        self.categoriesView.setModel(self.categoriesProxyModel)

        self.filterCategoriesEdit = QLineEdit()
        self.filterCategoriesEdit.setPlaceholderText("Filter categories")
        self.categoriesProxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filterCategoriesEdit.textEdited.connect(self.categoriesProxyModel.setFilterRegExp)

        self.layout().addWidget(self.filterCategoriesEdit, 0, 1, 1, 1)
        self.layout().addWidget(self.categoriesView, 1, 1, 1, 1)
