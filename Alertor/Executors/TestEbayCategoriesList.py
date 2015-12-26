
import sys
import os

# import in ../
sys.path.append(os.path.join(os.path.split(__file__)[0], os.pardir))

import unittest
from AlertsParameters.Categories.EbayCategoriesList import EbayCategoriesList
from AlertsParameters.Categories.Category import Category

class TestEbayCategoriesList(unittest.TestCase):

    def test_lineToCategory(self):
        """ Test that we can convert one well formatted line from ebay's http response
        into a Category object.
        """
        expectedRoot = Category("root", -1, 0)
        first = Category("First", 11, 1)
        first1 = Category("First1", 111, 2)
        first1_1 = Category("First1_1", 1111, 3)
        first2 = Category("First2", 112, 2)
        second = Category("Second", 22, 1)
#{'CategoryName': 'First', 'CategoryParentID': '-1', 'CategoryIDPath': '11', 'CategoryLevel': '1', 'CategoryNamePath': 'First', 'LeafCategory': 'false', 'CategoryID': '11'}
#{'CategoryName': 'First1', 'CategoryParentID': '11', 'CategoryIDPath': '11:111', 'CategoryLevel': '2', 'CategoryNamePath': 'First:First1', 'LeafCategory': 'false', 'CategoryID': '111'}
#{'CategoryName': 'First1_1', 'CategoryParentID': '111', 'CategoryIDPath': '11:111:1111', 'CategoryLevel': '3', 'CategoryNamePath': 'First:First1:First1_1', 'LeafCategory': 'true', 'CategoryID': '1111'}
#{'CategoryName': 'First2', 'CategoryParentID': '11', 'CategoryIDPath': '11:112', 'CategoryLevel': '2', 'CategoryNamePath': 'First:First2', 'LeafCategory': 'true', 'CategoryID': '112'}
#{'CategoryName': 'Second', 'CategoryParentID': '-1', 'CategoryIDPath': '22', 'CategoryLevel': '1', 'CategoryNamePath': 'Second', 'LeafCategory': 'false', 'CategoryID': '22'}
        expectedRoot.children.append(first)
        first.children.append(first1)
        first.children.append(first2)
        first1.children.append(first1_1)
        expectedRoot.children.append(second)

        actualCategoryList = EbayCategoriesList.fromCache('EbayCategoriesTest.dict')

        self.compareCategories(actualCategoryList.root, expectedRoot)
        for (actual, expected) in zip(actualCategoryList.root.children, expectedRoot.children):
            self.compareCategories(actual, expected) # level 1
            for (actual1, expected1) in zip(actual.children, expected.children):
                self.compareCategories(actual1, expected1) # level 2
                for (actual2, expected2) in zip(actual1.children, expected1.children):
                    self.compareCategories(actual2, expected2) # level 3

    def compareCategories(self, actualCategory, expectedCategory):
        self.assertEqual(len(actualCategory.children), len(expectedCategory.children))
        self.assertEqual(actualCategory.name, expectedCategory.name)
        self.assertEqual(actualCategory.level, expectedCategory.level)
        self.assertEqual(actualCategory.ID, expectedCategory.ID)
