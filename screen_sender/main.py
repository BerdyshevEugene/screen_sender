import sys
from PyQt5.QtWidgets import *
from ui.main_window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    mw = MainWindow()
    mw.hide()
    sys.exit(app.exec_())
