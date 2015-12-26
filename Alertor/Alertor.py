
import sys

from PyQt5.QtWidgets import QApplication
import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow.MainWindow("Alertor")
    window.show()
    sys.exit(app.exec_())
