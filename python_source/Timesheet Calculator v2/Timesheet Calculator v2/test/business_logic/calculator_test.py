import unittest
import datetime
from src.business_logic.calculator import Calculator


class CalculatorTest(unittest.TestCase):
    def test_calculate_total_hours_001(self):
        calculator = Calculator()
        # June 8, 2021 9:00 AM - 6:00 PM
        date = datetime.date(day=8, month=6, year=2021)
        time_in = datetime.time(hour=9)
        time_out = datetime.time(hour=18)
        actual_total_hour = calculator.calculate_task_hours(date, time_in, time_out)
        self.assertEqual(8, actual_total_hour)

    def test_calculate_total_hours_002(self):
        calculator = Calculator()
        # June 8, 2021 11:00PM - 12:30 AM
        date = datetime.date(day=8, month=6, year=2021)
        time_in = datetime.time(hour=23)
        time_out = datetime.time(hour=0, minute=30)
        actual_total_hour = calculator.calculate_task_hours(date, time_in, time_out)
        self.assertEqual(1, actual_total_hour)

    def test_calculate_total_hours_003(self):
        calculator = Calculator()
        # June 8, 2021 12:30 AM - 12:45 AM
        date = datetime.date(day=8, month=6, year=2021)
        time_in = datetime.time(hour=0, minute=30)
        time_out = datetime.time(hour=0, minute=45)
        actual_total_hour = calculator.calculate_task_hours(date, time_in, time_out)
        self.assertEqual(0, actual_total_hour)

    def test_calculate_total_hours_004(self):
        calculator = Calculator()
        # June 8, 2021 12:00 AM - 1:30 AM
        date = datetime.date(day=8, month=6, year=2021)
        time_in = datetime.time(hour=0)
        time_out = datetime.time(hour=1, minute=30)
        actual_total_hour = calculator.calculate_task_hours(date, time_in, time_out)
        self.assertEqual(0.5, actual_total_hour)

    def test_calculate_total_hours_005(self):
        calculator = Calculator()
        # June 8, 2021 12:30 AM - 1:30 AM
        date = datetime.date(day=8, month=6, year=2021)
        time_in = datetime.time(hour=0, minute=30)
        time_out = datetime.time(hour=1, minute=30)
        actual_total_hour = calculator.calculate_task_hours(date, time_in, time_out)
        self.assertEqual(0.5, actual_total_hour)

    def test_calculate_total_hours_006(self):
        calculator = Calculator()
        # June 8, 2021 1:00 AM - 1:30 AM
        date = datetime.date(day=8, month=6, year=2021)
        time_in = datetime.time(hour=1)
        time_out = datetime.time(hour=1, minute=30)
        actual_total_hour = calculator.calculate_task_hours(date, time_in, time_out)
        self.assertEqual(0.5, actual_total_hour)

    def test_calculate_total_hours_007(self):
        calculator = Calculator()
        # June 8, 2021 12:00 AM - 12:30 AM
        date = datetime.date(day=8, month=6, year=2021)
        time_in = datetime.time(hour=0)
        time_out = datetime.time(hour=0, minute=30)
        actual_total_hour = calculator.calculate_task_hours(date, time_in, time_out)
        self.assertEqual(0, actual_total_hour)

    def test_calculate_total_hours_008(self):
        calculator = Calculator()
        # June 8, 2021 12:00 AM - 1:00 AM
        date = datetime.date(day=8, month=6, year=2021)
        time_in = datetime.time(hour=0)
        time_out = datetime.time(hour=1)
        actual_total_hour = calculator.calculate_task_hours(date, time_in, time_out)
        self.assertEqual(0, actual_total_hour)

    def test_calculate_total_hours_009(self):
        calculator = Calculator()
        # June 8, 2021 12:30 AM - 1:00 AM
        date = datetime.date(day=8, month=6, year=2021)
        time_in = datetime.time(hour=0, minute=30)
        time_out = datetime.time(hour=1)
        actual_total_hour = calculator.calculate_task_hours(date, time_in, time_out)
        self.assertEqual(0, actual_total_hour)

    def test_calculate_total_hours_010(self):
        calculator = Calculator()
        # June 8, 2021 11:00 PM - 2:00 AM
        date = datetime.date(day=8, month=6, year=2021)
        time_in = datetime.time(hour=23)
        time_out = datetime.time(hour=2)
        actual_total_hour = calculator.calculate_task_hours(date, time_in, time_out)
        self.assertEqual(2, actual_total_hour)

    def test_calculate_total_hours_011(self):
        calculator = Calculator()
        # June 8, 2021 2:00 AM - 3:00 PM
        date = datetime.date(day=8, month=6, year=2021)
        time_in = datetime.time(hour=2)
        time_out = datetime.time(hour=3)
        actual_total_hour = calculator.calculate_task_hours(date, time_in, time_out)
        self.assertEqual(1, actual_total_hour)

    def test_calculate_total_hours_012(self):
        calculator = Calculator()
        # June 8, 2021 12:30 AM - 6:30 PM
        date = datetime.date(day=8, month=6, year=2021)
        time_in = datetime.time(hour=0, minute=30)
        time_out = datetime.time(hour=6, minute=30)
        actual_total_hour = calculator.calculate_task_hours(date, time_in, time_out)
        self.assertEqual(5, actual_total_hour)

    def test_calculate_total_hours_013(self):
        calculator = Calculator()
        # weekday
        # June 8, 2021 12:00 AM - 8:00 PM
        date = datetime.date(day=8, month=6, year=2021)
        time_in = datetime.time(hour=0)
        time_out = datetime.time(hour=20)
        actual_total_hour = calculator.calculate_task_hours(date, time_in, time_out)
        self.assertEqual(17, actual_total_hour)

    def test_calculate_total_hours_014(self):
        calculator = Calculator()
        # weekend
        # June 12, 2021 12:00 AM - 8:00 PM
        date = datetime.date(day=12, month=6, year=2021)
        time_in = datetime.time(hour=0)
        time_out = datetime.time(hour=20)
        actual_total_hour = calculator.calculate_task_hours(date, time_in, time_out)
        self.assertEqual(16, actual_total_hour)
