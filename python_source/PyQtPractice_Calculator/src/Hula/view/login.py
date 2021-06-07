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
