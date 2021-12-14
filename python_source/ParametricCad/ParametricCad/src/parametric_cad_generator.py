import csv
import os
import shutil
import tkinter
from comtypes import client
from comtypes import COMError
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


def main():
    tkinter.Tk().withdraw()
    template_path = askopenfilename(title="Select the Template DWG file", filetypes=[("DWG Files", ".dwg")])
    config_path = askopenfilename(title="Select the CSV config file", filetypes=[("CSV Files", ".csv")])

    print("Template File:\n{}\n".format(os.path.basename(template_path)))
    print("Config File:\n{}\n".format(os.path.basename(config_path)))
    b_cad_app = get_cad_application()

    with open(config_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        file_col_name = headers[0]
        parameter_names = headers[1:]
        for row in reader:
            dwg_file_name = os.path.splitext(row[file_col_name])[0] + ".dwg"
            dwg_output_path = shutil.copyfile(template_path, os.path.join(OUTPUT_PATH, dwg_file_name))
            dwg_doc = b_cad_app.Documents.Open(dwg_output_path)
            print("Generating {}...".format(dwg_file_name))
            # loop regardless if the parameter exists or not.
            for parameter_name in parameter_names:
                value = row[parameter_name]
                if value:
                    dwg_doc.SendCommand("-PARAMETERS edit {} {}\n".format(parameter_name, value))
                    dwg_doc.SendCommand("REGEN\n")
            # delete all constraints
            print("Deleting Parameters and Constraints...")
            objs = get_entities(dwg_doc, ["AcDbLine", "AcDbPolyline"])
            for cad_obj in objs:
                dwg_doc.SendCommand('DELCONSTRAINT (handent "{}")\n\n'.format(cad_obj.Handle))
            dwg_doc.Save()
            dwg_doc.Close()


if __name__ == "__main__":
    main()
