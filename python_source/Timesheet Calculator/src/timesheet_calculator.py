#!/usr/bin/env python
from constants import Constants
from collections import namedtuple
from logger import Logger
import csv
import os
import datetime
import dateutil.parser


class TimesheetCalculator:
    def __init__(self):
        self.logger = Logger().get_logger()
        self.all_employee_list = []

    def calculate_time(self, log_date, time_in, time_out):
        time_in = self.convert_12_hours(time_in)
        time_out = self.convert_12_hours(time_out)
        log_date = self.convert_date(log_date)

        noon_time1 = self.convert_12_hours('12:00 PM')
        noon_time2 = self.convert_12_hours('1:00 PM')

        mid_night1 = self.convert_12_hours('12:00 AM')
        mid_night2 = self.convert_12_hours('1:00 AM')

        before_morning1 = self.convert_12_hours('6:00 AM')
        before_morning2 = self.convert_12_hours('7:00 AM')

        after_evening1 = self.convert_12_hours('6:00 PM')
        after_evening2 = self.convert_12_hours('7:00 PM')

        constraint_counter = 0

        if self.is_within_time(time_in, time_out, noon_time1, noon_time2):
            constraint_counter += self.convert_to_hours(noon_time2 - noon_time1)
        if self.is_within_time(time_in, time_out, mid_night1, mid_night2):
            constraint_counter += self.convert_to_hours(mid_night2 - mid_night1)
        if self.is_within_time(time_in, time_out, before_morning1, before_morning2):
            constraint_counter += self.convert_to_hours(before_morning2 - before_morning1)
        if log_date.weekday() >= 5:
            if self.is_within_time(time_in, time_out, after_evening1, after_evening2):
                constraint_counter += self.convert_to_hours(after_evening2 - after_evening1)

        if time_out == self.convert_12_hours('12:00 AM'):
            time_out += datetime.timedelta(days=1)
        total_hours = self.convert_to_hours(time_out - time_in)
        total_hours -= constraint_counter
        return total_hours

    def is_within_time(self, time_in, time_out, fr_time, to_time):
        is_inside = False
        if time_in < fr_time and time_out > to_time:
            is_inside = True
        elif time_in < fr_time < time_out <= to_time:
            is_inside = True
        elif fr_time <= time_in < to_time < time_out:
            is_inside = True
        elif fr_time < time_in < time_out < to_time:
            is_inside = True

        return is_inside

    def convert_12_hours(self, time_string):
        time_obj = dateutil.parser.parse(time_string)
        time_obj = time_obj.strftime(Constants.TIME_FORMAT)
        time_obj = datetime.datetime.strptime(time_obj, Constants.TIME_FORMAT)
        return time_obj

    def convert_date(self, date_string):
        date_obj = dateutil.parser.parse(date_string)
        date_obj = date_obj.strftime(Constants.DATE_FORMAT)
        date_obj = datetime.datetime.strptime(date_obj, Constants.DATE_FORMAT)
        return date_obj

    def convert_to_hours(self, raw_time):
        (h, m, s) = str(raw_time).split(':')
        time_hours = int(h) + int(m) / 60 + int(s) / 3600
        return time_hours

    def add_to_list(self, timesheet_entry):
        found_flag = False
        Work = namedtuple('Work', ['projectName', 'taskName', 'date', 'timeIn', 'timeOut', 'totalHours'])
        Employee = namedtuple('Employee', ['employeeName', 'work'])

        # employee_name,date,project,task,time_in,time_out
        employee_name = timesheet_entry['employee_name'].strip()
        date = timesheet_entry['date'].strip()
        project = timesheet_entry['project'].strip()
        task = timesheet_entry['task'].strip()
        time_in = timesheet_entry['time_in'].strip()
        time_out = timesheet_entry['time_out'].strip()

        total_hours = self.calculate_time(date, time_in, time_out)
        work_obj = Work(projectName=project, taskName=task, date=date,
                        timeIn=time_in, timeOut=time_out, totalHours=total_hours)

        work_list = [work_obj]
        employee_obj = Employee(employeeName=employee_name, work=work_list)

        if self.all_employee_list:
            for employee in self.all_employee_list:
                if employee.employeeName == employee_name:
                    employee.work.append(work_obj)
                    found_flag = True
                    break
            if not found_flag:
                self.all_employee_list.append(employee_obj)
        else:
            self.all_employee_list.append(employee_obj)

    def display_all_employess(self):
        print(self.all_employee_list)

    def generate_between_days(self, fr_day, to_day):
        fr_day = self.convert_date(fr_day)
        to_day = self.convert_date(to_day)
        emp_list = []

        for employee in self.all_employee_list:
            emp_obj = {}
            rendered_hours = 0
            emp_obj['NAME'] = employee.employeeName
            emp_obj['PROJECT'] = []
            for work in employee.work:
                work_date = self.convert_date(work.date)
                if fr_day <= work_date <= to_day:
                    rendered_hours += work.totalHours
                    emp_obj['TIME_SPEND'] = rendered_hours
                    emp_obj['PROJECT'].append(work.projectName)
                else:
                    emp_obj['TIME_SPEND'] = 0
                    emp_obj['PROJECT'].append('None')

            emp_obj['PROJECT'] = set(emp_obj['PROJECT'])
            emp_obj['PROJECT'] = '/'.join(emp_obj['PROJECT'])
            if emp_obj['TIME_SPEND'] != 0:
                emp_list.append(emp_obj)

        date_today = datetime.datetime.today().strftime(Constants.DATE_FORMAT)
        output_path = os.path.join(Constants.OUTPUT_DIR, f'result_{fr_day.date()}_{to_day.date()}.csv')
        with open(output_path, 'w', newline='', encoding='utf-8') as output_csv:
            output_csv.write(f'PTCC TIME SHEET FOR WEEK ({fr_day.date()} to {to_day.date()})\n')
            output_csv.write(f'{date_today}\n\n')

            field_names = ['NAME', 'PROJECT', 'TIME_SPEND']
            csv_writer = csv.DictWriter(output_csv, fieldnames=field_names)
            csv_writer.writeheader()
            for data in emp_list:
                csv_writer.writerow(data)

    def generate_manhour_analysis(self, fr_day, to_day):
        fr_day = self.convert_date(fr_day)
        to_day = self.convert_date(to_day)



if __name__ == '__main__':
    logger = Logger().get_logger()
    input_csv_path = os.path.join(Constants.INPUT_DIR, 'timesheet.csv')
    ts_calc = TimesheetCalculator()

    logger.info('Importing Datasheet...')
    try:
        with open(input_csv_path, newline='') as timesheet_csv:
            reader = csv.DictReader(timesheet_csv)
            for row in reader:
                ts_calc.add_to_list(row)
    except FileNotFoundError as e:
        logger.error(e.strerror)
        logger.error('File not found!')
    logger.info('Importing Datasheet done..')

    fr_date = input('Input the from date <DD-MM-YYYY>: ')
    to_date = input('Input the to date <DD-MM-YYYY>: ')

    ts_calc.generate_between_days(fr_date, to_date)
