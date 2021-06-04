# DEBUGGING PURPOSES
# import sys
# def trap_exc_during_debug(*args):
#     print(args)
#
# sys.excepthook = trap_exc_during_debug

from PyQt5 import QtWidgets, QtCore, QtGui


class LoginUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(250, 150)
        self.email_label = QtWidgets.QLabel("EMAIL")
        self.password_label = QtWidgets.QLabel("PASSWORD")
        self.email_text = QtWidgets.QLineEdit()
        self.password_text = QtWidgets.QLineEdit()
        self.password_text.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_button = QtWidgets.QPushButton("SIGN IN")
        self.loading_anim = QtWidgets.QLabel()
        self.movie = QtGui.QMovie("drawable/spinner.gif")
        self.movie.setScaledSize(QtCore.QSize(30, 30))
        self.loading_anim.setMovie(self.movie)
        self.general_layout = QtWidgets.QVBoxLayout()
        self.central_widget = QtWidgets.QWidget(self)

    def create_login_window(self):
        email_layout = QtWidgets.QVBoxLayout()
        password_layout = QtWidgets.QVBoxLayout()
        lower_layout = QtWidgets.QHBoxLayout()

        email_layout.addWidget(self.email_label)
        email_layout.addWidget(self.email_text)
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_text)
        lower_layout.addWidget(self.login_button)
        lower_layout.addWidget(self.loading_anim)

        self.general_layout.addLayout(email_layout)
        self.general_layout.addLayout(password_layout)
        self.general_layout.addLayout(lower_layout)
        self.setWindowTitle("Login")
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.general_layout)

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


class LoginWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    def __init__(self, model, view, parent=None):
        super().__init__(parent)
        self.model = model
        self.view = view

    @QtCore.pyqtSlot()
    def run(self):
        email = self.view.email_text.text()
        password = self.view.password_text.text()
        self.model.create_session(email, password)
        self.finished.emit()


class LoginCtrl(QtCore.QObject):
    def __init__(self, view, model, bot_ctrl):
        super().__init__()
        self.login_worker = None
        self.login_thread = None
        self.view = view
        self.model = model
        self.bot_ctrl = bot_ctrl

        self.connect_signals()

    def connect_signals(self):
        self.view.login_button.clicked.connect(self.login)

    def launch_bot(self):
        self.view.close()
        self.bot_ctrl.init_UI()

    @QtCore.pyqtSlot()
    def __login_finished(self):
        session = self.model.get_session()
        # if login failed it will return None
        if session is not None:
            if session.is_logged_in():
                self.stop_loading_anim()
                self.launch_bot()
        else:
            self.view.display_message_box("Login Failed.", "warning")
            self.view.login_button.setDisabled(False)

    def login(self):
        self.start_loading_anim()
        self.view.login_button.setDisabled(True)
        self.login_thread = QtCore.QThread()
        self.login_worker = LoginWorker(self.model, self.view)
        self.login_worker.moveToThread(self.login_thread)
        self.login_worker.finished.connect(self.__login_finished)
        self.login_worker.finished.connect(self.login_thread.quit)
        self.login_worker.finished.connect(self.login_worker.deleteLater)
        self.login_thread.started.connect(self.login_worker.run)
        self.login_thread.finished.connect(self.login_thread.deleteLater)
        self.login_thread.start()

    def init_UI(self):
        self.view.create_login_window()
        self.view.show()

    def start_loading_anim(self):
        self.view.movie.start()

    def stop_loading_anim(self):
        self.view.movie.stop()
