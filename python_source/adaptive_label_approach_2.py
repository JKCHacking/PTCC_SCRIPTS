#!usr/bin/env python

import array
import comtypes
import comtypes.client
from comtypes import COMError

# Constants
APP_NAME = "ADAPTIVE_LABEL_APP"
SELECT_ALL = 5
SELECTION_SET_NAME = "PROJECTXX_SS"


class AdaptiveLabelApproach2:

    def __init__(self):
        try:
            self.bcad = comtypes.client.GetActiveObject("BricscadApp.AcadApplication", dynamic=True)
        except (OSError, COMError):
            print("BricsCad isn't running!")
            self.bcad = comtypes.client.CreateObject("BricscadApp.AcadApplication", dynamic=True)

        self.doc = self.bcad.ActiveDocument
        self.model_space = self.doc.ModelSpace
        self.paper_space = self.doc.PaperSpace
        self.util = self.doc.Utility

    def __get_selection_set(self, filter_types, filter_data):
        try:
            selection_sets = self.doc.SelectionSets.Add(SELECTION_SET_NAME)
        except:  # TODO: Create custom error class for pylint warnings
            selection_sets = self.doc.SelectionSets.Item(SELECTION_SET_NAME)

        pt1 = array.array('d', [0.0, 0.0, 0.0])
        pt2 = array.array('d', [0.0, 0.0, 0.0])

        selection_sets.Select(SELECT_ALL, pt1, pt2, filter_types, filter_data)

        return selection_sets

    def __modify_table_label(self, parameter_name, new_length):
        filter_types = array.array('h', [0])
        filter_data = ["ACAD_TABLE"]

        selection_set = self.__get_selection_set(filter_types, filter_data)
        table_object = selection_set.Item(0)  # since there is only 1 expected table.

        total_rows = table_object.Rows
        total_columns = table_object.Columns

        code_column_index = self.__get_column_index(total_columns, "Code", table_object)
        length_column_index = self.__get_column_index(total_columns, "Length", table_object)

        found_flag = False

        for irow in range(0, total_rows):
            cell_content = table_object.GetCellValue(irow, code_column_index)
            if str(cell_content) == parameter_name:
                table_object.SetCellValue(irow, length_column_index, new_length)
                found_flag = True

        if not found_flag:
            print("Parameter Name {} not found!".format(parameter_name))

        selection_set.Delete

    @staticmethod
    def __get_column_index(col, header_name, table_object):
        column_index = 0
        for icol in range(0, col):
            cell_content = table_object.GetCellValue(0, icol)
            if str(cell_content) == header_name:
                column_index = icol

        return column_index

    def __modify_parameter_values(self, parameter_name, new_length):
        command_str = "-PARAMETERS edit {} {}\n".format(parameter_name, new_length)
        self.doc.SendCommand(command_str)

    def start_automate(self, parameter_name, new_length):
        self.__modify_parameter_values(parameter_name, new_length)
        self.__modify_table_label(parameter_name, new_length)

    def add_extended_data(self, object_entity, parameter_name):
        x_data_type = array.array('i', [1001, 1000])
        x_data = [APP_NAME, parameter_name]
        object_entity.SetXData(x_data_type, x_data)


if __name__ == "__main__":
    parameter_name = input("Select a parametric constraint: ")
    new_length = input("Enter new length: ")

    adaptive_label_object = AdaptiveLabelApproach2()
    adaptive_label_object.start_automate(parameter_name, new_length)

