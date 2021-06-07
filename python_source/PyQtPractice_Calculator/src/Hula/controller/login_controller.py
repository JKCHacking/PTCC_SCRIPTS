from PyQt5 import QtCore


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