import os
from src.parser.holiday_parser import HolidayParser
from src.parser.timesheet_parser import TimesheetParser
from src.utils.constants import Constants


class TimesheetModel:
    def __init__(self):
        self.timesheet_list = []
        self.holiday_list = []

    def init_model(self):
        holiday_csv_fp = os.path.join(Constants.FILES_DIR, "holiday.csv")
        holiday_parser = HolidayParser(holiday_csv_fp)
        self.holiday_list = holiday_parser.parse()
        ts_parser = TimesheetParser()
        self.timesheet_list = ts_parser.parse()

    def get_timesheets(self):
        return self.timesheet_list

    def get_holidays(self):
        return self.holiday_list
