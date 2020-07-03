import sys
import os
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from pytube import YouTube
import youtube_dl

class Model(qtc.QObject):

    previewing = qtc.pyqtSignal(dict)
    status = qtc.pyqtSignal(float)

    def preview(self, e):

        try:
            youtube = YouTube(str(e))
            stream = youtube.streams[0]
            video_data = {
                "size" : round(int(stream.filesize) / 1000000, 2),
                "title" : stream.title,
                "length" : round(int(youtube.length) /60, 2),
                "description" : youtube.description,
                "status" : "pytube"
            }

        except:
            try:
                ydl_opts = {}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    meta = ydl.extract_info(str(e), download=False)
                    video_data = {
                    "size" : 0,
                    "title" : meta['title'],
                    "length" : round(int(meta['duration'])/60, 2),
                    "description" : meta['description'],
                    "status" : "youtube_dl"
                    }

            except:
                video_data = {
                "size" : 0,
                "title" : "Error!",
                "length" : 0,
                "description" : "Wasn't able to preview data from this URL.",
                "status" : "Error!"
                }
        
        self.previewing.emit(video_data)
    
    def setProgressVal(self, chunk, file_handle, bytes_remaining):
        percentage = 1 - bytes_remaining / self.size
        self.status.emit(percentage*100)

    def my_hook(self, d):
        if d['status'] == 'finished':
            file_tuple = os.path.split(os.path.abspath(d['filename']))
        if d['status'] == 'downloading':
            p = d['_percent_str']
            p = p.replace('%','')

            size = round(int(d['total_bytes']) / 1000000, 2)
            self.status.emit(float(p))

    def download(self, url, folder, library):
        if library == "pytube":
            self.size = YouTube(url).streams[0].filesize
            YouTube(url, on_progress_callback=self.setProgressVal).streams[0].download(folder)
            
        elif library == "youtube_dl":
            ydl_opts = {'progress_hooks': [self.my_hook], 'outtmpl': folder + '/' + '%(title)s', 'format': 'best',}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])


class View(qtw.QWidget):

    pasted = qtc.pyqtSignal(str)
    submitted = qtc.pyqtSignal(str, str, str)

    def __init__(self):

        super().__init__()
        # Main UI code
        self.url = qtw.QLineEdit()
        self.folder = qtw.QLineEdit()
        download_button = qtw.QPushButton("Download", self)
        folder_button = qtw.QPushButton("Folder", self)
        self.lable = qtw.QLabel()
        self.size_lable = qtw.QLabel()
        self.time_lable = qtw.QLabel()
        self.progress = qtw.QProgressBar()
        self.lcd1 = qtw.QLCDNumber()
        self.lcd2 = qtw.QLCDNumber()
        self.text = qtw.QTextBrowser()

        # Main UI layout
        layout = qtw.QGridLayout()
        self.setLayout(layout)

        # Right col layout
        right_layout = qtw.QVBoxLayout()
        layout.addLayout(right_layout, 3, 1)
        
        # Adding widgets to the main UI
        layout.addWidget(self.url, 0, 0)
        layout.addWidget(download_button, 0, 1)
        layout.addWidget(self.folder, 1, 0)
        layout.addWidget(folder_button, 1, 1)
        layout.addWidget(self.text, 3, 0)
        layout.addWidget(self.lable, 4, 1)
        layout.addWidget(self.progress, 4, 0)

        # Adding widgets to the right col
        right_layout.addWidget(self.size_lable)
        right_layout.addWidget(self.lcd1)
        right_layout.addWidget(self.time_lable)
        right_layout.addWidget(self.lcd2)

        # Setting lable text
        self.lable.setText("Status...")
        self.size_lable.setText("Size (MB):")
        self.time_lable.setText("Time (Mins):")

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
        self.submitted.emit(url, folder, library)
    
    def show_status(self, status):
        self.progress.setValue(status)

    def get_preview(self):
        url = str(self.url.text())
        self.pasted.emit(url)
    
    def show_preview(self, video_data):
        self.progress.reset()
        self.lcd1.display(video_data["size"])
        self.lcd2.display(video_data["length"])
        self.text.setText("Title: " + video_data["title"] + "\n\n" + "Description: " + video_data["description"])
        self.lable.setText(video_data["status"])


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