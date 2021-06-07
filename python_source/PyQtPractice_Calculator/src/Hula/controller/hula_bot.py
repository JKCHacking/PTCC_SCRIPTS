import fbchat
from PyQt5 import QtCore


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
                if event.author.id == self.view.chat_id_text.text():
                    message = "{}\n".format(event.message.text)
                    self.view.listen_result_text.setText(message)


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

    def alarm(self):
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