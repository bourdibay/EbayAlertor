
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QListView, QHBoxLayout, QToolButton
from PyQt5.QtCore import Qt, QStringListModel, QEvent, pyqtSignal
from PyQt5.QtGui import QColor

from Alerts.Alert import Alert

class AlertWidget(QWidget):

    MAX_WIDTH = 350

    clicked = pyqtSignal()
    closed = pyqtSignal()

    def __init__(self, alert, parent=None):
        super().__init__(parent)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.alert = alert

        self.topLayout = QHBoxLayout() # contains close button + title
        self.keywordsLabel = QLabel(self.alert.keywords)
        keywordFont = self.keywordsLabel.font()
        keywordFont.setPointSize(keywordFont.pointSize() + 2)
        keywordFont.setBold(True)
        self.keywordsLabel.setFont(keywordFont)
        self.keywordsLabel.setAlignment(Qt.AlignCenter)

        self.topLayout.addWidget(self.keywordsLabel)
        closeButton = QToolButton()
        closeButton.setText("X")
        closeButton.setStyleSheet("""
        QToolButton {
        color: black;
        font: bold;
        background-color: #FF3333;
        border: 2px solid #FF3333;
        border-radius: 9px;
        }
        QToolButton:hover {
        background-color: #FF0000;
        border: 2px solid #FF0000;
        }
        QToolButton:disabled {
        background-color: #FF8A8A;
        border: 2px solid #FF8A8A;
        }
        """)
        closeButton.clicked.connect(lambda: self.closed.emit())

        self.topLayout.addWidget(closeButton)
        self.topLayout.setContentsMargins(0, 0, 0, 0)

        self.mainLayout.addLayout(self.topLayout)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        categoryNames = [category.name for category in alert.categories]
        self.categoriesModel = QStringListModel(categoryNames)
        self.categoriesView = QListView()
        self.categoriesView.setModel(self.categoriesModel)
        self.categoriesModel.flags = lambda index: Qt.ItemIsEnabled | Qt.ItemNeverHasChildren

        self.categoriesView.setMaximumSize(self.MAX_WIDTH, 55)
        self.mainLayout.addWidget(self.categoriesView)
        self.setMaximumWidth(self.MAX_WIDTH)

        resultSummaryLayout = QHBoxLayout()
        self.addedResultsWidget = QLabel()
        self.removedResultsWidget = QLabel()
        self.updateResultsSummary("0", "0")
        self.addedResultsWidget.setAlignment(Qt.AlignCenter)
        self.removedResultsWidget.setAlignment(Qt.AlignCenter)
        resultSummaryLayout.addWidget(self.addedResultsWidget)
        resultSummaryLayout.addWidget(self.removedResultsWidget)
        self.mainLayout.addLayout(resultSummaryLayout)

        self.mainLayout.addWidget(QLabel("In store {}".format(self.alert.location)))
        self.mainLayout.addWidget(QLabel("Sort by {}".format(self.alert.sortOrder)))

        self.setAutoFillBackground(True)
        self.setStyleSheetLeave()

        self.installEventFilter(self)

    def updateResultsSummary(self, nbAddedResults, nbRemovedResults):
        self.addedResultsWidget.setText("Added: " + str(nbAddedResults))
        self.removedResultsWidget.setText("Removed: " + str(nbRemovedResults))

        def __createStylesheet(color):
            return """
            border: 2px solid {color};
            border-radius: 10px;
            background-color: {color};
            padding: 2px;""".format(color=color)

        colorAddedResult = __createStylesheet("green" if str(nbAddedResults) != "0" else "grey")
        colorRemovedResult = __createStylesheet("red" if str(nbRemovedResults) != "0" else "grey")
        self.addedResultsWidget.setStyleSheet(colorAddedResult)
        self.removedResultsWidget.setStyleSheet(colorRemovedResult)

    def setStyleSheetEnter(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor("#8DF6FC"))
        self.setPalette(p)

    def setStyleSheetLeave(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor("#CED6D6"))
        self.setPalette(p)

    def setStyleSheetMousePress(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor("#C0ECFA"))
        self.setPalette(p)

    def eventFilter(self, obj, event):
        if not isinstance(obj, AlertWidget):
            return super().eventFilter(obj, event)

        if event.type() == QEvent.Enter:
            obj.setStyleSheetEnter()
        elif event.type() == QEvent.Leave:
            obj.setStyleSheetLeave()
        elif event.type() == QEvent.MouseButtonRelease:
            if obj.isEnabled():
                obj.setStyleSheetEnter()
                self.clicked.emit()
        elif event.type() == QEvent.MouseButtonPress:
            obj.setStyleSheetMousePress()
        return super().eventFilter(obj, event)
