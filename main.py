import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication
import MainUi

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        main_win = MainUi.Ui_MainWindow()
        w = QtWidgets.QMainWindow()
        w.setAcceptDrops(True)
        main_win.setupUi(w)
        w.show()
        sys.exit(app.exec())
    except KeyboardInterrupt:
        sys.exit('Exit')
