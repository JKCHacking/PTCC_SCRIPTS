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
