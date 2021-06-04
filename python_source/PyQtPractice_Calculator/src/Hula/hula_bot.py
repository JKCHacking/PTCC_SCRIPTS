import fbchat
import json
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QRect


class BotModel:
    def __init__(self):
        self.session = None

    def create_session(self, email, password):
        session_cookies = self.__get_cookies()
        try:
            self.session = fbchat.Session.from_cookies(session_cookies)
        except fbchat.FacebookError as fb_err:
            print(str(fb_err))

    def get_session(self):
        return self.session

    def __get_cookies(self):
        cookie_path = "H:\\Desktop\\My Documents\\HulaAutomation\\session.json"
        with open(cookie_path) as f:
            data = json.load(f)
        return data


class ListenWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    def __init__(self, view, listener, parent=None):
        super().__init__(parent)
        self.view = view
        self.listener = listener

    @QtCore.pyqtSlot()
    def run(self):
        # start listening
        for event in self.listener.listen():
            if isinstance(event, fbchat.MessageEvent):
                self.view.listen_result_text.insertPlainText(event.message.text)


class BotCtrl:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.conversation = None
        self.session = None
        self.listener = None
        self.listener_worker = None
        self.listener_thread = None

        self.connect_signals()

    def connect_signals(self):
        self.view.listen_switch.clicked.connect(self.listen)
        self.view.verify_button.clicked.connect(self.verify)
        self.view.send_button.clicked.connect(self.send)

    def listen(self):
        if self.view.listen_switch.isChecked():
            # start listening
            self.listener_thread = QtCore.QThread()
            self.listener_worker = ListenWorker(self.view, self.listener)
            self.listener_worker.moveToThread(self.listener_thread)
            self.listener_worker.finished.connect(self.listener_thread.quit)
            self.listener_worker.finished.connect(self.listener_worker.deleteLater)
            self.listener_thread.started.connect(self.listener_worker.run)
            self.listener_thread.finished.connect(self.listener_thread.deleteLater)
            self.listener_thread.start()
        else:
            # stop listening
            self.listener.disconnect()
            self.listener_thread.quit()
            self.listener_thread.wait()
            self.listener = fbchat.Listener(session=self.session, chat_on=True, foreground=True)

    def send(self):
        message = self.view.message_text.toPlainText()
        if message:
            try:
                self.conversation.send_text(message)
                self.view.message_text.clear()
                self.view.display_message_box("Message sent", "info")
            except fbchat.FacebookError as fb_err:
                self.view.display_message_box(str(fb_err), "error")
        else:
            self.view.display_message_box("Please enter a message", "warning")

    def init_UI(self):
        self.view.create_main_window()
        self.view.show()
        self.disable_controls()

    def logout(self):
        pass

    def verify(self):
        # initialize the session and listener
        self.session = self.model.get_session()
        self.listener = fbchat.Listener(session=self.session, chat_on=True, foreground=True)
        # get the chat id from the view
        chat_id = self.view.chat_id_text.text()
        thread_type = None
        # get the thread type of the conversation
        for button in self.view.chat_type_rb_group.buttons():
            if button.isChecked():
                thread_type = button.text()

        # creates a User object if the selected is USER and Group object if GROUP
        try:
            if thread_type == "USER":
                self.conversation = fbchat.User(session=self.session, id=chat_id)
                print("USER")
            elif thread_type == "GROUP":
                self.conversation = fbchat.Group(session=self.session, id=chat_id)
                print("GROUP")
            else:
                print("Unable to process")
        except fbchat.FacebookError as fb_err:
            print(str(fb_err))

        # enables all the controls if everything is OK.
        if self.conversation is not None:
            self.view.display_message_box("Verified.", "info")
            self.enable_controls()
        else:
            self.view.display_message_box("Not Verified.", "warning")

    def enable_controls(self):
        self.view.listen_switch.setDisabled(False)
        self.view.message_text.setDisabled(False)
        self.view.send_button.setDisabled(False)
        self.view.schedule_switch.setDisabled(False)
        self.view.time_picker.setDisabled(False)
        self.view.date_picker.setDisabled(False)
        self.view.schedule_message_text.setDisabled(False)

    def disable_controls(self):
        self.view.listen_switch.setDisabled(True)
        self.view.message_text.setDisabled(True)
        self.view.send_button.setDisabled(True)
        self.view.schedule_switch.setDisabled(True)
        self.view.time_picker.setDisabled(True)
        self.view.date_picker.setDisabled(True)
        self.view.schedule_message_text.setDisabled(True)


class BotUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(250, 400)
        # self.setStyleSheet("background-color: #000000")
        # Widgets
        self.chat_id_label = QtWidgets.QLabel("CHAT ID")
        self.chat_id_text = QtWidgets.QLineEdit()
        self.verify_button = QtWidgets.QPushButton("VERIFY")
        self.user_rbutton = QtWidgets.QRadioButton("USER")
        self.group_rbutton = QtWidgets.QRadioButton("GROUP")
        self.chat_type_rb_group = QtWidgets.QButtonGroup()
        self.chat_type_rb_group.addButton(self.user_rbutton)
        self.chat_type_rb_group.addButton(self.group_rbutton)
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
        self.signout_button = QtWidgets.QPushButton("SIGNOUT")
        self.general_layout = QtWidgets.QVBoxLayout()
        self.central_widget = QtWidgets.QWidget(self)

    def create_main_window(self):
        self.setWindowTitle("Messenger Bot")
        # layouts
        chat_id_layout = QtWidgets.QHBoxLayout()
        chat_type_rbutton_layout = QtWidgets.QHBoxLayout()
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
        self.general_layout.addLayout(chat_id_layout)
        self.general_layout.addLayout(chat_type_rbutton_layout)
        self.general_layout.addLayout(listen_layout)
        self.general_layout.addLayout(message_layout)
        self.general_layout.addLayout(schedule_layout)
        self.general_layout.addWidget(self.signout_button)

        # adding widgets in respective layouts
        chat_id_layout.addWidget(self.chat_id_label)
        chat_id_layout.addWidget(self.chat_id_text)
        chat_id_layout.addWidget(self.verify_button)
        chat_type_rbutton_layout.addWidget(self.user_rbutton)
        chat_type_rbutton_layout.addWidget(self.group_rbutton)
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

    def display_message_box(self, message, level):
        msg = QtWidgets.QMessageBox()
        if level == "info":
            msg.setIcon(QtWidgets.QMessageBox.Information)
        elif level == "warning":
            msg.setIcon(QtWidgets.QMessageBox.Warning)
        elif level == "error":
            msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Message")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()


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
        pen.setWidth(1)
        painter.setPen(pen)

        painter.drawRoundedRect(QRect(-width, -radius, 2 * width, 2 * radius), radius, radius)
        painter.setBrush(QtGui.QBrush(bg_color))
        sw_rect = QRect(-radius, -radius, width + radius, 2 * radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, Qt.AlignCenter, label)
