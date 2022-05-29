class Employee:
    def __init__(self, id_number, first_name, middle_name, last_name):
        self.id_number = id_number
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name

    def get_id_num(self):
        return self.id_number

    def get_first_name(self):
        return self.first_name

    def get_middle_name(self):
        return self.middle_name

    def get_last_name(self):
        return self.last_name
