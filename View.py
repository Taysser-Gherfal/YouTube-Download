from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class View(qtw.QWidget):

    pasted = qtc.pyqtSignal(str)
    submitted = qtc.pyqtSignal(str, str, str, int)

    def __init__(self):

        super().__init__()
        # Main UI code
        self.url = qtw.QLineEdit()
        self.url.setToolTip("URL")
        self.folder = qtw.QLineEdit()
        self.folder.setReadOnly(True)
        download_button = qtw.QPushButton("Download", self)
        folder_button = qtw.QPushButton("...", self)
        folder_button.setMaximumWidth(60)
        folder_button.setMaximumHeight(35)

        #self.spin_box = qtw.QDial()
        self.combo_box = qtw.QComboBox()

        self.lable = qtw.QLabel()
        self.time_lable = qtw.QLabel()
        self.progress = qtw.QProgressBar()
        self.lcd2 = qtw.QLCDNumber()
        self.text = qtw.QTextBrowser()

        # Main UI layout
        layout = qtw.QGridLayout()
        self.setLayout(layout)

        # Right col layout
        right_layout = qtw.QVBoxLayout()
        layout.addLayout(right_layout, 2, 1)
        
        # Adding widgets to the main UI
        layout.addWidget(self.url, 0, 0)
        layout.addWidget(download_button, 4, 1)
        layout.addWidget(self.folder, 3, 0)
        layout.addWidget(folder_button, 3, 1)
        layout.addWidget(self.combo_box, 1, 0)
        layout.addWidget(self.text, 2, 0)
        layout.addWidget(self.lable, 0, 1)
        layout.addWidget(self.progress, 4, 0)

        # Adding widgets to the right col
        right_layout.addWidget(self.lcd2)
        right_layout.addWidget(self.time_lable)
        self.lcd2.setMaximumHeight(50)
        self.time_lable.setAlignment(qtc.Qt.AlignTop)
        self.time_lable.setAlignment(qtc.Qt.AlignRight)

        # Setting lable text
        self.lable.setText("Status...")
        self.time_lable.setText("minutes")

        # Connecting the download button and the URL change
        download_button.clicked.connect(self.download)
        self.url.textChanged.connect(self.get_preview)
        folder_button.clicked.connect(self.openFolder)

    def openFolder(self):
        loc = qtw.QFileDialog.getExistingDirectory(self, "Select Directory")
        self.folder.setText(loc)

    def download(self):
        url = self.url.text()
        folder = str(self.folder.text())
        library = self.lable.text()
        selected = self.combo_box.currentIndex()
        self.submitted.emit(url, folder, library, selected)
    
    def show_status(self, status):
        self.progress.setValue(status)

    def get_preview(self):
        url = str(self.url.text())
        self.pasted.emit(url)
    
    def show_preview(self, video_data):
        self.progress.reset()
        self.lcd2.display(video_data["length"])
        self.text.setText("Title: " + video_data["title"] + "\n\n" + "Description: " + video_data["description"])
        self.lable.setText(video_data["status"])
        self.combo_box.clear()
        self.combo_box.addItems(video_data["items"])
