import sys
import random
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QCheckBox


class HulaUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # widgets
        self.start_label = QLabel("Start:")
        self.stop_label = QLabel("Stop:")
        self.start_sb = QSpinBox()
        self.stop_sb = QSpinBox()
        self.generate_btn = QPushButton("Generate")
        self.reset_btn = QPushButton("Reset")
        self.generate_btn.setFixedSize(100, 50)
        self.guessed_label = QLabel("Guessed:")
        self.guessed_result_label = QLabel()
        self.tickbox_layout = QGridLayout()

        self.setWindowTitle('Hula')
        # self.setFixedSize(300, 300)
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.__create_main_window()

    def __create_main_window(self):
        upper_layout = QHBoxLayout()
        center_layout = QHBoxLayout()
        lower_layout = QHBoxLayout()

        upper_layout.addWidget(self.start_label)
        upper_layout.addWidget(self.start_sb)
        upper_layout.addWidget(self.stop_label)
        upper_layout.addWidget(self.stop_sb)

        center_layout.addLayout(self.tickbox_layout)

        lower_layout.addWidget(self.guessed_label)
        lower_layout.addWidget(self.guessed_result_label)
        lower_layout.addWidget(self.generate_btn)

        self.generalLayout.addLayout(upper_layout)
        self.generalLayout.addLayout(center_layout)
        self.generalLayout.addLayout(lower_layout)


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


class HulaGenerator:
    def __init__(self):
        self.taken = []

    def clear_taken(self):
        self.taken = []

    def add_taken(self, item):
        self.taken.append(item)

    def remove_taken(self, item):
        self.taken.remove(item)

    def generate(self, start, stop):
        if len(list(range(start, stop + 1))) == len(self.taken):
            rand_guessed = "Nothing To Guess"
        else:
            guessed = []
            while True:
                rand_guessed = random.randint(start, stop)
                if rand_guessed not in self.taken:
                    guessed.append(rand_guessed)
                    if guessed.count(rand_guessed) == 3:
                        break
        return rand_guessed


def main():
    app = QApplication(sys.argv)
    view = HulaUI()
    view.show()
    model = HulaGenerator()
    controller = HulaController(view, model)
    controller.connect_signals()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
