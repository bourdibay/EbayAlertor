import datetime

import ebaysdk.finding

from Executors.Executor import Executor

class EbayFindItemsExecutor(Executor):
    """Request all the items matching the search filters specified in Alert.
    """

    apiConnection = ebaysdk.finding.Connection(config_file="ebay.yaml", timeout=60)

    def __init__(self, alert):
        super().__init__()
        self.alert = alert

    def execute(self):
        print("[EbayFindItemsExecutor] execute()")
        categoryId = [str(category.ID) for category in self.alert.categories]
        requestArgs = {
            "keywords": self.alert.keywords,
            "categoryId": categoryId,
            "itemFilter": [
                { "name": "LocatedIn",
                 "value": self.alert.location
                 }
                ],
            "paginationInput": {
                "pageSize": 100
                },
            "sortOrder": self.alert.sortOrder
            }
        try:
            response = self.apiConnection.execute("findItemsAdvanced", requestArgs)

            if response.reply.ack == "Success":
                item = response.reply.searchResult.item[0]
                self.result = [item for item in response.reply.searchResult.item]
            else:
                pass # TODO: handle errors
        except Exception as e:
            print("[EbayFindItemsExecutor] Exception while finding items: {}".format(e))
