
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QStyle
from PyQt5.QtCore import Qt
import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Got a lot of errors related to Gtk on Linux:
    # Gtk-CRITICAL **: IA__gtk_widget_style_get: assertion 'GTK_IS_WIDGET (widget)' failed
    # A possible fix is provided here, by setting the fusion style:
    # http://stackoverflow.com/questions/35351024/pyqt5-gtk-critical-ia-gtk-widget-style-get-assertion-gtk-is-widget-widg    
    if sys.platform == "linux" or sys.platform == "linux2":
        app.setStyle("fusion")
 
    window = MainWindow.MainWindow("Alertor")
    # Put in the center of the screen.
    window.setGeometry(QStyle.alignedRect(Qt.LeftToRight,
                                          Qt.AlignCenter,
                                          window.size(),
                                          app.desktop().availableGeometry()))
    window.show()
    sys.exit(app.exec_())
