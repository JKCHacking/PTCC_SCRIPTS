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

        self.setWindowTitle('Hula')
        # self.setFixedSize(300, 300)
        self.generalLayout = QtWidgets.QVBoxLayout()
        self._centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.__create_main_window()
