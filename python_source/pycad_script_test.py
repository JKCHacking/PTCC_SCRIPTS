#!usr/bin/env python

import comtypes
import comtypes.client
from comtypes import COMError
# from pyautocad import
import array


class PyCadAutomator:
    def __init__(self):
        try:
            self.acad = comtypes.client.GetActiveObject("BricscadApp.AcadApplication", dynamic=True)
        except (OSError, COMError):
            print("BricsCad isn't running!")
            self.acad = comtypes.client.CreateObject("BricscadApp.AcadApplication", dynamic=True)

        self.doc = self.acad.ActiveDocument
        self.model_space = self.doc.ModelSpace
        self.paper_space = self.doc.PaperSpace
        self.util = self.doc.Utility

    def print_document_info(self):
        print("Application: {}".format(self.acad))
        print("Document: {}".format(self.doc))
        print("Model Space: {}".format(self.model_space))
        print("Paper Space: {}".format(self.paper_space))
        print("Utilities: {}".format(self.util))

    def create_line(self):
        pt1 = array.array('d', [0.0, 0.0, 0.0])
        pt2 = array.array('d', [210.0, 0.0, 0.0])
        pt3 = array.array('d', [210.0, 297.0, 0.0])
        pt4 = array.array('d', [0.0, 297.0, 0.0])

        line1 = self.model_space.AddLine(pt1, pt2)
        line2 = self.model_space.AddLine(pt2, pt3)
        line3 = self.model_space.AddLine(pt3, pt4)
        line4 = self.model_space.AddLine(pt4, pt1)

    def get_selection_set(self):
        try:
            selection_sets = self.doc.SelectionSets.Add("AllObjects")
            print("HELLO")
        except:
            selection_sets = self.doc.SelectionSets.Item("AllObjects")
            print(selection_sets)

        SELECT_ALL = 5
        filter_type = array.array('h', [0])
        filter_data = ['Line']

        pt1 = array.array('d', [0.0, 0.0, 0.0])
        pt2 = array.array('d', [0.0, 0.0, 0.0])

        selection_sets.Select(SELECT_ALL, pt1, pt2, filter_type, filter_data)
        total_objects = selection_sets.Count
        all_object = [selection_sets.Item(i) for i in range(0, total_objects)]

        for i in range(0, total_objects):
            print("Object name in index {}: {}".format(i, all_object[i].ObjectName))
            print("Handle in index {}: {}".format(i, all_object[i].Handle))

        # add extended data on the first object in selection set
        x_data_type = array.array('i', [1001, 1000])
        x_data = ['APP_NAME', 'First Object Data Message']

        all_object[0].SetXData(x_data_type, x_data)

        try:
            selection_sets_result = self.doc.SelectionSets.Add("AllObjects2")
        except:
            selection_sets_result = self.doc.SelectionSets.Item("AllObjects2")

        x_filter_type_result = array.array('h', [0, 1001, 1000])
        x_filter_data_result = ['Line', 'APP_NAME', 'First Object Data Message']
        pt1_res = array.array('d', [0.0, 0.0, 0.0])
        pt2_res = array.array('d', [0.0, 0.0, 0.0])

        selection_sets_result.Select(SELECT_ALL, pt1_res, pt2_res, x_filter_type_result, x_filter_data_result)
        total_objects_result = selection_sets_result.Count
        all_object_result = [selection_sets_result.Item(i) for i in range(0, total_objects_result)]

        print("--------------------------------------------------------------------------------------")
        for i in range(0, total_objects_result):
            print("Object name Result in index {}: {}".format(i, all_object_result[i].ObjectName))
            print("Handle Result in index {}: {}".format(i, all_object_result[i].Handle))

if __name__ == "__main__":
    py_cad_automator = PyCadAutomator()
    # py_cad_automator.create_line()
    py_cad_automator.get_selection_set()
    # py_cad_automator.print_document_info()
