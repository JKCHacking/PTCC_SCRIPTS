import time
import sys
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class LoginUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(250, 150)
        self.email_label = QLabel("EMAIL")
        self.password_label = QLabel("PASSWORD")
        self.email_text = QLineEdit()
        self.password_text = QLineEdit()
        self.password_text.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("SIGN IN")
        self.loading_anim = QLabel()
        self.movie = QMovie("drawable/spinner.gif")
        self.movie.setScaledSize(QSize(30, 30))
        self.loading_anim.setMovie(self.movie)
        self.error_label = QLabel()
        self.general_layout = QVBoxLayout()
        self.central_widget = QWidget(self)

    def create_login_window(self):
        email_layout = QVBoxLayout()
        password_layout = QVBoxLayout()
        lower_layout = QHBoxLayout()

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


def trap_exc_during_debug(*args):
    print(args)


sys.excepthook = trap_exc_during_debug


class LoginWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model

    @pyqtSlot()
    def run(self):
        # email = self.view.email_text.text()
        # password = self.view.password_text.text()
        # self.model.create_client(email, password)
        # print("Worker running...")
        time.sleep(10)
        self.finished.emit()


class LoginCtrl(QObject):
    def __init__(self, view, model, bot_ctrl):
        super().__init__()
        self.login_worker = None
        self.login_thread = QThread()
        self.view = view
        self.model = model
        self.bot_ctrl = bot_ctrl

        self.connect_signals()

    def connect_signals(self):
        self.view.login_button.clicked.connect(self.login)

    def launch_bot(self):
        self.view.close()
        self.bot_ctrl.init_UI()

    @pyqtSlot()
    def __login_finished(self):
        client = self.model.get_client()
        if client.isLoggedIn():
            self.stop_loading_anim()
            self.launch_bot()
        else:
            self.view.error_label.setText("Login Failed.")
            self.view.login_button.setDisabled(False)

    def login(self):
        self.start_loading_anim()
        self.view.login_button.setDisabled(True)
        self.login_worker = LoginWorker(self.model)
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
