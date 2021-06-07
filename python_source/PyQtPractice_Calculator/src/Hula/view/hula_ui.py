from PyQt5 import QtWidgets


class HulaUI(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        # widgets
        self.start_label = QtWidgets.QLabel("Start:")
        self.stop_label = QtWidgets.QLabel("Stop:")
        self.start_sb = QtWidgets.QSpinBox()
        self.stop_sb = QtWidgets.QSpinBox()
        self.generate_btn = QtWidgets.QPushButton("Generate")
        self.reset_btn = QtWidgets.QPushButton("Reset")
        self.generate_btn.setFixedSize(100, 50)
        self.guessed_label = QtWidgets.QLabel("Guessed:")
        self.guessed_result_label = QtWidgets.QLabel()
        self.tickbox_layout = QtWidgets.QGridLayout()
        self.bot_launcher_btn = QtWidgets.QPushButton("Launch Bot")

        self.setWindowTitle('Hula')
        # self.setFixedSize(300, 300)
        self.generalLayout = QtWidgets.QVBoxLayout()
        self._centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

    def create_main_window(self):
        upper_layout = QtWidgets.QHBoxLayout()
        center_layout = QtWidgets.QHBoxLayout()
        lower_layout = QtWidgets.QHBoxLayout()

        upper_layout.addWidget(self.start_label)
        upper_layout.addWidget(self.start_sb)
        upper_layout.addWidget(self.stop_label)
        upper_layout.addWidget(self.stop_sb)

        center_layout.addLayout(self.tickbox_layout)

        lower_layout.addWidget(self.guessed_label)
        lower_layout.addWidget(self.guessed_result_label)
        lower_layout.addWidget(self.generate_btn)
        lower_layout.addWidget(self.bot_launcher_btn)

        self.generalLayout.addLayout(upper_layout)
        self.generalLayout.addLayout(center_layout)
        self.generalLayout.addLayout(lower_layout)
