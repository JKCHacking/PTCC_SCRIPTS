from PyQt5 import QtWidgets, QtCore


class HulaController(QtCore.QObject):
    def __init__(self, view, model, login_controller):
        super().__init__()
        self.view = view
        self.model = model
        self.login_controller = login_controller

        self.connect_signals()

    def connect_signals(self):
        self.view.start_sb.valueChanged.connect(self.__create_ticks)
        self.view.stop_sb.valueChanged.connect(self.__create_ticks)
        self.view.generate_btn.clicked.connect(self.__generate)
        self.view.bot_launcher_btn.clicked.connect(self.launch_bot)

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
