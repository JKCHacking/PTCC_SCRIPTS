#!/usr/env/bin python

import unittest
import os
import csv
from timesheet_calculator import TimesheetCalculator
from timesheet_calculator_testdata import TimesheetCalculatorTestData
from constants import Constants


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


if __name__ == '__main__':
    unittest.main()
