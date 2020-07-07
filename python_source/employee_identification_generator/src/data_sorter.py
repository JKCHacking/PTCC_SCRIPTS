from operator import itemgetter
from src.logger import Logger


class DataSorter:
    def __init__(self):
        logger = Logger()
        self.logger = logger.get_logger()
        self.sorted_list = list()

    def sort_data_by_hired_date_name(self, ls):
        self.sorted_list = sorted(ls, key=itemgetter('hired_date', 'name'))
        return self.sorted_list

    def sort_data_by_name(self, ls):
        self.sorted_list = sorted(ls, key=itemgetter('name'))
        return self.sorted_list