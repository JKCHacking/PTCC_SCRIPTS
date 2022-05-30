import os
import json
import openpyxl
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import tkinter


def write_json_ws(holo_data, ws):
    for k, v in holo_data.items():
        if isinstance(v, dict):
            if k != "child_parts":
                data = [v["u_no"], v["s_no"], v["i_no"], v["desc"], v["desc2"], v["quantity"], v["unit"], v["length"],
                        v["width"], v["height"], v["d_no"]] + v["efal"]
                ws.append(data)
            write_json_ws(v, ws)


def main():
    tkinter.Tk().withdraw()
    holo_num = input("Holoplot Number: ")
    json_file = askopenfilename(title="Select JSON file.",
                               filetypes=[("JSON Files", ".json")])
    save_path = askdirectory(title="Select folder to save excel.")

    if os.path.exists(json_file):
        with open(json_file, "r") as jf:
            holoplot_data = json.load(jf)
        wb = openpyxl.Workbook()
        ws = wb.active
        column_names = ["unique no.", "structure no.", "item no.", "description", "description2", "quantity",
                        "unit", "length", "width", "height", "drawing no.", "E", "F", "A", "L"]
        ws.append(column_names)
        write_json_ws(holoplot_data, ws)
        wb.save(os.path.join(save_path, "H{} Partlist.xlsx".format(holo_num)))


if __name__ == "__main__":
    main()
