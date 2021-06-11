import datetime
from collections import namedtuple


class Calculator:
    def __init__(self, from_date, to_date):
        self.from_date = from_date
        self.to_date = to_date

    def calculate_total_hour(self, date, time_in, time_out):
        time_in_datetime = datetime.datetime.combine(date, time_in)
        time_out_datetime = datetime.datetime.combine(date, time_out)
        if time_in_datetime > time_out_datetime:
            time_out_datetime += datetime.timedelta(days=1)
        decrement_seconds = self.__decrement_prohibit_hours(date, time_in_datetime, time_out_datetime)
        time_delta = time_out_datetime - time_in_datetime
        total_seconds = time_delta.total_seconds() - decrement_seconds
        total_hours = total_seconds / 3600
        return total_hours

    def __decrement_prohibit_hours(self, date, time_in_datetime, time_out_datetime):
        decrement_seconds = 0
        # prohibit hours
        midnight_start = datetime.datetime(day=date.day, month=date.month, year=date.year, hour=0)
        midnight_end = datetime.datetime(day=date.day, month=date.month, year=date.year, hour=1)
        morning_start = datetime.datetime(day=date.day, month=date.month, year=date.year, hour=6)
        morning_end = datetime.datetime(day=date.day, month=date.month, year=date.year, hour=7)
        lunch_start = datetime.datetime(day=date.day, month=date.month, year=date.year, hour=12)
        lunch_end = datetime.datetime(day=date.day, month=date.month, year=date.year, hour=13)
        evening_start = datetime.datetime(day=date.day, month=date.month, year=date.year, hour=18)
        evening_end = datetime.datetime(day=date.day, month=date.month, year=date.year, hour=19)

        if time_out_datetime.time() > midnight_start.time() and time_in_datetime.day < time_out_datetime.day:
            midnight_start += datetime.timedelta(days=1)
            midnight_end += datetime.timedelta(days=1)
        if time_out_datetime.time() > morning_start.time() and time_in_datetime.day < time_out_datetime.day:
            morning_start += datetime.timedelta(days=1)
            morning_end += datetime.timedelta(days=1)
        if time_out_datetime.time() > lunch_start.time() and time_in_datetime.day < time_out_datetime.day:
            lunch_start += datetime.timedelta(days=1)
            lunch_end += datetime.timedelta(days=1)
        if time_out_datetime.time() > evening_start.time() and time_in_datetime.day < time_out_datetime.day:
            evening_start += datetime.timedelta(days=1)
            evening_end += datetime.timedelta(days=1)

        # midnight
        if self.__is_overlap(time_in_datetime, time_out_datetime, midnight_start, midnight_end):
            decrement_seconds += self.__overlap_seconds(time_in_datetime, time_out_datetime,
                                                        midnight_start, midnight_end)
        # morning
        if self.__is_overlap(time_in_datetime, time_out_datetime, morning_start, morning_end):
            decrement_seconds += self.__overlap_seconds(time_in_datetime, time_out_datetime, morning_start, morning_end)
        # lunch
        if self.__is_overlap(time_in_datetime, time_out_datetime, lunch_start, lunch_end):
            decrement_seconds += self.__overlap_seconds(time_in_datetime, time_out_datetime, lunch_start, lunch_end)
        # weekend evening
        if date.weekday() >= 5 and self.__is_overlap(time_in_datetime, time_out_datetime, evening_start, evening_end):
            decrement_seconds += self.__overlap_seconds(time_in_datetime, time_out_datetime, evening_start, evening_end)
        return decrement_seconds

    def __is_overlap(self, dta_start, dta_end, dtb_start, dtb_end):
        # uses De Morgan's Law to determine whether two ranges overlap on each other.
        # https://stackoverflow.com/questions/325933/determine-whether-two-date-ranges-overlap
        return max(dta_start, dtb_start) < min(dta_end, dtb_end)

    def __overlap_seconds(self, dta_start, dta_end, dtb_start, dtb_end):
        # uses De Morgan's Law to determine the value of overlap of two range. 0 if one completely overlaps the other
        # https://stackoverflow.com/questions/9044084/efficient-date-range-overlap-calculation-in-python
        return (min(dta_end, dtb_end) - max(dta_start, dtb_start)).total_seconds()

