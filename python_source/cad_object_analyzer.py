from comtypes import client
from comtypes import COMError
from comtypes import automation
import ctypes
import csv
import os


def get_cad_application():
    b_cad_guid = "BricscadApp.AcadApplication"
    try:
        b_cad_app = client.GetActiveObject(b_cad_guid, dynamic=True)
    except COMError:
        b_cad_app = client.CreateObject(b_cad_guid, dynamic=True)
    b_cad_app.Visible = True
    return b_cad_app


def get_bounding_box(obj):
    min_pt = automation.VARIANT([0, 0, 0])
    max_pt = automation.VARIANT([0, 0, 0])
    obj.GetBoundingBox(ctypes.byref(min_pt), ctypes.byref(max_pt))
    return min_pt, max_pt


def main():
    b_cad = get_cad_application()
    doc = b_cad.ActiveDocument
    modelSpace = doc.ModelSpace
    groups = {}
    for obj in modelSpace:
        if obj.ObjectName == "AcDb3dSolid":
            min_pt, max_pt = get_bounding_box(obj)
            x_dist = max_pt[0][0] - min_pt[0][0]
            y_dist = max_pt[0][1] - min_pt[0][1]
            z_dist = max_pt[0][2] - min_pt[0][2]
            length = round(max([x_dist, y_dist, z_dist]), 1)
            if length in groups:
                groups.update({length: groups[length] + 1})
            else:
                groups.update({length: 1})

    total = 0
    output = "H://Desktop//projects//ObjectCounter"
    csv_out = os.path.splitext(os.path.basename(doc.GetVariable("dwgname")))[0] + ".csv"
    with open(os.path.join(output, csv_out), "w", newline="") as csvfile:
        fieldnames = ["Length", "Count"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key, value in groups.items():
            print("{}: {}".format(key, value))
            writer.writerow({"Length": key, "Count": value})
            total = total + value
    print("Total: {}".format(total))


if __name__ == "__main__":
    main()

