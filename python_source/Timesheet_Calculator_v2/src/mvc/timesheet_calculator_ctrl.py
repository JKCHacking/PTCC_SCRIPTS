from PyQt5 import QtCore
from src.mvc.timesheet_calculator_ui import TimesheetCalculatorUI
from src.mvc.timesheet_model import TimesheetModel


class TimesheetCalculatorCtrl(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.view = TimesheetCalculatorUI()
        self.model = TimesheetModel()

        self.connect_signals()

    def connect_signals(self):
        self.view.generate_button.clicked.connect(self.generate)
        self.view.progress_dialog.cancel_button.rejected.connect(self.cancel)

    def init_ui(self):
        self.view.create_window()
        self.view.show()

    def init_model(self):
        self.model.init_model()

    @QtCore.pyqtSlot()
    def generate(self):

        self.view.progress_dialog.init_ui()
        self.view.progress_dialog.exec()

    @QtCore.pyqtSlot()
    def cancel(self):
        pass
