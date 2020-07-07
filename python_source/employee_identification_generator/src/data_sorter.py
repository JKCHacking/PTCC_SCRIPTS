from operator import itemgetter
from src.logger import Logger


class DataSorter:
    def __init__(self):
        logger = Logger()
        self.logger = logger.get_logger()
        self.sorted_employee_list = list()

    def sort_data(self, employee_list):
        self.sorted_employee_list = sorted(employee_list, key=itemgetter('hired_date', 'name'))
        return self.sorted_employee_list
