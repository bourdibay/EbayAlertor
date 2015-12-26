
from PyQt5.QtCore import QAbstractItemModel, QObject, QVariant, QModelIndex
from PyQt5.Qt import Qt

class TreeItem(QObject):

    def __init__(self, parent=None):
        super().__init__()

        self.children = []
        self.parent = parent
        self.checkedState = Qt.Unchecked

        self._nbSubItems = 0

    def getChildrenNumber(self):
        return len(self.children)

    def getChild(self, idx):
        if idx < 0 or idx >= self.getChildrenNumber():
            return None
        return self.children[idx]

    def appendChild(self, child):
        self.children.append(child)
        child.parent = self
        
        parent = self
        while parent:
            parent._nbSubItems += 1
            parent = parent.parent

    def __setCheckedStatesChildren(self, state):
        self.checkedState = state
        for child in self.children:
            child.__setCheckedStatesChildren(state)

    def setState(self, toState):
        self.__setCheckedStatesChildren(toState)
        parent = self.parent
        while parent:
            nb_checked = 0
            nb_checked_partially = 0
            for child in parent.children:
                if child.checkedState == Qt.Checked:
                    nb_checked += 1
                elif child.checkedState == Qt.PartiallyChecked:
                    nb_checked_partially += 1

            if nb_checked == 0 and nb_checked_partially == 0:
                parent.checkedState = Qt.Unchecked
            elif nb_checked == len(parent.children):
                parent.checkedState = Qt.Checked
            else:
                parent.checkedState = Qt.PartiallyChecked
            parent = parent.parent

    def setOppositeState(self):
        current_state = self.checkedState
        if current_state == Qt.PartiallyChecked or current_state == Qt.Unchecked:
            toState = Qt.Checked
        elif current_state == Qt.Checked:
            toState = Qt.Unchecked
        self.setState(toState)

    def row(self):
        if self.parent:
            for i, child in enumerate(self.parent.children):
                if child == self:
                    return i
        return 0;


class TreeModel(QAbstractItemModel):

    def __init__(self, root):
        super().__init__()
        self.root = root

    def columnCount(self, parent):
        return self.root.columnCount(parent)

    def rowCount(self, parent):
        item = self.getItem(parent)
        return item.getChildrenNumber()

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        item = self.getItem(index)
        return item.data(index, role)        

    def index(self, row, col, parent):
        if not self.hasIndex(row, col, parent):
            return QModelIndex()
        if not parent.isValid():
            parentItem = self.root
        else:
            parentItem = parent.internalPointer()
        child = parentItem.getChild(row)
        if child:
            return self.createIndex(row, col, child)
        return QModelIndex()

    def getItem(self, index):
        if index.isValid():
            return index.internalPointer()
        return self.root

    # TODO: bugged in some cases, to be recoded one day...
    def setData(self, index, value, role):
        if not index.isValid():
            return False
        item = index.internalPointer()
        if item.setData(index, value, role):
            if not item.children:
                lastIndex = index
            else:
                row = 0
                lastIndex = QModelIndex()
                while True:
                    rowIndex = self.index(row, 0, self.parent(index))
                    if not rowIndex.isValid():
                        break
                    lastIndex = rowIndex
                    row += 1

            startIndex = self.index(0, 0, QModelIndex())
            self.dataChanged.emit(startIndex, lastIndex)
            return True
        return False

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        child = index.internalPointer()
        parent = child.parent
        if parent == self.root:
            return QModelIndex()
        return self.createIndex(parent.row(), 0, parent)

    def flags(self, index):
        child = index.internalPointer()
        if child:
            return child.flags(index)
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled
