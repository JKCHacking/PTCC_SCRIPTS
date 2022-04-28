import sys
import csv
import os
import shutil
import tkinter
import ctypes
import re
import fractions
from comtypes import client
from comtypes import COMError
from comtypes import automation
from tkinter.filedialog import askopenfilename, askopenfilenames

SRC_PATH = ""
if getattr(sys, "frozen", False):
    SRC_PATH = os.path.dirname(os.path.realpath(sys.executable))
elif __file__:
    SRC_PATH = os.path.dirname(os.path.realpath(__file__))
OUTPUT_PATH = os.path.join(SRC_PATH, "output")
INPUT_PATH = ""
FRACTIONAL = 5
PRECISION = 5
UNITS = {
    1: "\"",
    4: "mm"
}


def except_hook(type, value, traceback, oldhook=sys.excepthook):
    oldhook(type, value, traceback)
    input("Press enter to exit...")


sys.excepthook = except_hook


def get_brics_app():
    b_cad = "BricscadApp.AcadApplication"
    try:
        b_cad_app = client.GetActiveObject(b_cad, dynamic=True)
        b_cad_app.Visible = True
    except COMError:
        b_cad_app = client.CreateObject(b_cad, dynamic=True)
        b_cad_app.Visible = True
    return b_cad_app


def get_acad_app():
    a_cad = "AutoCAD.Application"
    try:
        a_cad_app = client.GetActiveObject(a_cad, dynamic=True)
        a_cad_app.Visible = True
    except COMError:
        a_cad_app = client.CreateObject(a_cad, dynamic=True)
        a_cad_app.Visible = True
    return a_cad_app


def get_cad_app():
    try:
        cad_app = get_brics_app()
    except COMError:
        cad_app = get_acad_app()
    return cad_app


def get_entities(dwg_doc, object_names):
    entities = [obj for obj in dwg_doc.ModelSpace if obj.ObjectName in object_names]
    return entities


def get_parts(assm_temp_path):
    print("Getting parts...")
    parts = []
    doc = get_cad_app().Documents.Open(assm_temp_path)
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
    doc.Close(False)
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


def create_assembly(template, assembly_name, assembly_directory):
    try:
        os.makedirs(assembly_directory)
    except FileExistsError:
        print("{} already exists.".format(assembly_directory))
    directory = os.path.join(OUTPUT_PATH, assembly_name)
    path = shutil.copyfile(template, os.path.join(directory, assembly_name + ".dwg"))
    cad_app = get_cad_app()
    return cad_app.Documents.Open(path)


def update_assembly_params(assembly_doc, params):
    for param_name, value in params.items():
        assembly_doc.SendCommand("-PARAMETERS\nedit\n{}\n{}\n".format(param_name, value))
        assembly_doc.SendCommand("REGEN\n")


def update_part_params(part_doc, assembly_params):
    for obj in part_doc.ModelSpace:
        if "Dimension" in obj.ObjectName:
            type_out = automation.VARIANT([0, 0])
            data_out = automation.VARIANT(["", ""])
            obj.GetXData("PARAMETRIC", ctypes.byref(type_out), ctypes.byref(data_out))
            param_name = data_out[0][1]
            if param_name in assembly_params:
                val = assembly_params[param_name]
                # detects fractional as format of numbers in the document.
                if part_doc.GetVariable("DIMLUNIT") == FRACTIONAL:
                    val = part_doc.Utility.RealToString(val, FRACTIONAL, PRECISION)
                else:
                    val = str(val)
                obj.TextOverride = val + UNITS[part_doc.GetVariable("INSUNITS")]
                obj.Update()


