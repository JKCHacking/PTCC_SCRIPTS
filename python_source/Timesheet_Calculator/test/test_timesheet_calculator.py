#!/usr/env/bin python

import unittest
import os
import csv
from openpyxl import Workbook
from src.timesheet_calculator import TimesheetCalculator
from src.constants import Constants


class TestTimesheetCalculator(unittest.TestCase):

    def test_get_sunday_cluster(self):
        ts_calc = TimesheetCalculator()

        fr_day = ts_calc.convert_date('May 7, 2020')
        to_day = ts_calc.convert_date('May 21, 2020')
        sunday_cluster_list = ts_calc.get_sunday_clusters(fr_day, to_day)

        self.assertEqual(len(sunday_cluster_list), 3)
        self.assertEqual(len(sunday_cluster_list[0]), 4)
        self.assertEqual(len(sunday_cluster_list[1]), 7)
        self.assertEqual(len(sunday_cluster_list[2]), 4)

    def test_generate_manhour_analysis(self):
        ts_calc = TimesheetCalculator()
        test_csv = os.path.join(Constants.TEST_DIR, 'test_timesheet.csv')
        with open(test_csv, newline='') as csv_test:
            reader = csv.DictReader(csv_test)
            for row in reader:
                ts_calc.add_to_list(row)

        ts_calc.generate_manhour_analysis('April 25, 2020', 'April 30, 2020')

        fr_day = ts_calc.convert_date('April 25, 2020')
        to_day = ts_calc.convert_date('April 30, 2020')
        output_path = os.path.join(Constants.OUTPUT_DIR, f'employee_timesheet_{fr_day.date()}_{to_day.date()}.xlsx')

        file_not_found = False
        try:
            open(output_path)
        except (FileNotFoundError, FileExistsError):
            file_not_found = True

        self.assertEqual(file_not_found, False)

    def test_generate_manhour_analysis_on_holiday(self):
        ts_calc = TimesheetCalculator()
        test_csv = os.path.join(Constants.TEST_DIR, 'test_timesheet_holiday.csv')
        with open(test_csv, newline='') as csv_test:
            reader = csv.DictReader(csv_test)
            for row in reader:
                ts_calc.add_to_list(row)

        from_date_str = 'January 1, 2020'
        to_date_str = 'January 31, 2020'

        ts_calc.generate_manhour_analysis(from_date_str, to_date_str)

        fr_day = ts_calc.convert_date(from_date_str)
        to_day = ts_calc.convert_date(to_date_str)
        output_path = os.path.join(Constants.OUTPUT_DIR,
                                   f'employee_timesheet_{fr_day.date()}_{to_day.date()}.xlsx')

        file_not_found = False
        try:
            open(output_path)
        except (FileNotFoundError, FileExistsError):
            file_not_found = True

        self.assertEqual(file_not_found, False)

    def test_is_holiday(self):
        ts_calc = TimesheetCalculator()
        day_str = 'January 1, 2020'
        self.assertEqual(ts_calc.is_holiday(day_str), True)

    def test_not_holiday(self):
        ts_calc = TimesheetCalculator()
        day_str = 'January 2, 2020'
        self.assertEqual(ts_calc.is_holiday(day_str), False)

    def test_adjust_cell_width(self):
        ts_calc = TimesheetCalculator()
        test_workbook = Workbook()
        worksheet = test_workbook.active

        row = ['1', '1\n2\n', '1\n2\n1\n']
        worksheet.append(row)
        row = ['123']
        worksheet.append(row)
        row = ['1234']
        worksheet.append(row)
        row = ['1\n', '1\n1\n1\n', '1\n2\n']
        worksheet.append(row)
        row = [1, 1.5, 2]
        worksheet.append(row)

        ts_calc.adjust_cell_height_width(worksheet)

        self.assertEqual(4, worksheet.column_dimensions['A'].width)
        self.assertEqual(8, worksheet.row_dimensions[1].height)
        self.assertEqual(12, worksheet.row_dimensions[4].height)
        self.assertEqual(None, worksheet.row_dimensions[5].height)
        self.assertEqual(None, worksheet.row_dimensions[2].height)

    def test_calculate_time_weekday(self):
        ts_calc = TimesheetCalculator()
        weekday = 'May 4,2020'
        time_in = '1:00 AM'
        time_out = '8:00 PM'
        total_hours = ts_calc.calculate_time(weekday, time_in, time_out)

        self.assertEqual(17, total_hours)

    def test_calculate_time_weekend(self):
        ts_calc = TimesheetCalculator()
        weekend = '5-9-2020'
        time_in = '1:00 AM'
        time_out = '8:00 PM'
        total_hours = ts_calc.calculate_time(weekend, time_in, time_out)

        self.assertEqual(16, total_hours)

    def test_calculate_time_midnight(self):
        ts_calc = TimesheetCalculator()
        weekend = '5/9/2020'
        weekday = 'May 4,2020'
        time_in = '9:00 PM'
        time_out = '12:00 AM'

        total_hours = ts_calc.calculate_time(weekend, time_in, time_out)
        self.assertEqual(3, total_hours)

        total_hours = ts_calc.calculate_time(weekday, time_in, time_out)
        self.assertEqual(3, total_hours)

    def test_calculate_time_midnight_weekday(self):
        ts_calc = TimesheetCalculator()
        weekday = 'May 4, 2020'
        time_in = '12:00 AM'
        time_out = '8:00 PM'

        total_hours = ts_calc.calculate_time(weekday, time_in, time_out)
        self.assertEqual(17, total_hours)

    def test_calculate_time_midnight_weekend(self):
        ts_calc = TimesheetCalculator()
        weekend = 'May 9, 2020'
        time_in = '12:00 AM'
        time_out = '8:00 PM'

        total_hours = ts_calc.calculate_time(weekend, time_in, time_out)
        self.assertEqual(16, total_hours)

    def test_calculate_time_shortcut_time(self):
        ts_calc = TimesheetCalculator()
        weekday = 'May 4, 2020'
        time_in = '12 AM'
        time_out = '8PM'

        total_hours = ts_calc.calculate_time(weekday, time_in, time_out)
        self.assertEqual(17, total_hours)

    def test_add_to_list_invalid_time(self):
        ts_calc = TimesheetCalculator()
        time_sheet_entry = {
            'employee_name': 'emp001',
            'date': 'April 4, 2020',
            'project': 'project001',
            'task': 'task001',
            'time_in': 'invalid time',
            'time_out': 'invalid time'
        }

        self.assertEqual(-1, ts_calc.add_to_list(time_sheet_entry))

    def test_add_to_list_invalid_date(self):
        ts_calc = TimesheetCalculator()
        time_sheet_entry = {
            'employee_name': 'emp001',
            'date': 'Invalid date',
            'project': 'project001',
            'task': 'task001',
            'time_in': '12:00 AM',
            'time_out': '1:00 PM'
        }

        self.assertEqual(-1, ts_calc.add_to_list(time_sheet_entry))

    def test_add_to_list_shortcut_date(self):
        ts_calc = TimesheetCalculator()
        time_sheet_entry = {
            'employee_name': 'emp001',
            'date': '12-Apr-20',
            'project': 'project001',
            'task': 'task001',
            'time_in': '12:00 AM',
            'time_out': '1:00 PM'
        }

        self.assertEqual(1, ts_calc.add_to_list(time_sheet_entry))

    def test_add_to_list_reverse_log_time(self):
        ts_calc = TimesheetCalculator()
        time_sheet_entry = {
            'employee_name': 'emp001',
            'date': 'April 4, 2020',
            'project': 'project001',
            'task': 'task001',
            'time_in': '9:00 PM',
            'time_out': '8:00 PM'
        }

        self.assertEqual(-1, ts_calc.add_to_list(time_sheet_entry))

    def test_add_to_list_reverse_midnight_out(self):
        ts_calc = TimesheetCalculator()
        time_sheet_entry = {
            'employee_name': 'emp001',
            'date': 'April 4, 2020',
            'project': 'project001',
            'task': 'task001',
            'time_in': '9:00 PM',
            'time_out': '12:00 AM'
        }

        self.assertEqual(1, ts_calc.add_to_list(time_sheet_entry))
