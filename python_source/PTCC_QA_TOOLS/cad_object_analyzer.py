from comtypes import client
from comtypes import COMError
from comtypes import automation
import array
import ctypes
import csv
import os
import math


SS_NAME = "SSOBJECTS"
CROSSWINDOW_SEL_MODE = 1


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


def get_length(obj):
    min_pt, max_pt = get_bounding_box(obj)
    x_dist = max_pt[0][0] - min_pt[0][0]
    y_dist = max_pt[0][1] - min_pt[0][1]
    z_dist = max_pt[0][2] - min_pt[0][2]
    length = round(max([x_dist, y_dist, z_dist]), 1)
    return length


def get_solids(doc):
    solids = []
    model_space = doc.ModelSpace
    for obj in model_space:
        if obj.ObjectName == "AcDb3dSolid":
            solids.append(obj)
    return solids


def remove_duplicate_objects(doc):
    solids = get_solids(doc)
    to_delete = []
    for solid in solids:
        if solid not in to_delete:
            min_pt, max_pt = get_bounding_box(solid)
            selection_set = doc.SelectionSets.Add(SS_NAME)
            selection_set.Select(CROSSWINDOW_SEL_MODE, min_pt, max_pt)
            if selection_set.Count > 1:
                print("{} duplicates found for {}".format(selection_set.Count, solid.Handle))
                for i in range(1, selection_set.Count):
                    sel_obj = selection_set.Item(i)
                    to_delete.append(sel_obj)
            # so you can use the same SS_NAME
            selection_set.Delete()
    for solid in to_delete:
        try:
            solid.Delete()
        except COMError:
            pass


def create_count_report(doc):
    groups = {}
    solids = get_solids(doc)
    for solid in solids:
        length = get_length(solid)
        if length != 0:
            if length in groups:
                groups.update({length: groups[length] + 1})
            else:
                groups.update({length: 1})
        else:
            print("solid with 0 length: {}".format(solid.Handle))

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


def is_square(obj):
    square = False
    min_pt, max_pt = get_bounding_box(obj)
    x_dist = max_pt[0][0] - min_pt[0][0]
    y_dist = max_pt[0][1] - min_pt[0][1]
    z_dist = max_pt[0][2] - min_pt[0][2]
    dists = [x_dist, y_dist, z_dist]
    max_dist = max(dists)
    dists.remove(max_dist)
    if dists[0] == dists[1]:
        square = True
    return square


def is_vertical(obj):
    vertical = False
    min_pt, max_pt = get_bounding_box(obj)
    x_dist = max_pt[0][0] - min_pt[0][0]
    y_dist = max_pt[0][1] - min_pt[0][1]
    if y_dist > x_dist:
        vertical = True
    return vertical


def get_centroid(obj):
    min_pt, max_pt = get_bounding_box(obj)
    midx = (min_pt[0][0] + max_pt[0][0]) / 2
    midy = (min_pt[0][1] + max_pt[0][1]) / 2
    midz = (min_pt[0][2] + max_pt[0][2]) / 2
    return automation.VARIANT([midx, midy, midz])


def move_solids(solids, start_point):
    col_offset = 0
    row_offset = 0
    padding = 100
    for i, solid in enumerate(solids):
        solid_copy = solid.Copy()
        centroid = array.array("d", get_centroid(solid)[0])
        if is_vertical(solid_copy):
            solid_copy.Rotate(centroid, math.radians(90))
        solid_copy.Move(centroid,
                        array.array("d", [start_point[0] + col_offset + padding, start_point[1] - row_offset, 0]))
        col_offset += get_length(solid)
        if i % 50 == 0:
            col_offset = 0
            row_offset += 1000


def sort_solid(doc):
    square = []
    rect = []
    solids = get_solids(doc)
    for solid in solids:
        if is_square(solid):
            square.append(solid)
        else:
            rect.append(solid)
    move_solids(square, array.array("d",
                                    doc.Utility.GetPoint(
                                        array.array("d", [0, 0, 0]), "Pick a start point for squares: ")))
    move_solids(rect, array.array("d",
                                  doc.Utility.GetPoint(
                                      array.array("d", [0, 0, 0]), "Pick a start point for rectangles: ")))


def main():
    b_cad = get_cad_application()
    doc = b_cad.ActiveDocument
    # removing duplicate objects
    print("Removing duplicate objects...")
    remove_duplicate_objects(doc)
    # create csv file for different solid counts
    print("Creating CSV Count Report...")
    create_count_report(doc)
    # sort according to square and rectangle
    print("Sorting solids...")
    sort_solid(doc)


if __name__ == "__main__":
    main()

