import os
from src.data_parser import DataParser
from src.data_sorter import DataSorter
from src.id_creator import IdCreator
from src.logger import Logger
from src.constants import Constants

logger = Logger()
main_logger = logger.get_logger()

if __name__ == "__main__":
    input_file = os.path.join(Constants.INPUT_DIR, "input.csv")
    dp = DataParser()
    ds = DataSorter()
    ic = IdCreator()

    employee_list = dp.parse_csv(input_file)
    sorted_employee_list = ds.sort_data(employee_list)
    sorted_employee_list = ic.create_id(sorted_employee_list)
    dp.create_csv_output(sorted_employee_list)
