import csv
import datetime


class HolidayParser:
    def __init__(self, holiday_csv_fp):
        self.holiday_csv_fp = holiday_csv_fp

    def parse(self):
        holiday_list = []
        with open(self.holiday_csv_fp, "r", newline='') as csv_f:
            reader = csv.DictReader(csv_f)
            for row in reader:
                try:
                    holiday = datetime.date(day=int(row["date"]),
                                            month=int(row["month"]),
                                            year=int(row["year"]))
                    holiday_list.append(holiday)
                except ValueError:
                    pass
        return holiday_list