def get_all_assm_params(assembly_doc):
    params = {}
    assembly_doc.SetVariable("LOGFILEMODE", 1)
    assembly_doc.SendCommand("-Parameters\n\n")
    log_path = assembly_doc.GetVariable("LOGFILENAME")
    assembly_doc.SetVariable("LOGFILEMODE", 0)
    with open(log_path, "r") as log_file:
        for line in log_file.readlines():
            res_param = re.search(r'(?<=Parameter:).*(?=Expression:)', line)
            res_val = re.search(r'(?<=Value:).*', line)
            if res_param and res_val:
                parameter_name = res_param.group(0).strip()
                if parameter_name:
                    value = res_val.group(0).strip()
                    value = round(float(value), PRECISION)
                    params.update({parameter_name: value})
    os.remove(log_path)
    return params


def get_all_part_params(part_doc):
    params = {}
    for obj in part_doc.ModelSpace:
        if "Dimension" in obj.ObjectName:
            type_out = automation.VARIANT([0, 0])
            data_out = automation.VARIANT(["", ""])
            obj.GetXData("PARAMETRIC", ctypes.byref(type_out), ctypes.byref(data_out))
            param = data_out[0][1]
            if param:
                val = obj.TextOverride if obj.TextOverride else round(obj.Measurement, PRECISION)
                if isinstance(val, str):
                    # remove the unit
                    val = val.replace(UNITS[part_doc.GetVariable("INSUNITS")], "")
                    if "/" in val:
                        if " " in val:
                            whole, frac = val.split(" ")
                        else:
                            frac = val
                            whole = 0
                        dec = round(float(fractions.Fraction(frac)), PRECISION)
                        try:
                            whole = int(whole)
                        except ValueError:
                            # remove the color format "\\C7;" = white
                            whole = whole.split(";")[1]
                            whole = int(whole)
                        val = whole + dec
                    else:
                        val = int(val)
                params.update({param: val})
    return params


def is_part_exists(assembly_name, part, parts_params):
    cad_app = get_cad_app()
    exists = False
    duplicate_file = ""
    for root, dirs, files in os.walk(OUTPUT_PATH):
        for file in files:
            part_name, part_num_letter = part.split("-")
            part_number, part_letter = get_suff_num_letter(part_num_letter)
            pattern = "{}-\\d{{3}}{}".format(part_name, part_letter)
            if not file.startswith(assembly_name) and re.match(pattern, os.path.splitext(file)[0]) and \
                    file.endswith(".dwg"):
                part_file = os.path.join(root, file)
                part_doc = cad_app.Documents.Open(part_file)
                part_params = get_all_part_params(part_doc)
                checks = [True if param_name in parts_params and value == parts_params[param_name]
                          else False for param_name, value in part_params.items()]
                # this means that all part parameters are equal in assembly params.
                # a part with those parameters already exists.
                if all(checks):
                    exists = True
                    duplicate_file = os.path.join(root, file)
                part_doc.Close(False)
    return exists, duplicate_file


def update_assembly_part_table(assembly_doc, old_part, new_part):
    part_table = find_part_table(assembly_doc)
    part_col = find_col_idx(part_table, "PART NUMBER")
    part_row = find_row_idx(part_table, part_col, old_part)
    if part_row != -1:
        # update the cell
        part_table.SetCellValue(part_row, part_col, os.path.splitext(new_part)[0])
    else:
        print("Cannot find part {} in the part table".format(old_part))


def delete_parametric_dims(assm_doc, assembly_params):
    for param in assembly_params.keys():
        assm_doc.SendCommand("-PARAMETERS\nDelete\n{}\n".format(param))

    for obj in assm_doc.ModelSpace:
        assm_doc.SendCommand('DELCONSTRAINT\n(handent "{}")\n\n'.format(obj.Handle))


def get_suff_num_letter(suffix_pname):
    suff_num = 0
    suff_letter = ""

    res = re.split('(\\d+)', suffix_pname)
    for c in res:
        if c.isnumeric():
            suff_num = int(c)
        elif c.isalpha():
            suff_letter = c
    return suff_num, suff_letter


