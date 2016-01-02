
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QStyle
from PyQt5.QtCore import Qt
import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow.MainWindow("Alertor")
    # Put in the center of the screen.
    window.setGeometry(QStyle.alignedRect(Qt.LeftToRight,
                                          Qt.AlignCenter,
                                          window.size(),
                                          app.desktop().availableGeometry()))
    window.show()
    sys.exit(app.exec_())
