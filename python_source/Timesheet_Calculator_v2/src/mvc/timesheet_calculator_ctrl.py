import datetime
from PyQt5 import QtCore
from src.mvc.timesheet_calculator_ui import TimesheetCalculatorUI
from src.mvc.timesheet_model import TimesheetModel


class TimesheetCalculatorCtrl(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.view = TimesheetCalculatorUI()
        self.model = TimesheetModel()
        self.ss_gen_thread = None
        self.ss_gen_worker = None

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


class SpreadsheetGeneratorWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    def __init__(self, view, model):
        QtCore.QObject.__init__(self)
        self.view = view
        self.model = model

        start_date_str = self.view.from_date_picker.date().toString()
        end_date_str = self.view.to_date_picker.date().toString()
        start_date = datetime.datetime.strptime(start_date_str, "%a %b %d %Y")
        end_date = datetime.datetime.strptime(end_date_str, "%a %b %d %Y")
        self.timesheets = self.model.get_timesheets()
        self.holidays = self.model.get_holidays()

    @QtCore.pyqtSlot()
    def run(self):
        for timesheet in self.timesheets:
            employee = timesheet.get_employee()
            tasks = timesheet.get_tasks()
