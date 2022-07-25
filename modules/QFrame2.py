from PyQt5 import QtCore, QtGui, QtWidgets
import modules.vlc_mod as vlc_mod


class QFrame2(QtWidgets.QFrame):

    def __init__(self, parent=None):
        super(QFrame2, self).__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            vlc_mediaplayer = vlc_mod.get_vlc_mediaplayer()
            if(vlc_mediaplayer.is_playing()):
                vlc_mediaplayer.set_pause(1)
            else:
                vlc_mediaplayer.set_pause(0)
