import fbchat
import json
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QRect


class Bot(fbchat.Client):
    def onMessage(
        self,
        mid=None,
        author_id=None,
        message=None,
        message_object=None,
        thread_id=None,
        thread_type=fbchat.ThreadType.USER,
        ts=None,
        metadata=None,
        msg=None,
    ):
        pass


class BotModel:
    def __init__(self):
        self.client = None

    def create_client(self, email, password):
        session_cookies = self.__get_cookies()
        try:
            self.client = Bot(email, password, session_cookies=session_cookies)
        except fbchat.FBchatException as fb_err:
            print(str(fb_err))

    def get_client(self):
        return self.client

    def __get_cookies(self):
        cookie_path = "H:\\Desktop\\My Documents\\HulaAutomation\\session.json"
        with open(cookie_path) as f:
            data = json.load(f)
        return data


class BotCtrl:
    def __init__(self, view, model):
        self.view = view
        self.model = model

    def listen(self):
        pass

    def send(self):
        pass

    def init_UI(self):
        self.view.create_main_window()
        self.view.show()

    def logout(self):
        pass


class BotUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(250, 400)
        # self.setStyleSheet("background-color: #000000")
        # Widgets
        self.chat_id_label = QtWidgets.QLabel("CHAT ID")
        self.chat_id_text = QtWidgets.QLineEdit()
        self.verify_button = QtWidgets.QPushButton("VERIFY")
        self.listen_label = QtWidgets.QLabel("LISTEN")
        self.listen_switch = Switch()
        self.listen_result_text = QtWidgets.QPlainTextEdit()
        self.listen_result_text.setDisabled(True)
        self.message_label = QtWidgets.QLabel("MESSAGE")
        self.message_text = QtWidgets.QPlainTextEdit()
        self.send_button = QtWidgets.QPushButton("SEND")
        self.schedule_label = QtWidgets.QLabel("SCHEDULE")
        self.schedule_switch = Switch()
        self.time_label = QtWidgets.QLabel("TIME")
        self.time_picker = QtWidgets.QTimeEdit()
        self.time_picker.setTime(QtCore.QTime.currentTime())
        self.date_label = QtWidgets.QLabel("DATE")
        self.date_picker = QtWidgets.QDateEdit(calendarPopup=True)
        self.date_picker.setDate(QtCore.QDate.currentDate())
        self.schedule_message_label = QtWidgets.QLabel("MESSAGE")
        self.schedule_message_text = QtWidgets.QPlainTextEdit()
        self.t_remaining_label1 = QtWidgets.QLabel("TIME REMAINING")
        self.t_remaining_label2 = QtWidgets.QLabel()
        self.error_label = QtWidgets.QLabel()
        self.signout_button = QtWidgets.QPushButton("SIGNOUT")
        self.general_layout = QtWidgets.QVBoxLayout()
        self.central_widget = QtWidgets.QWidget(self)

    def create_main_window(self):
        self.setWindowTitle("Messenger Bot")
        # layouts
        chat_id_layout = QtWidgets.QHBoxLayout()
        listen_switch_layout = QtWidgets.QHBoxLayout()
        listen_layout = QtWidgets.QVBoxLayout()
        schedule_layout = QtWidgets.QVBoxLayout()
        schedule_switch_layout = QtWidgets.QHBoxLayout()
        time_layout = QtWidgets.QVBoxLayout()
        date_layout = QtWidgets.QVBoxLayout()
        date_time_layout = QtWidgets.QHBoxLayout()
        message_layout = QtWidgets.QVBoxLayout()
        time_remaining_layout = QtWidgets.QHBoxLayout()

        # nesting layouts and widgets
        self.general_layout.addWidget(self.error_label)
        self.general_layout.addLayout(chat_id_layout)
        self.general_layout.addLayout(listen_layout)
        self.general_layout.addLayout(message_layout)
        self.general_layout.addLayout(schedule_layout)
        self.general_layout.addWidget(self.signout_button)

        # adding widgets in respective layouts
        chat_id_layout.addWidget(self.chat_id_label)
        chat_id_layout.addWidget(self.chat_id_text)
        chat_id_layout.addWidget(self.verify_button)
        listen_switch_layout.addWidget(self.listen_label)
        listen_switch_layout.addWidget(self.listen_switch)
        listen_layout.addLayout(listen_switch_layout)
        listen_layout.addWidget(self.listen_result_text)
        message_layout.addWidget(self.message_label)
        message_layout.addWidget(self.message_text)
        message_layout.addWidget(self.send_button)
        schedule_switch_layout.addWidget(self.schedule_label)
        schedule_switch_layout.addWidget(self.schedule_switch)
        time_layout.addWidget(self.time_label)
        time_layout.addWidget(self.time_picker)
        date_layout.addWidget(self.date_label)
        date_layout.addWidget(self.date_picker)
        date_time_layout.addLayout(time_layout)
        date_time_layout.addLayout(date_layout)
        time_remaining_layout.addWidget(self.t_remaining_label1)
        time_remaining_layout.addWidget(self.t_remaining_label2)
        schedule_layout.addLayout(schedule_switch_layout)
        schedule_layout.addLayout(date_time_layout)
        schedule_layout.addWidget(self.schedule_message_label)
        schedule_layout.addWidget(self.schedule_message_text)
        schedule_layout.addLayout(time_remaining_layout)

        self.central_widget.setLayout(self.general_layout)
        self.setCentralWidget(self.central_widget)


class Switch(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setMinimumWidth(66)
        self.setMinimumHeight(22)

    def paintEvent(self, event):
        label = "ON" if self.isChecked() else "OFF"
        bg_color = Qt.blue if self.isChecked() else Qt.red

        radius = 10
        width = 32
        center = self.rect().center()

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QtGui.QColor(255, 255, 255))

        pen = QtGui.QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawRoundedRect(QRect(-width, -radius, 2 * width, 2 * radius), radius, radius)
        painter.setBrush(QtGui.QBrush(bg_color))
        sw_rect = QRect(-radius, -radius, width + radius, 2 * radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, Qt.AlignCenter, label)
