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
            emp_id = f"{date_tracker.date}{date_tracker.month}{date_tracker.year}{index}"
            employee.update({"name": employee["name"], "hired_date": employee["hired_date"], "id": emp_id})
            index += 1
        return sorted_employee_list
