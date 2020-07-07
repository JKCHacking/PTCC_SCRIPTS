from src.logger import Logger


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
            day = str(date_tracker.day).zfill(2)
            month = str(date_tracker.month).zfill(2)
            year = str(date_tracker.year).zfill(2)
            emp_id = f"{day}{month}{year}{index}"
            employee.update({"name": employee["name"], "hired_date": employee["hired_date"], "id": emp_id})
            index += 1
        return sorted_employee_list
