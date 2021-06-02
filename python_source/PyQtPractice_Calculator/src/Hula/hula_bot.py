import re
import fbchat  # type: ignore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton


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
        session_cookies = {
          "c_user": "",
          "xs": ""
        }
        try:
            self.client = Bot(email, password, session_cookies=session_cookies)
        except fbchat.FBchatException as fb_err:
            print(str(fb_err))

    def get_client(self):
        return self.client


class BotCtrl:
    def __init__(self, view, model):
        self.view = view
        self.model = model

    def listen(self):
        pass

    def send(self):
        pass

    def init_UI(self):
        print("Initializing UI")

    def logout(self):
        pass


class BotUI(QMainWindow):
    def __init__(self):
        self.chat_id_label = QLabel()
        self.chat_id_text = QLineEdit()
        self.verify_button = QPushButton()

        self.listen_label = QLabel()
        super().__init__()
        self.setWindowTitle("Login")
        self.general_layout = QVBoxLayout()
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.general_layout)

    def create_main_window(self):
        pass