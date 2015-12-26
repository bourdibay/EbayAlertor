
import datetime

class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.delta = self.end - datetime.datetime.now()

    def strfdelta(self, fmt):
        """ From https://stackoverflow.com/questions/8906926/formatting-python-timedelta-objects
        """
        d = self.deltaToDict()
        return fmt.format(**d)

    def deltaToDict(self):
        d = { "days": self.delta.days }
        d["hours"], rem = divmod(self.delta.seconds, 3600)
        d["minutes"], d["seconds"] = divmod(rem, 60)
        return d

class Price(object):
    def __init__(self, value, currency):
        self.value = value
        self.currency = currency

class Result(object):

    def __init__(self, itemID, title, imgURL, itemURL, price,
                 interval, country):
        self.itemID = itemID
        self.title = title
        self.imgURL = imgURL
        self.itemURL = itemURL
        self.price = price
        self.interval = interval

        self.country = country

        self.imageInCache = None
        self.shippingCost = Price("N/A", "N/A")

    @staticmethod
    def createFromSerialized(info):
        result = Result(info.get("itemId"),
                        info.get("title"),
                        info.get("galleryURL"),
                        info.get("viewItemURL"),
                        Price(info.get("sellingStatus").get("currentPrice").get("value"),
                              info.get("sellingStatus").get("currentPrice").get("_currencyId")),
                        Interval(info.get("listingInfo").get("startTime"),
                                 info.get("listingInfo").get("endTime")),
                        info.get("country")
                        )
        shippingCost = info.get("shippingCost", None)
        if shippingCost:
            result.shippingCost = Price(shippingCost.get("value", "N/A"),
                                        shippingCost.get("currency", "N/A"))
        return result

    def serialize(self):
        return {
            "itemId": self.itemID,
            "title": self.title,
            "galleryURL" : self.imgURL,
            "viewItemURL" : self.itemURL,
            "sellingStatus" : {
                "currentPrice" : {
                "value" : self.price.value,
                "_currencyId" : self.price.currency
                }
                },
            "listingInfo" : {
                "endTime" : self.interval.end,
                "startTime" : self.interval.start
                },
            "shippingCost": {
                "value": self.shippingCost.value,
                "currency": self.shippingCost.currency
                },
            "country": self.country
            }
