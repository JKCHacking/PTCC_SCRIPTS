import csv
import os
import datetime
import dateutil
from src.constants import Constants
from src.logger import Logger


class DataParser:
    def __init__(self):
        logger = Logger()
        self.logger = logger.get_logger()
        self.employee_list = list()

    def parse_csv(self, csv_path):
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                hired_date_obj = self.convert_date(row['hired_date'])
                employee_dict = {'name': row['name'], 'hired_date': hired_date_obj}
                self.employee_list.append(employee_dict)
        return self.employee_list

    @staticmethod
    def convert_date(date_string):
        date_obj = None
        try:
            date_obj = dateutil.parser.parse(date_string)
            date_obj = date_obj.strftime(Constants.DATE_FORMAT)
            date_obj = datetime.datetime.strptime(date_obj, Constants.DATE_FORMAT)
        except (TypeError, ValueError):
            print(f"You have input an Invalid date {date_string}")
        return date_obj

    def create_csv_output(self, sorted_employee_list):
        output_path = os.path.join(Constants.OUTPUT_DIR, "employee_list.csv")
        fieldnames = ['name', 'hired_date', 'id']
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for employee_dict in sorted_employee_list:
                writer.writerow(employee_dict)