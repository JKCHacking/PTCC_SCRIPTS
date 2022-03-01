import os
import json
import openpyxl
from tkinter.filedialog import askopenfilename
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
    holo_num = input("Holoplot Number:")
    tkinter.Tk().withdraw()
    filename = askopenfilename(initialdir="H:\\Desktop\\projects\\holoplot\\HOLOPLOTS\\H{holo_num}\\".format(
        holo_num=holo_num),
                               filetypes=[("JSON Files", ".json")])
    if os.path.exists(filename):
        with open(filename, "r") as jf:
            holoplot_data = json.load(jf)
        wb = openpyxl.Workbook()
        ws = wb.active
        column_names = ["unique no.", "structure no.", "item no.", "description", "description2", "quantity",
                        "unit", "length", "width", "height", "drawing no.", "E", "F", "A", "L"]
        ws.append(column_names)
        write_json_ws(holoplot_data, ws)
        wb.save("H:\\Desktop\\projects\\holoplot\\HOLOPLOTS\\H{holo_num}\\H{holo_num} Partlist.xlsx".format(
            holo_num=holo_num))


if __name__ == "__main__":
    main()
