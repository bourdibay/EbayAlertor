
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTreeView, QDialog, QLineEdit
from PyQt5.QtWidgets import QDialogButtonBox, QComboBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt

from AlertsParameters.Categories.CategoryTreeItem import CategoryTreeItem
from TreeModel import TreeModel
from AlertDialog.CategoriesWidget import CategoriesWidget
from Alerts.Alert import Alert

from AlertsParameters import StandardLocationsList

class NewEbayAlertDialog(QDialog):

    alertCreated = pyqtSignal(Alert)

    def __init__(self, categoriesList, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Create alert")

        self.resize(800, 600)
        mainLayout = QGridLayout()
        self.setLayout(mainLayout)

        # Right widget
        self.categoriesTreeItems = self.categoriesListToModel(categoriesList)
        self.categoriesWidget = CategoriesWidget(self.categoriesTreeItems)

        # left widget
        leftWidget = QWidget()
        optionsLayout = QVBoxLayout()
        leftWidget.setLayout(optionsLayout)
        optionsLayout.setAlignment(Qt.AlignTop)

        # keywords edition
        self.keywordsEdit = QLineEdit()
        self.keywordsEdit.setPlaceholderText("Keywords to search")

        # Locations
        self.locationsComboBox = QComboBox()
        sortedLocations = sorted(StandardLocationsList.locations.items())
        locationsDisplayed = ["{}_{}".format(country, code)
                              for code, country in sortedLocations]
        self.locationsComboBox.addItems(locationsDisplayed)
        locationsLabel = QLabel("Items location:")
        locationsLayout = QHBoxLayout()
        locationsLayout.addWidget(locationsLabel)
        locationsLayout.addWidget(self.locationsComboBox)

        # Sort order
        self.sortOrderComboBox = QComboBox()
        self.sortOrderComboBox.addItems(["StartTimeNewest",
                                         "BestMatch",
                                         "BidCountFewest",
                                         "BidCountMost",
                                         "CurrentPriceHighest",
                                         "EndTimeSoonest",
                                         "PricePlusShippingLowest",
                                         "PricePlusShippingHighest"])
        sortOrderLabel = QLabel("Sort by:")
        sortOrderLayout = QHBoxLayout()
        sortOrderLayout.addWidget(sortOrderLabel)
        sortOrderLayout.addWidget(self.sortOrderComboBox)

        optionsLayout.addWidget(self.keywordsEdit)
        optionsLayout.addLayout(locationsLayout)
        optionsLayout.addLayout(sortOrderLayout)
        
        mainLayout.addWidget(leftWidget, 0, 0, 1, 1)
        mainLayout.addWidget(self.categoriesWidget, 0, 1, 1, 1)

        # Standard buttons on the bottom
        self.buttons = QDialogButtonBox(self)
        self.buttons.addButton(QDialogButtonBox.Ok)
        self.buttons.addButton(QDialogButtonBox.Cancel)
        self.buttons.button(QDialogButtonBox.Ok).setText("Create new alert")
        self.buttons.button(QDialogButtonBox.Ok).clicked.connect(self.createAlert)
        self.buttons.button(QDialogButtonBox.Cancel).clicked.connect(self.close)

        mainLayout.addWidget(self.buttons, 1, 0, 1, 2)

    def categoriesListToModel(self, categoriesList):
        rootItem = CategoryTreeItem(categoriesList.root)
        def _buildItems(categoryRoot, rootItem):
            for categoryChild in categoryRoot.children:
                childItem = CategoryTreeItem(categoryChild)
                rootItem.appendChild(childItem)
                _buildItems(categoryChild, childItem)
        _buildItems(categoriesList.root, rootItem)
        return rootItem

    def __getCheckedCategories(self):
        def getCheckedCategoriesHelper(root):
            checkedCategories = []
            for child in root.children:
                if child.checkedState == Qt.Checked:
                    checkedCategories.append(child.category)
                else:
                    checkedCategories += getCheckedCategoriesHelper(child)
            return checkedCategories
        return getCheckedCategoriesHelper(self.categoriesTreeItems)

    def createAlert(self):
        # TODO : limit category list to 3 ! (it's a limitation of Ebay)
        checkedCategories = self.__getCheckedCategories()
        location = self.locationsComboBox.currentText().split('_')[-1]
        sortOrder = self.sortOrderComboBox.currentText()
        alert = Alert(self.keywordsEdit.text(), checkedCategories, location=location,
                      sortOrder=sortOrder)
        self.keywordsEdit.clear()
        self.alertCreated.emit(alert)
        self.accept()
