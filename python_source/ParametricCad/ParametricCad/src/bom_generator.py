import xlwt
import xlrd
import tkinter
import os
from xlutils.copy import copy
from comtypes import client, COMError
from tkinter.filedialog import askopenfilename

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


def find_part_table(doc):
    part_table = None
    tables = get_entities(doc, ["AcDbTable"])
    for table in tables:
        col_idx = find_col_idx(table, "PART NUMBER")
        if col_idx != -1:
            part_table = table
            break
    return part_table


def get_part_data(part_table, data_cols):
    part_data = []
    if part_table.TitleSuppressed:
        row_head = 0
    else:
        row_head = 1
    for row in range(row_head + 1, part_table.Rows):
        part_dict = {}
        for col in range(0, part_table.Columns):
            col_name = part_table.GetCellValue(row_head, col)
            if col_name in data_cols:
                part_dict.update({col_name: part_table.GetCellValue(row, col)})
        part_data.append(part_dict)
    return part_data


def create_bom_data(cad_app, metal_takeoff_cols):
    bom_data = []
    for root_dir, dirs, files in os.walk(OUTPUT_PATH):
        for file in files:
            if file.endswith(".dwg"):
                dwg_path = os.path.join(root_dir, file)
                doc = cad_app.Documents.Open(dwg_path)
                part_table = find_part_table(doc)
                if part_table:
                    part_data = get_part_data(part_table, metal_takeoff_cols)
                    elevation_name = os.path.splitext(file)[0]
                    for part_data_dict in part_data:
                        # Description and Mark Qty are unknown.
                        part_bom_data = [elevation_name,  # Elevation
                                         part_data_dict["QTY"],  # Elev Qty
                                         part_data_dict["PART NUMBER"],  # Part
                                         "",  # Description
                                         part_data_dict["FINISH"],  # Finish
                                         part_data_dict["LENGTH"],  # Length
                                         elevation_name.split("-")[0],  # Mark
                                         ""  # Mark Qty
                                         ]
                        bom_data.append(part_bom_data)
                doc.Close(False)
    return bom_data


def create_bom_excel(bom_data, bom_temp_path, file_name):
    rb = xlrd.open_workbook(bom_temp_path)
    wb = copy(rb)
    metal_takeoff_ws = wb.get_sheet(0)
    row_offset = 5
    for row, bom in enumerate(bom_data):
        for i in range(0, 8):
            metal_takeoff_ws.write(row + row_offset, i, bom[i])
    wb.save(os.path.join(os.path.dirname(bom_temp_path), file_name + ".xls"))


def main():
    tkinter.Tk().withdraw()
    cad_app = get_cad_application()
    metal_takeoff_cols = ["QTY", "PART NUMBER", "LENGTH", "FINISH"]
    bom_file_name = os.path.splitext(input("Enter Excel file name: "))[0]
    bom_temp_path = askopenfilename(title="Select the BOM File Template",
                                    filetypes=[("Excel Files", ".xls")])
    bom_data = create_bom_data(cad_app, metal_takeoff_cols)
    create_bom_excel(bom_data, bom_temp_path, bom_file_name)


if __name__ == "__main__":
    main()
