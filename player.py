import glob
import os
import sys
from time import sleep
from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QMainWindow, QStyle, QFileDialog
from PyQt5.QtCore import QTime
import vlc
from ui.main import Ui_MainWindow
import modules.vlc_mod as vlc_mod
from natsort import os_sorted


class myMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(myMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("Media Player")

        self.playButton.setText('')
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.setEnabled(False)

        self.rn = self.playlistTableWidget.rowCount()

        self.vlc_instance = vlc_mod.get_vlc_instance()
        self.vlc_mediaplayer = vlc_mod.get_vlc_mediaplayer()

        if sys.platform.startswith("linux"):
            self.vlc_mediaplayer.set_xwindow(self.videoFrame.winId())
        elif sys.platform == "win32":
            self.vlc_mediaplayer.set_hwnd(self.videoFrame.winId())
        elif sys.platform == "darwin":
            self.vlc_mediaplayer.set_nsobject(self.videoFrame.winId())

        events = self.vlc_mediaplayer.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerPaused, self.mediaPlayerPaused)
        events.event_attach(vlc.EventType.MediaPlayerPlaying, self.mediaPlayerPlaying)
        events.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.mediaPlayerPositionChanged)
        events.event_attach(vlc.EventType.MediaDurationChanged, self.mediaDurationChanged)

        # filename = "001.mp4"
        # media = self.vlc_instance.media_new(filename)
        # media.parse()
        # self.vlc_mediaplayer.set_media(media)
        # self.vlc_mediaplayer.play()
        # mtime = QTime(0, 0, 0, 0)
        # mtime = mtime.addMSecs(media.get_duration())
        # self.endDurationLabel.setText(mtime.toString())

        self.positionSlider.setRange(0, 1000)

        self.playButton.clicked.connect(self.playButtonClicked)

        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(self.vlc_mediaplayer.audio_get_volume())
        self.volumeSlider.valueChanged.connect(self.volumeSliderValueChanged)

        self.rateSliderValues = {1: 0.5, 2: 0.75, 3: 1.0, 4: 1.25, 5: 1.5, 6: 1.75, 7: 2.0,
                                 8: 2.25, 9: 2.5, 10: 2.75, 11: 3.0, 12: 3.25, 13: 3.5, 14: 3.75, 15: 4.0}

        self.rateSlider.setRange(1, 15)
        self.rateSlider.setTickInterval(1)
        self.rateSlider.setValue(3)
        self.rateSlider.valueChanged.connect(self.rateSliderValueChanged)

        self.openButton.clicked.connect(self.open_file)

        self.positionSlider.sliderMoved.connect(self.positionSliderSliderMoved)

        self.playlistTableWidget.itemDoubleClicked.connect(self.itemDoubleClicked)

        self.playlist = []

    def itemDoubleClicked(self, event):
        media = self.vlc_instance.media_new(self.playlist[event.row()])
        media.parse()
        self.vlc_mediaplayer.set_media(media)
        self.startDurationLabel.setText('00:00:00')
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(media.get_duration())
        self.endDurationLabel.setText(mtime.toString())
        self.vlc_mediaplayer.play()

    def positionSliderSliderMoved(self):
        pos = self.positionSlider.value()
        self.vlc_mediaplayer.set_position(pos / 1000.0)

    def open_file(self):
        directory = QFileDialog.getExistingDirectory(self, 'Open Video')
        if directory != '':
            print(directory)

            self.playlist = os_sorted(glob.glob(directory + '/**/*.mp4', recursive=True))

            print(self.playlist)

            for item in self.playlist:
                self.playlistTableWidget.insertRow(self.rn)
                self.playlistTableWidget.setItem(self.rn, 0, QTableWidgetItem(os.path.basename(item)))
                self.playlistTableWidget.setItem(self.rn, 1, QTableWidgetItem("Visto"))
                self.playlistTableWidget.setItem(self.rn, 2, QTableWidgetItem("3:45"))
                self.rn += 1

    def rateSliderValueChanged(self, value):
        self.vlc_mediaplayer.set_rate(self.rateSliderValues[value])
        self.rateLabel.setText(str(self.rateSliderValues[value]))

    def playButtonClicked(self):
        if(self.vlc_mediaplayer.is_playing()):
            self.vlc_mediaplayer.set_pause(1)
        else:
            self.vlc_mediaplayer.set_pause(0)

    def volumeSliderValueChanged(self, value):
        self.vlc_mediaplayer.audio_set_volume(value)
        self.volumeLabel.setText(str(value))

    def mediaDurationChanged(self, event):
        print(int(self.vlc_mediaplayer.get_length() / 1000))
        print('mediaDurationChanged')

    def mediaPlayerPaused(self, event):
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def mediaPlayerPlaying(self, event):
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.playButton.setEnabled(True)

    def mediaPlayerPositionChanged(self, event):
        self.positionSlider.setValue(int(self.vlc_mediaplayer.get_position() * 1000))
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(self.vlc_mediaplayer.get_time())
        self.startDurationLabel.setText(mtime.toString())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    vlc_mod.initialize()
    MainWindow = myMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
