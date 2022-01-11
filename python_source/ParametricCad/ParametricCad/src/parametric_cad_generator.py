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

SRC_PATH = os.path.dirname(os.path.realpath(__file__))
APP_PATH = os.path.dirname(SRC_PATH)
PROJ_PATH = os.path.dirname(APP_PATH)
OUTPUT_PATH = os.path.join(PROJ_PATH, "output")

FRACTIONAL = 5
UNITS = {
    1: "\"",
    4: "mm"
}


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
    bcad = get_cad_application()
    return bcad.Documents.Open(path)


def update_assembly_params(assembly_doc, params):
    for param_name, value in params.items():
        assembly_doc.SendCommand("-PARAMETERS edit {} {}\n".format(param_name, value))
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
                    val = dec_to_frac(val)
                else:
                    val = str(val)
                obj.TextOverride = val + UNITS[part_doc.GetVariable("INSUNITS")]
                obj.Update()


def dec_to_frac(num):
    dec = round(num % 1, 3)
    whole = int(num)
    frac = str(whole)
    if dec != 0:
        frac = "{} {}".format(whole, fractions.Fraction(dec))
    return frac


def get_all_assm_params(assembly_doc):
    params = {}
    for obj in assembly_doc.ModelSpace:
        if obj.Layer == "*ADSK_CONSTRAINTS":
            param_name, value = obj.TextOverride.split("=")
            if is_number(value):
                value = round(float(value), 3)
            params.update({param_name: value})
    return params


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def extract_variables(equation_string):
    tokens = re.split('\\+|\\+ |\\*|\\* |-|- |/|/ |\\(|\\)|\\s', equation_string)
    variables = [token for token in tokens if token and not is_number(token)]
    return variables


def equation_resolver(equation_string, params):
    variables = extract_variables(equation_string)
    for var in variables:
        try:
            val = params[var]
            equation_string = equation_string.replace(var, str(val))
        except KeyError:
            print("Parameter {} does not exists".format(var))
    res = eval(equation_string)
    return res


def simplify_parameters(assembly_params):
    # resolve all equation to numbers
    for name, val in assembly_params.items():
        if not is_number(val):
            new_val = equation_resolver(val, assembly_params)
            assembly_params.update({name: new_val})


def get_all_part_params(part_doc):
    params = {}
    for obj in part_doc.ModelSpace:
        if "Dimension" in obj.ObjectName:
            type_out = automation.VARIANT([0, 0])
            data_out = automation.VARIANT(["", ""])
            obj.GetXData("PARAMETRIC", ctypes.byref(type_out), ctypes.byref(data_out))
            param = data_out[0][1]
            if param:
                val = obj.TextOverride if obj.TextOverride else round(obj.Measurement, 3)
                if isinstance(val, str):
                    # remove the unit
                    val = val.replace(UNITS[part_doc.GetVariable("INSUNITS")], "")
                    if "/" in val:
                        whole, frac = val.split(" ")
                        dec = round(float(fractions.Fraction(frac)), 3)
                        val = int(whole) + dec
                    else:
                        val = int(val)
                params.update({param: val})
    return params


def find_duplicate_part(part_name, assembly_params):
    b_app = get_cad_application()
    dup_part = None
    count = 0
    for root, dirs, files in os.walk(OUTPUT_PATH):
        for file in files:
            if file.startswith(part_name) and file.endswith(".dwg"):
                part_file = os.path.join(root, file)
                part_doc = b_app.Documents.Open(part_file)
                part_params = get_all_part_params(part_doc)
                checks = [True if param_name in assembly_params and value == assembly_params[param_name]
                          else False for param_name, value in part_params.items()]
                # this means that all part parameters are equal in assembly params.
                # a part with those parameters already exists.
                if all(checks):
                    dup_part = part_file
                part_doc.Close(False)
                count += 1
    return dup_part, count


def update_assembly_part_table(assembly_doc, part_name):
    part_table = find_part_table(assembly_doc)
    default_part_name = part_name.split("-")[0] + "-000"
    part_col = find_col_idx(part_table, "PART NUMBER")
    part_row = find_row_idx(part_table, part_col, default_part_name)
    if part_row != -1:
        # update the cell
        part_table.SetCellValue(part_row, part_col, os.path.splitext(part_name)[0])
    else:
        print("Cannot find part {} in the part table".format(default_part_name))


def delete_parametric_dims(assm_doc):
    lines = []
    for obj in assm_doc.ModelSpace:
        if obj.ObjectName == "AcDbLine" or obj.ObjectName == "AcDbPolyline":
            lines.append(obj)
    for line in lines:
        assm_doc.SendCommand('DELCONSTRAINT (handent "{}")\n\n'.format(line.Handle))


def main():
    b_app = get_cad_application()
    tkinter.Tk().withdraw()
    assm_temp_path = askopenfilename(title="Select the Template Assembly DWG file", filetypes=[("DWG Files", ".dwg")])
    config_path = askopenfilename(title="Select the CSV config file", filetypes=[("CSV Files", ".csv")])
    part_names = get_part_names(assm_temp_path)
    print("Assembly File:\n{}\n".format(os.path.basename(assm_temp_path)))
    print("Config File:\n{}\n".format(os.path.basename(config_path)))
    print("Parts:\n{}\n".format("\n".join(part_names)))

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
                assembly_directory = os.path.join(OUTPUT_PATH, assembly_name)
                print("Generating Assembly:\n{}".format(assembly_name))
                assembly_doc = create_assembly(assm_temp_path, assembly_name, assembly_directory)
                parameters = {param_name: row[param_name] for param_name in parameter_names}
                update_assembly_params(assembly_doc, parameters)
                assembly_params = get_all_assm_params(assembly_doc)
                simplify_parameters(assembly_params)
                print("\nGenerating Part:")
                for part_name in part_names:
                    dup_part, count = find_duplicate_part(part_name.split("-")[0], assembly_params)
                    if dup_part:
                        new_part_file_name = os.path.basename(dup_part)
                        try:
                            shutil.copyfile(dup_part, os.path.join(assembly_directory, new_part_file_name))
                            print(os.path.splitext(new_part_file_name)[0])
                        except shutil.SameFileError:
                            pass
                    else:
                        part_template = os.path.join(os.path.dirname(assm_temp_path), part_name + ".dwg")
                        new_part_file_name = "{}-{:03d}.dwg".format(part_name.split("-")[0], count + 1)
                        try:
                            new_part = shutil.copyfile(part_template, os.path.join(assembly_directory,
                                                                                   new_part_file_name))
                            print(os.path.splitext(new_part_file_name)[0])
                        except FileNotFoundError:
                            print("Cannot find part {} in {}".format(part_name.split("-")[0],
                                                                     os.path.dirname(assm_temp_path)))
                        # update the new part
                        part_doc = b_app.Documents.Open(new_part)
                        update_part_params(part_doc, assembly_params)
                        part_doc.Close()
                    update_assembly_part_table(assembly_doc, new_part_file_name)
                delete_parametric_dims(assembly_doc)
                assembly_doc.Close()
                print("")
    else:
        print("Cannot find parts.")


if __name__ == "__main__":
    main()
