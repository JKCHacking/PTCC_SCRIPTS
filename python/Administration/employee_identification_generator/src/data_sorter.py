from operator import itemgetter
from src.logger import Logger


class DataSorter:
    def __init__(self):
        logger = Logger()
        self.logger = logger.get_logger()

    @staticmethod
    def sort_data(ls, *args):
        sorted_list = sorted(ls, key=itemgetter(*args))
        return sorted_list
