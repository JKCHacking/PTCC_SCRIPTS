class Watcher:
    def __init__(self, value):
        self.variable = value  # ''
        self.changed = False

    def set_value(self, new_value):
        # if the name starts with a number it will only check once it changed.
        # if the name starts with a letter it will always check if it changed.
        # ex: "a" -> "1" = changed
        #     "1" -> "2" = not changed
        #     "2" -> "a" = changed
        #     "a" -> "b" = changed
        old_value = self.variable
        self.changed = False
        if (not old_value.isnumeric() and new_value.isnumeric()) or \
                (old_value.isnumeric() and not new_value.isnumeric()) or \
                (not old_value.isnumeric() and not new_value.isnumeric()):
            if self.variable != new_value:
                self.variable = new_value
                self.changed = True

    def has_changed(self):
        return self.changed
