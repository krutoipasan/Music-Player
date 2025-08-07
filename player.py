import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QMainWindow
import os
from pygame import mixer
from PIL import Image, ImageFilter
from musicplayer import *

mixer.init()

class Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.current_song = None
        self.current_filedir = None

    def choosefiledir(self):
        filedir = QFileDialog.getExistingDirectory()
        return filedir
    
    def showfilenameslist(self):
        global songs
        extensions = [".mp3", ".wav", ".ogg"]
        self.current_filedir = self.choosefiledir()
        if not self.current_filedir:
            return  
        try:
            files = os.listdir(self.current_filedir)
            songs = [file for file in files if any(file.lower().endswith(ext) for ext in extensions)]
            self.ui.songlist.clear()
            for song in songs:
                self.ui.songlist.addItem(song)
                
        except Exception as e:
            self.show_error(str(e))
    
    def play_song(self):
        if not self.current_filedir:
            self.show_error("Виберіть папку з піснями!")
            return
        current_item = self.ui.songlist.currentItem()
        if not current_item:
            self.show_error("Виберіть пісню!")
            return
            
        song_path = os.path.join(self.current_filedir, current_item.text())
        
        try:
            mixer.music.load(song_path)
            mixer.music.play()
            self.ui.songnamelabel.setText(current_item.text())
        except Exception as e:
            self.show_error(f"Ошибка! Вже грає пісня/музика: {str(e)}")
    
    def pause_song(self):
        if mixer.music.get_busy():
            mixer.music.pause()
            self.ui.pauseButton.setText("Unpause")
        else:
            mixer.music.unpause()
            self.ui.pauseButton.setText("Pause")
    
    def stop_song(self):
        mixer.music.stop()
    
    def set_volume(self, value):
        volume = value / 100.0
        mixer.music.set_volume(volume)
    
    def search(self):
        searchtext = self.ui.searchbar.text().lower()
        try:
            if self.ui.searchbutton.text() == "Шукати":
                songs_filtered = [song for song in songs if searchtext in song.lower()]
                self.ui.searchbutton.setText("Скинути пошук")
                self.ui.songlist.clear()
                self.ui.songlist.addItems(songs_filtered)
            elif self.ui.searchbutton.text() == "Скинути пошук":
                self.ui.songlist.clear()
                self.ui.songlist.addItems(songs)
                self.ui.searchbutton.setText("Шукати")
        except Exception as e:
            self.show_error(f"{str(e)}")

    def configure(self):
        self.ui.folderbutton.clicked.connect(self.showfilenameslist)
        self.ui.startbutton.clicked.connect(self.play_song)
        self.ui.pauseButton.clicked.connect(self.pause_song)
        self.ui.stopbutton.clicked.connect(self.stop_song)
        self.ui.searchbutton.clicked.connect(self.search)
        self.ui.volumeslider.valueChanged.connect(self.set_volume)
        self.ui.songlist.itemDoubleClicked.connect(self.play_song)
    
    def show_error(self, message):
        error_message = QMessageBox()
        error_message.setIcon(QMessageBox.Warning)
        error_message.setWindowTitle("Обережно!")
        error_message.setText(message)
        error_message.setStandardButtons(QMessageBox.Ok)
        error_message.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget()
    ex.configure()
    ex.show()
    sys.exit(app.exec_())
