import csv
import os
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
                self.employee_list.append(row)
        return self.employee_list

    def create_csv_output(self, sorted_employee_list):
        output_path = os.path.join(Constants.OUTPUT_DIR, "employee_list.csv")
        fieldnames = ['name', 'hired_date', 'id']
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for employee_dict in sorted_employee_list:
                writer.writerow(employee_dict)