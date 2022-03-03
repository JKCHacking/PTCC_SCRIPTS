import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore
from controller import Controller
from model import Model


class GUI(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.input_edit = QLineEdit()
        self.input_edit.setFixedHeight(22.5)
        self.input_label = QLabel("INPUT PDF")
        self.output_edit = QLineEdit()
        self.output_edit.setFixedHeight(22.5)
        self.output_label = QLabel("OUTPUT PDF")

        self.page_label = QLabel("Page")
        self.pad_top_edit = QLineEdit()
        self.pad_bot_edit = QLineEdit()
        self.pad_left_edit = QLineEdit()
        self.pad_right_edit = QLineEdit()
        self.page_label.setFixedWidth(25)
        self.pad_top_edit.setFixedWidth(25)
        self.pad_bot_edit.setFixedWidth(25)
        self.pad_left_edit.setFixedWidth(25)
        self.pad_right_edit.setFixedWidth(25)
        self.pad_top_edit.setText("0")
        self.pad_bot_edit.setText("0")
        self.pad_left_edit.setText("0")
        self.pad_right_edit.setText("0")

        button_ss = """
            QPushButton{
                border-radius:5px;
                border:1px solid black;
                border-style: outset;
                background-color:#9e9e9e;
            }
            QPushButton:pressed {
                background-color:#757575;
            }
        """
        self.browse_button = QPushButton("BROWSE")
        self.browse_button.setStyleSheet(button_ss)
        self.split_button = QPushButton("SPLIT")
        self.split_button.setStyleSheet(button_ss)
        self.split_button.setFixedWidth(75)
        self.split_button.setFixedHeight(25)
        self.browse_button.setFixedWidth(75)
        self.browse_button.setFixedHeight(22.5)

        self.pdf_file_path = ""

        self.c_widget = QWidget(self)
        self.setCentralWidget(self.c_widget)
        self.general_layout = QVBoxLayout()
        self.c_widget.setLayout(self.general_layout)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PDF SPLITTER")
        self.setFixedSize(250, 275)

        file_picker_layout = QHBoxLayout()
        file_picker_layout.addWidget(self.input_edit)
        file_picker_layout.addWidget(self.browse_button)

        io_layout = QFormLayout()
        io_layout.addRow(self.input_label)
        io_layout.addRow(file_picker_layout)
        io_layout.addRow(self.output_label)
        io_layout.addRow(self.output_edit)

        io_groupbox = QGroupBox()
        io_groupbox.setLayout(io_layout)

        padding_layout = QVBoxLayout()
        padding_layout.addWidget(self.pad_top_edit, alignment=QtCore.Qt.AlignCenter)
        h1 = QHBoxLayout()
        h1.addWidget(self.pad_left_edit, alignment=QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        h1.addWidget(self.page_label, alignment=QtCore.Qt.AlignCenter)
        h1.addWidget(self.pad_right_edit, alignment=QtCore.Qt.AlignCenter | QtCore.Qt.AlignLeft)
        padding_layout.addLayout(h1)
        padding_layout.addWidget(self.pad_bot_edit, alignment=QtCore.Qt.AlignCenter)

        pad_groupbox = QGroupBox("PADDING")
        pad_groupbox.setLayout(padding_layout)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(5, 10, 5, 5)
        button_layout.addWidget(self.split_button, alignment=QtCore.Qt.AlignCenter)

        self.general_layout.addWidget(io_groupbox)
        self.general_layout.addWidget(pad_groupbox)
        self.general_layout.addLayout(button_layout)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                   "Open File",
                                                   "H:\Desktop",
                                                   "*.pdf",
                                                   options=QFileDialog.DontUseNativeDialog)
        self.pdf_file_path = file_path
        self.input_edit.setText(file_path)

    def display_message_box(self, message, level="info"):
        msg = QMessageBox()
        if level == "info":
            msg.setIcon(QMessageBox.Information)
        elif level == "warning":
            msg.setIcon(QMessageBox.Warning)
        elif level == "error":
            msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Message")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def clear_all(self):
        self.input_edit.setText("")
        self.output_edit.setText("")
        self.pad_top_edit.setText("0")
        self.pad_bot_edit.setText("0")
        self.pad_right_edit.setText("0")
        self.pad_left_edit.setText("0")


class Application(QApplication):
    def __init__(self, argv):
        super(Application, self).__init__(argv)
        self.model = Model()
        self.view = GUI()
        self.controller = Controller(self.model, self.view)

    def show(self):
        self.view.show()
