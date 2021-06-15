import sys
from PyQt5 import QtWidgets
from src.mvc.timesheet_calculator_ctrl import TimesheetCalculatorCtrl


def main():
    app = QtWidgets.QApplication(sys.argv)
    ts_controller = TimesheetCalculatorCtrl()
    ts_controller.init_ui()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
