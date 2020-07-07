from src.logger import Logger
from src.constants import Constants


class IdCreator:
    def __init__(self):
        logger = Logger()
        self.logger = logger.get_logger()

    def create_id(self, sorted_employee_list):
        index = 0
        date_tracker = sorted_employee_list[0]["hired_date"]
        for employee in sorted_employee_list:
            if date_tracker != employee["hired_date"]:
                index = 0
                date_tracker = employee["hired_date"]
            day = date_tracker.day
            month = date_tracker.month
            year = date_tracker.year
            emp_id = f"{day:02d}{month:02d}{year:02d}{index:02d}"
            employee.update({"name": employee["name"], "hired_date": date_tracker.strftime(Constants.DATE_FORMAT),
                             "id": emp_id})
            index += 1
        return sorted_employee_list
