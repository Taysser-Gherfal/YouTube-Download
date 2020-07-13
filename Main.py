import sys
import os
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from View import *
from Model import *


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        # Main UI code goes here

        self.setWindowTitle("YouTube Downloader V1.2 - By Taysser")
        self.resize(1000,450)

        self.view = View()
        self.setCentralWidget(self.view)

        self.model = Model()

        self.view.pasted.connect(self.model.preview)
        self.model.previewing.connect(self.view.show_preview)

        self.view.submitted.connect(self.model.download)
        self.model.status.connect(self.view.show_status)

        # End main UI code
        self.show()

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())