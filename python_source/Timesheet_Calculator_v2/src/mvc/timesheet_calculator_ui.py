from PyQt5 import QtWidgets, QtCore


class TimesheetCalculatorUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.from_date_label = QtWidgets.QLabel("From Date")
        self.to_date_label = QtWidgets.QLabel("To Date")
        self.from_date_picker = QtWidgets.QDateEdit(calendarPopup=True)
        self.from_date_picker.setDate(QtCore.QDate.currentDate())
        self.to_date_picker = QtWidgets.QDateEdit(calendarPopup=True)
        self.to_date_picker.setDate(QtCore.QDate.currentDate())
        self.generate_button = QtWidgets.QPushButton("Generate")
        self.generate_button.setFixedSize(70, 50)
        self.general_layout = QtWidgets.QVBoxLayout()
        self.central_widget = QtWidgets.QWidget(self)
        self.progress_dialog = TimesheetProgressDialog(self)

    def create_window(self):
        from_date_layout = QtWidgets.QVBoxLayout()
        to_date_layout = QtWidgets.QVBoxLayout()
        from_date_layout.addWidget(self.from_date_label)
        from_date_layout.addWidget(self.from_date_picker)
        to_date_layout.addWidget(self.to_date_label)
        to_date_layout.addWidget(self.to_date_picker)
        self.general_layout.addLayout(from_date_layout)
        self.general_layout.addLayout(to_date_layout)
        self.general_layout.addWidget(self.generate_button, alignment=QtCore.Qt.AlignRight)
        self.central_widget.setLayout(self.general_layout)
        self.setWindowTitle("Timesheet Calculator")
        self.resize(300, 100)
        self.setCentralWidget(self.central_widget)

    def display_message_box(self, message, level):
        msg = QtWidgets.QMessageBox()
        if level == "info":
            msg.setIcon(QtWidgets.QMessageBox.Information)
        elif level == "warning":
            msg.setIcon(QtWidgets.QMessageBox.Warning)
        elif level == "error":
            msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Message")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()


class TimesheetProgressDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.progress_message_label = QtWidgets.QLabel("")
        self.progress_label = QtWidgets.QLabel("")
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.close_button = QtWidgets.QPushButton("OK")
        self.rerun_button = QtWidgets.QPushButton("Rerun")

    def init_ui(self):
        general_layout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.close_button)
        button_layout.addWidget(self.rerun_button)
        button_layout.addWidget(self.cancel_button, alignment=QtCore.Qt.AlignRight)
        general_layout.addWidget(self.progress_message_label)
        general_layout.addWidget(self.progress_label)
        general_layout.addWidget(self.progress_bar)
        general_layout.addLayout(button_layout)
        self.setLayout(general_layout)
        self.resize(250, 100)
        self.setWindowTitle("Timesheet Calculator")
