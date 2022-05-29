from PyQt5 import QtWidgets, QtCore


class InputWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    message_receive_sig = QtCore.pyqtSignal(str)
    generate_sig = QtCore.pyqtSignal()
    reset_sig = QtCore.pyqtSignal()
    range_sig = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            user_input = input("Hula> ")
            if user_input == "generate":
                self.generate_sig.emit()
            elif user_input == "reset":
                self.reset_sig.emit()
            elif "-" in user_input:
                self.range_sig.emit(user_input)
            elif user_input == "exit":
                break
            else:
                try:
                    guess_num = int(user_input)
                except ValueError:
                    continue
                self.message_receive_sig.emit(str(guess_num))
        self.finished.emit()


class HulaController(QtCore.QObject):
    def __init__(self, view, model, login_controller):
        super().__init__()
        self.view = view
        self.model = model
        self.login_controller = login_controller
        self.input_worker = None
        self.input_thread = None

        self.connect_signals()
        self.listen_input()

    def connect_signals(self):
        self.view.start_sb.valueChanged.connect(self.__create_ticks)
        self.view.stop_sb.valueChanged.connect(self.__create_ticks)
        self.view.generate_btn.clicked.connect(self.__generate)
        self.view.bot_launcher_btn.clicked.connect(self.launch_bot)

    def listen_input(self):
        self.input_thread = QtCore.QThread()
        self.input_worker = InputWorker()
        self.input_worker.moveToThread(self.input_thread)
        self.input_worker.message_receive_sig.connect(self.listen)
        self.input_worker.generate_sig.connect(self.__generate)
        self.input_worker.reset_sig.connect(self.__create_ticks)
        self.input_worker.range_sig.connect(self.create_ticks_from_range)
        self.input_worker.finished.connect(self.input_thread.quit)
        self.input_worker.finished.connect(self.input_worker.deleteLater)
        self.input_thread.started.connect(self.input_worker.run)
        self.input_thread.finished.connect(self.input_thread.deleteLater)
        self.input_thread.start()

    def __create_ticks(self):
        start = self.view.start_sb.value()
        stop = self.view.stop_sb.value()
        num_ticks = list(range(start, stop + 1))

        self.__clear_layout(self.view.tickbox_layout)
        row = 0
        col = 0
        for i, num_tick in enumerate(num_ticks):
            if i % 10 == 0:
                row += 1
                col = 0
            cb = QtWidgets.QCheckBox(str(num_tick))
            cb.setObjectName("checkbox_{}".format(num_tick))
            cb.stateChanged.connect(self.__add_remove_taken)
            self.view.tickbox_layout.addWidget(cb, col, row)
            col += 1
        self.__clear_taken()

    def create_ticks_from_range(self, range_str):
        range_str = range_str.split("-")
        start = int(range_str[0])
        stop = int(range_str[1])
        self.view.start_sb.setValue(start)
        self.view.stop_sb.setValue(stop)
        self.__create_ticks()

    def __clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def __clear_taken(self):
        self.model.clear_taken()

    def __generate(self):
        start = self.view.start_sb.value()
        stop = self.view.stop_sb.value()
        result_guessed = self.model.generate(start, stop)
        self.view.guessed_result_label.setText(str(result_guessed))

    def __add_remove_taken(self):
        cb = self.view.sender()
        if cb.isChecked():
            self.model.add_taken(int(cb.text()))
        else:
            self.model.remove_taken(int(cb.text()))

    @QtCore.pyqtSlot(str)
    def listen(self, message):
        if message.isnumeric():
            cb = self.view.findChild(QtWidgets.QCheckBox, "checkbox_{}".format(message))
            if cb is not None:
                self.model.add_taken(message)
                cb.setChecked(True)

    def connect_bot_signal(self, bot_signal):
        bot_signal.connect(self.listen)

    def init_UI(self):
        self.view.create_main_window()
        self.view.show()

    def launch_bot(self):
        self.login_controller.init_UI()
