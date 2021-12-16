import csv
import os
import shutil
import tkinter
import ctypes
from comtypes import client
from comtypes import COMError
from comtypes import automation
from tkinter.filedialog import askopenfilename, askopenfilenames


SRC_PATH = os.path.dirname(os.path.realpath(__file__))
APP_PATH = os.path.dirname(SRC_PATH)
PROJ_PATH = os.path.dirname(APP_PATH)
OUTPUT_PATH = os.path.join(PROJ_PATH, "output")


def get_cad_application():
    b_cad = "BricscadApp.AcadApplication"
    try:
        b_cad_app = client.GetActiveObject(b_cad, dynamic=True)
        b_cad_app.Visible = True
    except COMError:
        b_cad_app = client.CreateObject(b_cad, dynamic=True)
        b_cad_app.Visible = True
    return b_cad_app


def get_entities(dwg_doc, object_names):
    entities = [obj for obj in dwg_doc.ModelSpace if obj.ObjectName in object_names]
    return entities


def get_part_names(assm_temp_path):
    print("Getting parts...")
    parts = []
    doc = get_cad_application().Documents.Open(assm_temp_path)
    part_table = find_part_table(doc)
    if part_table:
        if part_table.TitleSuppressed:
            row = 0
        else:
            row = 1
        for icol in range(part_table.Columns):
            if part_table.GetCellValue(row, icol) == "PART NUMBER":
                for irow in range(row + 1, part_table.Rows):
                    val = part_table.GetCellValue(irow, icol)
                    if val:
                        parts.append(val)
    else:
        print("Cannot find part table.")
    doc.Close()
    return parts


def find_col_idx(table, col_name):
    col_idx = -1
    if table.TitleSuppressed:
        row = 0
    else:
        row = 1
    for icol in range(table.Columns):
        if table.GetCellValue(row, icol) == col_name:
            col_idx = icol
            break
    return col_idx


def find_row_idx(table, col_idx, row_name):
    row_idx = -1
    if table.TitleSuppressed:
        row = 1
    else:
        row = 2
    for irow in range(row, table.Rows):
        if table.GetCellValue(irow, col_idx) == row_name:
            row_idx = irow
            break
    return row_idx


def find_part_table(doc):
    part_table = None
    tables = get_entities(doc, ["AcDbTable"])
    for table in tables:
        col_idx = find_col_idx(table, "PART NUMBER")
        if col_idx != -1:
            part_table = table
            break
    return part_table


def main():
    tkinter.Tk().withdraw()
    assm_temp_path = askopenfilename(title="Select the Template Assembly DWG file", filetypes=[("DWG Files", ".dwg")])
    config_path = askopenfilename(title="Select the CSV config file", filetypes=[("CSV Files", ".csv")])
    part_names = get_part_names(assm_temp_path)
    print("Assembly File:\n{}\n".format(os.path.basename(assm_temp_path)))
    print("Config File:\n{}\n".format(os.path.basename(config_path)))
    print("SubComponents:\n{}\n".format("\n".join(part_names)))

    if part_names:
        with open(config_path, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames
            part_name_col = headers[0]
            parameter_names = headers[1:]
            # note that each row is 1 assembly dwg file.
            # and each row creates a subdirectory for assembly and parts of the assembly.
            for row in reader:
                assembly_name = row[part_name_col]
                print("Generating Assembly: {}".format(assembly_name))
                parameters = {param_name: row[param_name] for param_name in parameter_names}
                assembly_directory = os.path.join(OUTPUT_PATH, assembly_name)
                try:
                    os.makedirs(assembly_directory)
                except FileExistsError:
                    print("{} already exists.".format(assembly_directory))
                assembly = Assembly(assembly_name)
                assembly.copy_to_directory(assm_temp_path, assembly_directory)
                assembly.open()
                for part_name in part_names:
                    print("Generating Part: {}".format(part_name))
                    part_temp_path = os.path.join(os.path.dirname(assm_temp_path), part_name + ".dwg")
                    if os.path.exists(part_temp_path):
                        part = Part(part_name)
                        part.copy_to_directory(part_temp_path, assembly_directory)
                        assembly.add_parts(part)
                    else:
                        print("Part Template does not exists {}".format(part_temp_path))
                # this will also implicitly update the parts parameters.
                print("Updating parameters...")
                assembly.update_parameters(parameters)
                assembly.delete_constraints()
                assembly.save_and_close()
                print("\n")
    else:
        print("Cannot find parts.")


class Assembly:
    def __init__(self, assembly_name):
        self.assembly_name = assembly_name
        self.parts = []
        self.doc = None
        self.path = ""

    def add_parts(self, part):
        self.parts.append(part)

    def update_parameters(self, parameters):
        for k, v in parameters.items():
            self.__edit_parameters(k, v)
        # extract parameters for parts
        # use the part table in the assembly document
        part_table = find_part_table(self.doc)
        if part_table:
            # get the col index for part number, length, width, height
            part_col_idx = find_col_idx(part_table, "PART NUMBER")
            length_col_idx = find_col_idx(part_table, "LENGTH")
            width_col_idx = find_col_idx(part_table, "WIDTH")
            height_col_idx = find_col_idx(part_table, "HEIGHT")
            for part in self.parts:
                part.open()
                row_idx = find_row_idx(part_table, part_col_idx, part.part_name)
                # get the actual values of the parameter in the table.
                length = part_table.GetCellValue(row_idx, length_col_idx)
                width = part_table.GetCellValue(row_idx, width_col_idx)
                height = part_table.GetCellValue(row_idx, height_col_idx)

                length = length if length else 0
                width = width if width else 0
                height = height if height else 0

                parameters = {"LENGTH": length, "WIDTH": width, "HEIGHT": height}
                part.update_parameters(parameters)
                part.save_and_close()

    def delete_constraints(self):
        objs = get_entities(self.doc, ["AcDbLine", "AcDbPolyline"])
        for cad_obj in objs:
            self.doc.SendCommand('DELCONSTRAINT (handent "{}")\n\n'.format(cad_obj.Handle))

    def __edit_parameters(self, param_name, value):
        self.doc.SendCommand("-PARAMETERS edit {} {}\n".format(param_name, value))
        self.doc.SendCommand("REGEN\n")

    def copy_to_directory(self, assm_temp, directory):
        self.path = shutil.copyfile(assm_temp, os.path.join(directory, self.assembly_name + ".dwg"))

    def open(self):
        self.doc = get_cad_application().Documents.Open(self.path)

    def save_and_close(self):
        self.doc.Save()
        self.doc.Close()


class Part:
    def __init__(self, part_name):
        self.part_name = part_name
        self.doc = None
        self.path = ""

    def update_parameters(self, parameters):
        for k, v in parameters.items():
            found = False
            for obj in self.doc.ModelSpace:
                if "Dimension" in obj.ObjectName:
                    type_out = automation.VARIANT([0, 0])
                    data_out = automation.VARIANT(["", ""])
                    obj.GetXData("PARAMETRIC", ctypes.byref(type_out), ctypes.byref(data_out))
                    param = data_out[0][1]
                    if k == param:
                        obj.TextOverride = v
                        obj.Update()
                        found = True
            if not found:
                print("Cannot find {} parameter".format(k))

    def copy_to_directory(self, part_temp, directory):
        self.path = shutil.copyfile(part_temp, os.path.join(directory, self.part_name + ".dwg"))

    def open(self):
        self.doc = get_cad_application().Documents.Open(self.path)

    def save_and_close(self):
        self.doc.Save()
        self.doc.Close()


if __name__ == "__main__":
    main()
