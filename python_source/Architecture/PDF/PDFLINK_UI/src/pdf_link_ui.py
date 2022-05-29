import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QSpinBox


class PDFLinkUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # initialize UI Widgets
        self.keyword_line_edit = QLineEdit()
        self.page_line_edit = QLineEdit()
        self.pdf_fp_line_edit = QLineEdit()
        self.pdf_fp_line_edit.setReadOnly(True)
        self.browse_button = QPushButton("Browse")
        self.ok_button = None
        self.cancel_button = None
        self.pdf_file_path = ""

        self.setWindowTitle('PDF Linker')
        self.setFixedSize(500, 135)

        self.c_widget = QWidget(self)
        self.setCentralWidget(self.c_widget)
        self.general_layout = QVBoxLayout()
        self.c_widget.setLayout(self.general_layout)
        self.init_ui()

    def init_ui(self):
        # creating Main UI
        file_picker_layout = QHBoxLayout()
        file_picker_layout.addWidget(self.pdf_fp_line_edit)
        file_picker_layout.addWidget(self.browse_button)

        form_layout = QFormLayout()
        form_layout.addRow('PDF File:', file_picker_layout)
        form_layout.addRow('Keyword:', self.keyword_line_edit)
        form_layout.addRow('Page to link:', self.page_line_edit)
        self.general_layout.addLayout(form_layout)

        # initializing ok and cancel buttons
        buttons = QDialogButtonBox()
        buttons.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        )
        self.ok_button = buttons.accepted
        self.cancel_button = buttons.rejected
        self.general_layout.addWidget(buttons)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                   "Open File",
                                                   "H:\Desktop",
                                                   "*.pdf",
                                                   options=QFileDialog.DontUseNativeDialog)
        self.pdf_file_path = file_path
        self.pdf_fp_line_edit.setText(os.path.basename(file_path))

    def messagebox(self, message, icon):
        msg = QMessageBox()
        if icon == "Warning":
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Warning")
        else:
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Information")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def clear(self):
        # make to default values
        self.pdf_fp_line_edit.setText("")
        self.keyword_line_edit.setText("")
        self.page_line_edit.setText("")
