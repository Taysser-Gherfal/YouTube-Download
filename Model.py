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
    items = []

    def preview(self, e):
        self.items.clear()
        try:
            youtube = YouTube(str(e))
            stream = youtube.streams[0]
            for i in youtube.streams.filter(progressive=True).all():
                self.items.append("Type: Video & Audio" + " - " + "Size: " + str(round(int(i.filesize) / 1000000, 2)) + "MB")

            for i in youtube.streams.filter(adaptive=True).all():
                self.items.append("Type: " + str(i.type) + " only" + " - " + "Size: " + str(round(int(i.filesize) / 1000000, 2)) + "MB")

            video_data = {
                "title": stream.title,
                "length": round(int(youtube.length) /60, 2),
                "description": youtube.description,
                "items": self.items,
                "status": "pytube"
            }

        except:
            try:
                ydl_opts = {}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    meta = ydl.extract_info(str(e), download=False)
                    
                    for i in meta['formats']:
                        self.items.append("Type: " + i['acodec'] + " - " + i['format'] + " - " + i['ext'] + " - " + "Size: " + str(round(int(i['filesize']) / 1000000, 2)) + "MB" + " / " + i['format_id'])

                    video_data = {
                        "title": meta['title'],
                        "length": round(int(meta['duration'])/60, 2),
                        "description": meta['description'],
                        "items": self.items,
                        "status": "youtube_dl"
                    }

            except:
                video_data = {
                "title" : "Error!",
                "length" : 0,
                "description" : "Wasn't able to preview data from this URL.",
                "items": ["Not supported for this video!"],
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

    def download(self, url, folder, library, selected=0):
        # removing attached list if found
        result = url.find("&list=")
        if result != -1:
            url = url[:result]

        if library == "pytube":
            self.size = YouTube(url).streams[selected].filesize
            YouTube(url, on_progress_callback=self.setProgressVal).streams[selected].download(folder)
            
        elif library == "youtube_dl":
            select = self.items[selected]
            left, right = select.split('/')
            
            ydl_opts = {'progress_hooks': [self.my_hook], 'outtmpl': folder + '/' + '%(title)s', 'format': right.lstrip(),}
            #ydl_opts = {'progress_hooks': [self.my_hook], 'outtmpl': folder + '/' + '%(title)s', 'format': 'worst',}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            