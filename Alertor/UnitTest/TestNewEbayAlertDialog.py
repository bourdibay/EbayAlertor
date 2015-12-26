
import unittest
import sys
import os

# import in ../
sys.path.append(os.path.join(os.path.split(__file__)[0], os.pardir))
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox

from AlertDialog.NewEbayAlertDialog import NewEbayAlertDialog
from AlertsParameters.Categories.EbayCategoriesList import EbayCategoriesList
from AlertsParameters.Categories.Category import Category

class TestNewEbayAlertDialog(unittest.TestCase):

    def test_categoriesListToItems(self):        
        categoriesList = EbayCategoriesList.fromCache('EbayCategoriesTest.dict')
        dialog = NewEbayAlertDialog(categoriesList)
        
        categoriesRootItem = dialog.categoriesListToModel(categoriesList)

        self.compareCategoriesTree(categoriesList.root, categoriesRootItem)

    def compareCategoriesTree(self, rootCategory, rootItem):
        self.compareCategories(rootCategory, rootItem.category)
        for categoryChild, categoryItem in zip(rootCategory.children, rootItem.children):
            self.compareCategoriesTree(categoryChild, categoryItem)

        
    def compareCategories(self, actualCategory, expectedCategory):
        self.assertEqual(len(actualCategory.children), len(expectedCategory.children))
        self.assertEqual(actualCategory.name, expectedCategory.name)
        self.assertEqual(actualCategory.level, expectedCategory.level)
        self.assertEqual(actualCategory.ID, expectedCategory.ID)


