import fbchat
from PyQt5 import QtCore


class QtInterface(QtCore.QObject):
    message_receive_sig = QtCore.pyqtSignal(str)


qt_interface = QtInterface()


class HulaClient(fbchat.Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        message = message_object.text
        qt_interface.message_receive_sig.emit(message)

    def connect_signal(self, func):
        qt_interface.message_receive_sig.connect(func)




