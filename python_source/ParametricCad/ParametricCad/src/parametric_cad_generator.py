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


def main():
    tkinter.Tk().withdraw()
    template_path = askopenfilename(title="Select the Template DWG file", filetypes=[("DWG Files", ".dwg")])
    config_paths = askopenfilenames(title="Select the CSV config files", filetypes=[("CSV Files", ".csv")])

    print("Template File:\n{}\n".format(os.path.basename(template_path)))
    print("Config Files:\n{}\n".format("\n".join([os.path.basename(c) for c in config_paths])))
    b_cad_app = get_cad_application()

    for config_path in config_paths:
        dwg_file_name = os.path.splitext(os.path.basename(config_path))[0] + ".dwg"
        dwg_output_path = shutil.copyfile(template_path, os.path.join(OUTPUT_PATH, dwg_file_name))
        dwg_doc = b_cad_app.Documents.Open(dwg_output_path)
        model_space = dwg_doc.ModelSpace
        print("Generating {}...".format(dwg_file_name))

        # open csv file
        with open(config_path, "r") as config_csv:
            reader = csv.DictReader(config_csv)
            for row in reader:
                parameter_name = row["Name"]
                parameter_value = row["Value"]
                found = False
                for cad_obj in model_space:
                    if "Dimension" in cad_obj.ObjectName and cad_obj.Layer == "*ADSK_CONSTRAINTS":
                        if cad_obj.TextOverride.split("=")[0] == parameter_name:
                            dwg_doc.SendCommand("-PARAMETERS edit {} {}\n".format(parameter_name, parameter_value))
                            dwg_doc.SendCommand("REGEN\n")
                            found = True
                if not found:
                    print("Parameter {} does not exists.".format(parameter_name))
        dwg_doc.Save()
        dwg_doc.Close()


if __name__ == "__main__":
    main()
