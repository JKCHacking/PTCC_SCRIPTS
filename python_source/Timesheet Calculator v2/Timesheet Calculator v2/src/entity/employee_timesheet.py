class EmployeeTimesheet:
    def __init__(self, employee, task_list):
        self.employee = employee
        self.tasks = task_list

    def get_employee(self):
        return self.employee

    def get_tasks(self):
        return self.tasks
