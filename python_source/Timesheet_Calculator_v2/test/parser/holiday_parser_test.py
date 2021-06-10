import os
import unittest
from src.utils.constants import Constants
from src.parser.holiday_parser import HolidayParser


class HolidayParserTest(unittest.TestCase):
    def test_holiday_parser_001(self):
        expected_holidays = [
            "January 01, 2021",
            "April 01, 2021",
            "April 02, 2021",
            "April 09, 2021",
            "May 01, 2021",
            "June 12, 2021",
            "August 30, 2021",
            "November 30, 2021",
            "December 25, 2021",
            "December 30, 2021",
            "February 12, 2021",
            "February 25, 2021",
            "April 03, 2021",
            "August 21, 2021",
            "November 01, 2021",
            "December 08, 2021",
            "November 02, 2021",
            "December 24, 2021",
            "December 31, 2021"
        ]
        holiday_csv_fp = os.path.join(Constants.FILES_DIR, "holiday.csv")
        holiday_parser = HolidayParser(holiday_csv_fp)
        actual = holiday_parser.parse()
        self.assertEqual(19, len(actual))
        for holiday in actual:
            holiday_str = holiday.strftime("%B %d, %Y")
            self.assertTrue(holiday_str in expected_holidays)

    def test_holiday_parser_002(self):
        testdata_fp = os.path.join(Constants.TEST_DIR, "parser", "testdata", "holiday_parser_testdata_001.csv")
        holiday_parser = HolidayParser(testdata_fp)
        actual = holiday_parser.parse()
        self.assertEqual(0, len(actual))