def get_max_part_num(part_name, part_letter):
    part_num_list = []
    max_part_num = 0
    for root, dirs, files in os.walk(OUTPUT_PATH):
        for file in files:
            if file.endswith(".dwg") and "-" in file:
                pattern = "{}-\\d{{3}}{}".format(part_name, part_letter)
                curr_part = os.path.splitext(file)[0]
                curr_part_name, curr_part_num_letter = curr_part.split("-")
                curr_part_num, curr_part_letter = get_suff_num_letter(curr_part_num_letter)
                if re.match(pattern, curr_part):
                    part_num_list.append(curr_part_num)
    if part_num_list:
        max_part_num = max(part_num_list)
    return max_part_num


def main():
    global INPUT_PATH
    cad_app = get_cad_app()
    tkinter.Tk().withdraw()
    assm_temp_path = askopenfilename(title="Select the Template Assembly DWG file", filetypes=[("DWG Files", ".dwg")])
    config_path = askopenfilename(title="Select the CSV config file", filetypes=[("CSV Files", ".csv")])
    parts = get_parts(assm_temp_path)
    INPUT_PATH = os.path.dirname(assm_temp_path)
    print("Assembly File:\n{}\n".format(os.path.basename(assm_temp_path)))
    print("Config File:\n{}\n".format(os.path.basename(config_path)))
    print("Parts:\n{}\n".format("\n".join(parts)))

    if parts:
        with open(config_path, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames
            assembly_col = headers[0]
            parameter_names = headers[1:]
            # note that each row is 1 assembly dwg file.
            # and each row creates a subdirectory for sub-assembly and parts of the assembly.
            for row in reader:
                assembly_name = row[assembly_col]
                assembly_directory = os.path.join(OUTPUT_PATH, assembly_name)
                print("Generating Assembly:\n{}".format(assembly_name))
                assembly_doc = create_assembly(assm_temp_path, assembly_name, assembly_directory)
                # set to modelspace
                assembly_doc.SetVariable("TILEMODE", 1)
                parameters = {param_name: row[param_name] for param_name in parameter_names}
                update_assembly_params(assembly_doc, parameters)
                assembly_params = get_all_assm_params(assembly_doc)
                print("\nGenerating Part:")
                for part in parts:
                    print(part)
                    part_file = os.path.join(INPUT_PATH, "{}.dwg".format(part))
                    temp_part_file = os.path.join(INPUT_PATH, "{}_temp.dwg".format(part))
                    if os.path.exists(part_file):
                        # create a temporary file first
                        part_doc = cad_app.Documents.Open(part_file)
                        update_part_params(part_doc, assembly_params)
                        part_params = get_all_part_params(part_doc)
                        part_doc.SaveAs(temp_part_file)
                        part_doc.Close(False)
                        exists, duplicate_file = is_part_exists(assembly_name, part, part_params)
                        src = temp_part_file
                        if exists:
                            src = duplicate_file
                            new_part = os.path.basename(src)
                        else:
                            part_name, part_num_letter = part.split("-")
                            part_number, part_letter = get_suff_num_letter(part_num_letter)
                            new_part_num = get_max_part_num(part_name, part_letter)
                            # this means that it does not have any other relatives.
                            if new_part_num == 0:
                                new_part_num = part_number
                            else:
                                new_part_num = new_part_num + 1
                            new_part = "{}-{:03d}{}.dwg".format(part_name, new_part_num, part_letter)
                        dst = os.path.join(assembly_directory, new_part)
                        try:
                            shutil.copyfile(src, dst)
                        except shutil.SameFileError:
                            pass
                        update_assembly_part_table(assembly_doc, part, new_part)
                    else:
                        print("Cannot find part {} in {}".format(part, INPUT_PATH))
                    if os.path.exists(temp_part_file):
                        os.remove(temp_part_file)
                delete_parametric_dims(assembly_doc, assembly_params)
                assembly_doc.Close()
                print("")
    else:
        print("Cannot find parts.")


if __name__ == "__main__":
    main()
