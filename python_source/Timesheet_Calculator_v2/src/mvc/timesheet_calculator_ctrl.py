from src.mvc.timesheet_calculator_ui import TimesheetCalculatorUI


class TimesheetCalculatorCtrl:
    def __init__(self):
        self.view = TimesheetCalculatorUI()

    def init_ui(self):
        self.view.create_window()
        self.view.show()
