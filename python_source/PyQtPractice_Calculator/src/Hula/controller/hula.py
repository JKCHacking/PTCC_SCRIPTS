from PyQt5.QtWidgets import QCheckBox


class HulaController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

    def connect_signals(self):
        self.view.start_sb.valueChanged.connect(self.__create_ticks)
        self.view.stop_sb.valueChanged.connect(self.__create_ticks)
        self.view.generate_btn.clicked.connect(self.__generate)

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
            cb = QCheckBox(str(num_tick))
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