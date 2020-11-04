class Watcher:
    def __init__(self, value):
        self.variable = value  # ''
        self.changed = False
        self.numeric = False

    def set_value(self, new_value):
        temp_numeric = self.numeric
        if new_value.isnumeric():
            self.numeric = True
        else:
            self.numeric = False

        if (temp_numeric and not self.numeric) or (not temp_numeric and self.numeric) or \
                (not temp_numeric and not self.numeric):
            if self.variable != new_value:
                self.variable = new_value
                self.changed = True
        else:
            self.changed = False

    def has_changed(self):
        return self.changed
