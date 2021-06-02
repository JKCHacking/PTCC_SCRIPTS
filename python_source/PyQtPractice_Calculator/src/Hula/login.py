import csv
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QSize


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

        self.setWindowTitle("Login")
        self.general_layout = QVBoxLayout()
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.general_layout)

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


class LoginCtrl:
    def __init__(self, view, model, bot_ctrl):
        self.view = view
        self.model = model
        self.bot_ctrl = bot_ctrl

        self.connect_signals()

    def connect_signals(self):
        self.view.login_button.clicked.connect(self.login)

    def launch_bot(self):
        self.view.close()
        self.bot_ctrl.init_UI()

    def login(self):
        self.start_loading_anim()
        email = self.view.email_text.text()
        password = self.view.password_text.text()
        self.model.create_client(email, password)
        client = self.model.get_client()
        if client.isLoggedIn():
            self.stop_loading_anim()
            self.launch_bot()

    def init_UI(self):
        self.view.create_login_window()
        self.view.show()

    def start_loading_anim(self):
        self.view.movie.start()

    def stop_loading_anim(self):
        self.view.movie.stop()
