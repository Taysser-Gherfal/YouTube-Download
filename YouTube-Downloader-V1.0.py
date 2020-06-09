import sys
import os
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from pytube import YouTube
import youtube_dl

class MainWindow(qtw.QWidget):
    status = qtc.pyqtSignal(int)

    def __init__(self):

        super().__init__()
        # Main UI code
        self.setWindowTitle("YouTube Downloader - By Taysser")
        self.resize(1000,350)

        self.url = qtw.QLineEdit()
        download_button = qtw.QPushButton("Download", self)
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
        layout.addLayout(right_layout, 1, 1)
        
        # Adding widgets to the main UI
        layout.addWidget(self.url, 0, 0)
        layout.addWidget(download_button, 0, 1)
        layout.addWidget(self.text, 1, 0)
        layout.addWidget(self.lable, 2, 1)
        layout.addWidget(self.progress, 2, 0)

        # Adding widgets to the right col
        right_layout.addWidget(self.size_lable)
        right_layout.addWidget(self.lcd1)
        right_layout.addWidget(self.time_lable)
        right_layout.addWidget(self.lcd2)

        # Connecting the download button and the URL change
        download_button.clicked.connect(self.youtube)
        self.url.textChanged.connect(self.preview)

        # Setting lable text
        self.lable.setText("Status...")
        self.size_lable.setText("Size (MB):")
        self.time_lable.setText("Time (Mins):")

        # End main UI code
        self.show()
    
    def preview(self, e):
        try:
            youtube = YouTube(str(self.url.text()))
            stream = youtube.streams[0]
            size = round(int(stream.filesize) / 1000000, 2)
            title = stream.title
            length = round(int(youtube.length) /60, 2)
            description = youtube.description

            self.lcd1.display(size)
            self.lcd2.display(length)
            self.text.setText("Title: " + title + "\n\n" + "Description: " + description)
            self.lable.setText("pytube")
        except:
            try:
                ydl_opts = {}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    meta = ydl.extract_info(str(self.url.text()), download=False)
                self.lcd2.display(round(int(meta['duration'])/60, 2))
                self.text.setText("Title:" + meta['title'] + "\n\n" + "Description: " + meta['description'])
                self.lable.setText("youtube_dl")

            except:
                self.lable.setText("Error!")
                self.lcd1.display(0)
                self.lcd2.display(0)
                self.text.setText("Wasn't able to preview data from this URL. You should still be able to download your video(s)")

    def setProgress(self, val):
        self.progress.setValue(val)

    def setProgressVal(self, chunk, file_handle, bytes_remaining):
        percentage = 1 - bytes_remaining / self.size
        self.status.emit(percentage*100)
    
    def openFolder(self):
        self.file = str(qtw.QFileDialog.getExistingDirectory(self, "Select Directory"))

    def youtube(self, e):
        self.openFolder()
        try:
            self.status.connect(self.setProgress)
            self.size = YouTube(str(self.url.text())).streams[0].filesize
            YouTube(str(self.url.text()), on_progress_callback=self.setProgressVal).streams[0].download(self.file)
            self.lable.setText("Done!")
        except:
            self.lable.setText("youtube_dl")
            try:
                self.youtube2(self.file)
            except:
                self.lable.setText("Error!")
                self.text.setText("Sorry, not able to download your video!")
    
    def my_hook(self, d):
        if d['status'] == 'finished':
            file_tuple = os.path.split(os.path.abspath(d['filename']))
            print("Done downloading {}".format(file_tuple[1]))
        if d['status'] == 'downloading':
            p = d['_percent_str']
            p = p.replace('%','')

            size = round(int(d['total_bytes']) / 1000000, 2)
            self.lcd1.display(size)
            self.text.setText(d['filename'])
            self.status.emit(float(p))

    def youtube2(self, file):
        ydl_opts = {'progress_hooks': [self.my_hook], 'outtmpl': file + '/' + '%(title)s', 'format': 'best',}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([str(self.url.text())])
        #'format': 'bestaudio/best',
        #'noplaylist' : True,
        


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())