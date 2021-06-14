import os
import openpyxl
from src.utils.constants import Constants


class TimesheetWorkbook:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.workbook = openpyxl.Workbook()
        self.output_path = os.path.join(Constants.OUTPUT_DIR, "Employee Timesheet {} to {}.xlsx".format(
            self.start_date.strftime("%d-%b-%Y"), self.end_date.strftime("%d-%b-%Y")))

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_output_path(self):
        return self.output_path

    def get_workbook(self):
        return self.workbook

    def save(self):
        self.workbook.save(self.output_path)
