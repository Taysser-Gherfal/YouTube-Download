from Model import *
from View import *



class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        # Main UI code goes here

        self.setWindowTitle("YouTube Downloader V1.5 - By Taysser")
        self.resize(1000, 350)

        self.view = View()
        self.setCentralWidget(self.view)

        self.model = Model()
        self.download_thread = qtc.QThread()
        self.model.moveToThread(self.download_thread)
        self.model.previewing.connect(self.view.show_preview)
        self.model.status.connect(self.view.show_status)
        self.download_thread.start()

        self.view.pasted.connect(self.model.preview)
        self.view.submitted.connect(self.model.download)
        self.view.play_url.connect(self.model.play)

        # End main UI code
        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.

    # Dark Theme
    app.setStyle('Fusion')
    palette = qtg.QPalette()
    palette.setColor(qtg.QPalette.Window, qtg.QColor(53,53,53))
    palette.setColor(qtg.QPalette.WindowText, qtc.Qt.white)
    palette.setColor(qtg.QPalette.Base, qtg.QColor(15,15,15))
    palette.setColor(qtg.QPalette.AlternateBase, qtg.QColor(53,53,53))
    palette.setColor(qtg.QPalette.ToolTipBase, qtc.Qt.white)
    palette.setColor(qtg.QPalette.ToolTipText, qtc.Qt.white)
    palette.setColor(qtg.QPalette.Text, qtc.Qt.white)
    palette.setColor(qtg.QPalette.Button, qtg.QColor(53,53,53))
    palette.setColor(qtg.QPalette.ButtonText, qtc.Qt.white)
    palette.setColor(qtg.QPalette.BrightText, qtc.Qt.red)
    palette.setColor(qtg.QPalette.Highlight, qtg.QColor(45,100,197).lighter())
    palette.setColor(qtg.QPalette.HighlightedText, qtc.Qt.black)
    app.setPalette(palette)

    mw = MainWindow()
    sys.exit(app.exec())
