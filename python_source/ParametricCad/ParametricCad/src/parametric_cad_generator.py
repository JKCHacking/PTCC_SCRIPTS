import csv
import os
import shutil
from comtypes import client
from comtypes import COMError


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
    return b_cad


def main():
    template_path = ""
    config_paths = []

    for config_path in config_paths:
        b_cad_app = get_cad_application()
        dwg_file_name = os.path.splitext(os.path.basename(config_path))[0] + ".dwg"
        dwg_output_path = shutil.copyfile(template_path, os.path.join(OUTPUT_PATH, dwg_file_name))
        dwg_doc = b_cad_app.Documents.Open("dwg_file_name")
        modelspace = dwg_doc.ModelSpace

        # open csv file
        with open(config_path, "r") as config_csv:
            reader = csv.DictReader(config_csv)
            for row in reader:
                parameter_name = row["Parameter Name"]
                parameter_value = row["Value"]
                for cad_obj in modelspace:
                    if "Dimension" in cad_obj.ObjectName and cad_obj.DimConstrForm:
                        print(cad_obj.DimConstrExpression)
                        print(cad_obj.DimConstrName)
                        print(cad_obj.DimConstrValue)
        dwg_doc.Save()
        dwg_doc.Close()




if __name__ == "__main__":
    pass
