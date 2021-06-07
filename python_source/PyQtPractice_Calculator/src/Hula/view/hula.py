from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QLabel


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
