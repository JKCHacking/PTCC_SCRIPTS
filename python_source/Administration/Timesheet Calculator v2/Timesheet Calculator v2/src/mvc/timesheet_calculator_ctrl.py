import datetime
import time
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
        self.view.progress_dialog.close_button.clicked.connect(self.close)
        self.view.progress_dialog.cancel_button.clicked.connect(self.cancel)
        self.view.progress_dialog.rerun_button.clicked.connect(self.generate)

    def init_ui(self):
        self.view.create_window()
        self.view.show()

    @QtCore.pyqtSlot()
    def generate(self):
        start_date_str = self.view.from_date_picker.date().toString()
        end_date_str = self.view.to_date_picker.date().toString()
        start_date = datetime.datetime.strptime(start_date_str, "%a %b %d %Y").date()
        end_date = datetime.datetime.strptime(end_date_str, "%a %b %d %Y").date()
        if start_date > end_date:
            self.view.display_message_box("From date is greater than To date.", "error")
            return
        self.model.init_model()
        timesheets = self.model.get_timesheets()
        if len(timesheets) == 0:
            self.view.display_message_box("No timesheet detected.", "warning")
            return
        holidays = self.model.get_holidays()
        self.ss_gen_thread = QtCore.QThread()
        self.ss_gen_worker = SpreadsheetGeneratorWorker(start_date, end_date, timesheets, holidays)
        self.ss_gen_worker.moveToThread(self.ss_gen_thread)
        self.ss_gen_worker.progress_message.connect(self.set_progress_label)
        self.ss_gen_worker.progress_percentage.connect(self.set_progress_bar)
        self.ss_gen_worker.finished.connect(self.done)
        self.ss_gen_worker.finished.connect(self.ss_gen_thread.quit)
        self.ss_gen_worker.finished.connect(self.ss_gen_worker.deleteLater)
        self.ss_gen_thread.started.connect(self.ss_gen_worker.run)
        self.ss_gen_thread.finished.connect(self.ss_gen_thread.deleteLater)
        self.ss_gen_thread.start()

        self.view.progress_dialog.close_button.setEnabled(False)
        self.view.progress_dialog.cancel_button.setEnabled(True)
        self.view.progress_dialog.rerun_button.setEnabled(False)
        if not self.view.progress_dialog.isVisible():
            self.view.progress_dialog.init_ui()
            self.view.progress_dialog.exec_()

    @QtCore.pyqtSlot()
    def cancel(self):
        self.view.progress_dialog.progress_message_label.setText("Cancelling...")
        self.ss_gen_thread.quit()
        self.ss_gen_thread.wait()
        self.view.progress_dialog.progress_message_label.setText("Cancelled")
        self.view.progress_dialog.progress_label.setText("")
        self.view.progress_dialog.progress_bar.setValue(0)
        self.view.progress_dialog.close_button.setEnabled(True)
        self.view.progress_dialog.cancel_button.setEnabled(False)
        self.view.progress_dialog.rerun_button.setEnabled(True)

    @QtCore.pyqtSlot()
    def close(self):
        self.view.progress_dialog.close()

    @QtCore.pyqtSlot(str)
    def set_progress_label(self, message):
        self.view.progress_dialog.progress_message_label.setText(message)

    @QtCore.pyqtSlot(int)
    def set_progress_bar(self, percentage):
        complete = "{}% Complete".format(percentage)
        self.view.progress_dialog.progress_label.setText(complete)
        self.view.progress_dialog.progress_bar.setValue(percentage)

    def done(self):
        self.view.progress_dialog.close_button.setEnabled(True)
        self.view.progress_dialog.cancel_button.setEnabled(False)
        self.view.progress_dialog.rerun_button.setEnabled(True)


class SpreadsheetGeneratorWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    progress_message = QtCore.pyqtSignal(str)
    progress_percentage = QtCore.pyqtSignal(int)

    def __init__(self, start_date, end_date, timesheets, holidays):
        QtCore.QObject.__init__(self)
        self.start_date = start_date
        self.end_date = end_date
        self.timesheets = timesheets
        self.holidays = holidays

    @QtCore.pyqtSlot()
    def run(self):
        timing = 0.01
        total_progress = len(self.timesheets) + 2  # all employee sheets + summary sheets + saving
        current_progress = 0
        ts_wb = TimesheetWorkbook(self.start_date, self.end_date)
        summ_ts = SummarySpreadsheet(ts_wb)
        summ_ts.write_headers()
        for i, timesheet in enumerate(self.timesheets):
            employee = timesheet.get_employee()
            tasks = timesheet.get_tasks()
            emp_ts = EmployeeSpreadsheet(ts_wb, employee, tasks, self.holidays)
            emp_ts.write_headers()
            emp_ts.write_body()
            summ_ts.write_body(employee, tasks)
            current_progress += 1
            self.progress_message.emit("Creating Employee sheet ({}/{})...".format(i + 1, len(self.timesheets)))
            self.progress_percentage.emit((current_progress / total_progress) * 100)
            time.sleep(timing)
        self.progress_message.emit("Creating Summary Sheet...")
        time.sleep(timing)
        summ_ts.write_footers()
        current_progress += 1
        self.progress_percentage.emit((current_progress / total_progress) * 100)
        self.progress_message.emit("Saving to output folder...")
        time.sleep(timing)
        ts_wb.save()
        current_progress += 1
        self.progress_percentage.emit((current_progress / total_progress) * 100)
        time.sleep(timing)
        self.finished.emit()
