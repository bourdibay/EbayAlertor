
import ebaysdk
import ast
from AlertsParameters.Categories.Category import Category

class EbayCategoriesList(object):

    def __init__(self):
        self.root = Category("root", -1, 0)

    @staticmethod
    def fromEbayResquest(cache):
        categoriesList = EbayCategoriesList()
        api = ebaysdk.shopping.Connection(config='ebay.yaml')
        categoriesList.__buildCategoriesFromEbayRequests(self.categoryRoot, api)
        return categoriesList

    @staticmethod
    def fromCache(cache):
        categoriesList = EbayCategoriesList()
        with open(cache, 'r') as fd:
            categoriesList.__buildCategoriesFromStream(categoriesList.root, fd)
        return categoriesList

    def __buildCategoriesFromStream(self, root, stream):
            lastRoot = root
            for line in stream:
                attr = ast.literal_eval(line)
                child = Category(attr["CategoryName"],
                                 int(attr["CategoryID"]),
                                 int(attr["CategoryLevel"]))
                while lastRoot.level >= child.level:
                    lastRoot = lastRoot.parent
                lastRoot.children.append(child)
                child.parent = lastRoot
                lastRoot = child

    def __buildCategoriesFromEbayRequests(self, root, api):
        resp = api.execute('GetCategoryInfo', {'CategoryID' : root.id,
                                               'IncludeSelector' : 'ChildCategories'})
        category_array = resp.reply.get('CategoryArray').get('Category')
        for child_category in category_array:
            if child_category.get('CategoryID') != root_category.id:
                child = Category(child_category.get('CategoryName'),
                                 int(child_category.get('CategoryID')),
                                 int(child_category.get('CategoryLevel')))
                root.children.append(child)
                if child_category.get('LeafCategory') == 'false':
                    self.__buildCategoriesFromEbayRequests(root, api)
