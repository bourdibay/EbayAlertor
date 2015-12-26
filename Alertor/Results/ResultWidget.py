
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QColor, QPalette
from PyQt5.QtCore import Qt

from Results.Result import Result

class ResultWidget(QWidget):
    def __init__(self, result, parent=None):
        super().__init__(parent)

        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.setBackgroundColor(QColor("#EBFCAE"))

        self.result = result

        self.title = QLabel("""<a href='{}'>{}</a>""".format(self.result.itemURL,
                                                             self.result.title))
        self.title.setTextFormat(Qt.RichText)
        self.title.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.title.setOpenExternalLinks(True)

        self.price = QLabel("Current price: <b>{} {}</b>".format(self.result.price.value,
                                                                 self.result.price.currency))
        self.price.setTextFormat(Qt.RichText)

        self.shippingCost = QLabel()
        self.shippingCost.setTextFormat(Qt.RichText)
        self.refreshShippingCost()

        self.thumb = QLabel()
        self.thumb.setMaximumWidth(140)
        self.refreshThumb()

        startAuction = QLabel("Start: {}".format(self.result.interval.start.strftime("%c")))
        endAuction = QLabel("End: {}".format(self.result.interval.end.strftime("%c")))

        deltaDict = self.result.interval.deltaToDict()
        strDelta = "{hours}h {minutes}m {seconds}s"
        if deltaDict["days"] > 0:
            strDelta = "{days} days " + strDelta
        deltaAuction = QLabel("Finished in: {}".format(self.result.interval.strfdelta(strDelta)))

        detailLayout = QVBoxLayout()
        detailLayout.setAlignment(Qt.AlignTop)
        detailLayout.addWidget(self.title)
        detailLayout.addWidget(self.price)
        detailLayout.addWidget(self.shippingCost)
        detailLayout.addWidget(startAuction)
        detailLayout.addWidget(endAuction)
        detailLayout.addWidget(deltaAuction)

        self.mainLayout.addWidget(self.thumb, 0, 0, 2, 1)
        self.mainLayout.addLayout(detailLayout, 0, 1, 1, 1)

    def refreshThumb(self):
        if self.result.imageInCache:
            pixmap = QPixmap(self.result.imageInCache)
        else:
            pixmap = QPixmap()
        self.thumb.setPixmap(pixmap)

    def refreshShippingCost(self):
        self.shippingCost.setText("Shipping cost: <b>{} {}</b>".format(self.result.shippingCost.value,
                                                                       self.result.shippingCost.currency))

    def setBackgroundColor(self, color):
        p = self.palette()
        p.setColor(QPalette.Background, color)
        self.setAutoFillBackground(True)
        self.setPalette(p)
