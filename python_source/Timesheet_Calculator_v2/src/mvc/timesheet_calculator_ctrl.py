import datetime
from PyQt5 import QtCore
from src.mvc.timesheet_calculator_ui import TimesheetCalculatorUI
from src.mvc.timesheet_model import TimesheetModel
from src.business_logic.timesheet_workbook import TimesheetWorkbook
from src.business_logic.employee_spreadsheet import EmployeeSpreadsheet
from src.business_logic.summary_spreadsheet import SummarySpreadsheet


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
        # start_date_str = self.view.from_date_picker.date().toString()
        # end_date_str = self.view.to_date_picker.date().toString()

    @QtCore.pyqtSlot()
    def cancel(self):
        pass


class SpreadsheetGeneratorWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    def __init__(self, start_date, end_date, timesheets, holidays):
        QtCore.QObject.__init__(self)
        self.start_date = start_date
        self.end_date = end_date
        self.timesheets = timesheets
        self.holidays = holidays

    @QtCore.pyqtSlot()
    def run(self):
        ts_wb = TimesheetWorkbook(self.start_date, self.end_date)
        summ_ts = SummarySpreadsheet(ts_wb)
        summ_ts.write_headers()
        for timesheet in self.timesheets:
            employee = timesheet.get_employee()
            tasks = timesheet.get_tasks()
            emp_ts = EmployeeSpreadsheet(ts_wb, employee, tasks)
            emp_ts.write_headers()
            emp_ts.write_body()
            summ_ts.write_body(employee, tasks)
        summ_ts.write_footers()
        ts_wb.save()
