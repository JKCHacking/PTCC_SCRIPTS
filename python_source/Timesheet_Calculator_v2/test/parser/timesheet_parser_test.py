import datetime
import unittest
import shutil
import os
from src.utils.constants import Constants
from src.parser.timesheet_parser import TimesheetParser


class TimesheetParserTest(unittest.TestCase):
    def test_parse_001(self):
        test_data = "testdata/test_parse_testdata_001.xlsx"

        # put testdata in input folder
        source = test_data
        dest = os.path.join(Constants.INPUT_DIR, "test_parse_testdata_001.xlsx")
        shutil.copyfile(source, dest)
        # run the test
        ts_parser = TimesheetParser()
        ts_list = ts_parser.parse()
        # assert results
        self.assertEqual(len(ts_list), 1)
        self.assertEqual(ts_list[0].employee.id_number, 1234)
        self.assertEqual(ts_list[0].employee.first_name, "Juan")
        self.assertEqual(ts_list[0].employee.middle_name, "Dela")
        self.assertEqual(ts_list[0].employee.last_name, "Cruz")
        self.assertEqual(len(ts_list[0].tasks), 2)
        self.assertEqual(ts_list[0].tasks[0].date, datetime.datetime.strptime("06/06/2021", "%d/%m/%Y").date())
        self.assertEqual(ts_list[0].tasks[0].start_time, datetime.datetime.strptime("09:00 AM", "%I:%M %p").time())
        self.assertEqual(ts_list[0].tasks[0].end_time, datetime.datetime.strptime("06:00 PM", "%I:%M %p").time())
        self.assertEqual(ts_list[0].tasks[0].task_name, "task1")
        self.assertEqual(ts_list[0].tasks[0].project_name, "project1")
        # remove testdata in input folder
        os.remove(dest)
        # remove result files in output folder

    def test_parse_002(self):
        test_data = "testdata/test_parse_testdata_002.xlsx"

        # put testdata in input folder
        source = test_data
        dest = os.path.join(Constants.INPUT_DIR, "test_parse_testdata_002.xlsx")
        shutil.copyfile(source, dest)
        # run the test
        ts_parser = TimesheetParser()
        ts_list = ts_parser.parse()
        # assert results
        self.assertEqual(len(ts_list), 1)
        self.assertEqual(ts_list[0].employee.id_number, 1234)
        self.assertEqual(ts_list[0].employee.first_name, "Juan")
        self.assertEqual(ts_list[0].employee.middle_name, "Dela")
        self.assertEqual(ts_list[0].employee.last_name, "Cruz")
        self.assertEqual(len(ts_list[0].tasks), 5)
        self.assertEqual(ts_list[0].tasks[0].date, datetime.datetime.strptime("09/06/2021", "%d/%m/%Y").date())
        self.assertEqual(ts_list[0].tasks[0].start_time, datetime.datetime.strptime("09:00 AM", "%I:%M %p").time())
        self.assertEqual(ts_list[0].tasks[0].end_time, datetime.datetime.strptime("06:00 PM", "%I:%M %p").time())
        self.assertEqual(ts_list[0].tasks[0].task_name, "task1")
        self.assertEqual(ts_list[0].tasks[0].project_name, "project1")
        # remove testdata in input folder
        os.remove(dest)
        # remove result files in output folder

    def test_parse_003(self):
        test_data = "testdata/test_parse_testdata_003.xlsx"

        # put testdata in input folder
        source = test_data
        dest = os.path.join(Constants.INPUT_DIR, "test_parse_testdata_003.xlsx")
        shutil.copyfile(source, dest)
        # run the test
        ts_parser = TimesheetParser()
        ts_list = ts_parser.parse()
        # assert results
        self.assertEqual(len(ts_list), 1)
        self.assertEqual(ts_list[0].employee.id_number, 1234)
        self.assertEqual(ts_list[0].employee.first_name, "Joshnee")
        self.assertEqual(ts_list[0].employee.middle_name, "Baring")
        self.assertEqual(ts_list[0].employee.last_name, "Cunanan")
        self.assertEqual(len(ts_list[0].tasks), 1)
        self.assertEqual(ts_list[0].tasks[0].date, datetime.date(year=2021, month=6, day=6))
        self.assertEqual(ts_list[0].tasks[0].start_time, datetime.datetime.strptime("09:00 AM", "%I:%M %p").time())
        self.assertEqual(ts_list[0].tasks[0].end_time, datetime.datetime.strptime("06:00 PM", "%I:%M %p").time())
        self.assertEqual(ts_list[0].tasks[0].task_name, "task2")
        self.assertEqual(ts_list[0].tasks[0].project_name, "project2")
        # remove testdata in input folder
        os.remove(dest)
        # remove result files in output folder