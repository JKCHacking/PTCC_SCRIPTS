class Task:
    def __init__(self, date, time_in, time_out, project_name, task_name):
        self.date = date
        self.time_in = time_in
        self.time_out = time_out
        self.project_name = project_name
        self.task_name = task_name

    def get_date(self):
        return self.date

    def get_time_in(self):
        return self.time_in

    def get_time_out(self):
        return self.time_out

    def get_project_name(self):
        return self.project_name

    def get_task_name(self):
        return self.task_name
