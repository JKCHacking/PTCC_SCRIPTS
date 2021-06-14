import datetime
from src.business_logic.calculator import Calculator


class SummarySpreadsheet:
    def __init__(self, workbook):
        self.ts_workbook = workbook
        self.ws = self.ts_workbook.workbook.create_sheet("Summary")

    def write_headers(self):
        self.ws["A1"] = "PTCC TIMESHEET FOR WEEK ({} to {})".format(
            self.ts_workbook.get_start_date().strftime("%d-%b-%Y"),
            self.ts_workbook.get_end_date().strftime("%d-%b-%Y"))
        self.ws["A2"] = datetime.datetime.now().strftime("%d-%B-%Y")
        self.ws.append([""])
        self.ws.append(["NAME", "PROJECT", "TIME SPENT"])

    def write_body(self, employee, tasks):
        name = "{}, {} {}.".format(employee.get_last_name(),
                                   employee.get_first_name(),
                                   employee.get_middle_name()[0])
        projects = self.__get_projects(tasks)
        projects = "\n".join(sorted(projects))
        time_spent = self.__get_total_hours(tasks)
        self.ws.append([name, projects, time_spent])

    def write_footers(self):
        self.ws.append([""])
        self.ws.append(["APPROVED by (SUPERVISOR)"])
        self.ws.append([""])
        self.ws.append(["_________________________"])
        self.ws.append(["ADAM LEE"])
        self.ws.append([""])
        self.ws.append([""])
        self.ws.append(["NOTED BY:"])
        self.ws.append([""])
        self.ws.append(["_________________________"])
        self.ws.append(["SUSAN BENJAMIN"])

    def __get_projects(self, tasks):
        project_set = set()
        for task in tasks:
            project_set.add(task.get_project_name())
        return project_set

    def __get_total_hours(self, tasks):
        calculator = Calculator()
        total_hours = 0
        for task in tasks:
            total_hours += calculator.calculate_task_hours(task.get_date(), task.get_time_in(), task.get_time_out())
        return total_hours
