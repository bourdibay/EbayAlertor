import datetime

import ebaysdk.shopping

from Executors.Executor import Executor

class EbayShippingFeesExecutor(Executor):
    """Request the shipping fees of an item (= Result).
    """

    apiConnection = ebaysdk.shopping.Connection(config_file="ebay.yaml", timeout=60)

    def __init__(self, itemID, destinationCountry):
        """
        Args:
          itemID: from Result.itemID
          destinationCountry: http://developer.ebay.com/DevZone/Shopping/docs/CallRef/extra/GtShppngCsts.Rqst.DstntnCntryCd.html
        """
        super().__init__()
        self.itemID = itemID
        self.destinationCountry = destinationCountry

    def execute(self):
        requestArgs = {
            "ItemID": self.itemID,
            "DestinationCountryCode": self.destinationCountry
            }
        try:
            response = self.apiConnection.execute("GetShippingCosts", requestArgs)

            if response.reply.Ack == "Success":
                cost = response.reply.ShippingCostSummary.ListedShippingServiceCost
                self.result = (cost.get("value"), cost.get("_currencyID"))
            else:
                pass # TODO: handle errors
        except Exception as e:
            print("[EbayShippingFeesExecutor] Exception while retrieving shipping cost: {}".format(e))
