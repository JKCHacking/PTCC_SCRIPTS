import math
import numpy as np
import array
from comtypes import client


bs_app = client.GetActiveObject("BricscadApp.AcadApplication", dynamic=True)
doc = bs_app.ActiveDocument
model = doc.ModelSpace


def get_height_width_coldbent(polyline):
    lines = polyline.Explode()
    # get the top and bottom line
    line_centroid = []
    for line in lines:
        centroid = get_centroid([line.StartPoint, line.EndPoint])
        line_centroid.append([centroid, line])

    top_side = max(line_centroid, key=lambda x: (x[0][2]))[1]
    bottom_side = min(line_centroid, key=lambda x: (x[0][2]))[1]
    right_side = max(line_centroid, key=lambda x: (x[0][0]))[1]
    left_side = min(line_centroid, key=lambda x: (x[0][0]))[1]
    in_between_angle = abs(top_side.Angle - bottom_side.Angle)
    dist_top_side = top_side.Length

    cold_bent = abs(round(dist_top_side * math.sin(in_between_angle), 4))
    height = round(right_side.Length if right_side.Length < left_side.Length else left_side.Length, 4)
    width = round(bottom_side.Length if bottom_side.Length > top_side.Length else top_side.Length, 4)
    return height, width, cold_bent


def get_centroid(vertices):
    centroid = np.mean(vertices, axis=0)
    return centroid[0], centroid[1], centroid[2]


def get_objects(object_name):
    objects = []
    for obj in model:
        if obj.ObjectName == object_name:
            objects.append(obj)
    return objects


def set_object_color(obj, cold_bent):
    color_red = bs_app.GetInterfaceObject("BricscadDb.AcadAcCmColor")
    color_orange = bs_app.GetInterfaceObject("BricscadDb.AcadAcCmColor")
    color_yellow = bs_app.GetInterfaceObject("BricscadDb.AcadAcCmColor")
    color_yellow_green = bs_app.GetInterfaceObject("BricscadDb.AcadAcCmColor")
    color_green = bs_app.GetInterfaceObject("BricscadDb.AcadAcCmColor")
    color_blue = bs_app.GetInterfaceObject("BricscadDb.AcadAcCmColor")
    color_violet = bs_app.GetInterfaceObject("BricscadDb.AcadAcCmColor")

    color_red.SetRGB(255, 0, 0)
    color_orange.SetRGB(255, 165, 0)
    color_yellow.SetRGB(255, 255, 0)
    color_yellow_green.SetRGB(60, 80, 20)
    color_green.SetRGB(0, 128, 0)
    color_blue.SetRGB(0, 0, 255)
    color_violet.SetRGB(238, 130, 238)

    color_string = ''

    if 60 <= cold_bent < 70:
        obj.TrueColor = color_red
        color_string = 'Red'
    elif 50 <= cold_bent < 60:
        obj.TrueColor = color_orange
        color_string = 'Magenta'
    elif 40 <= cold_bent < 50:
        obj.TrueColor = color_yellow
        color_string = 'Yellow'
    elif 30 <= cold_bent < 40:
        obj.TrueColor = color_yellow_green
        color_string = 'Yellow Green'
    elif 20 <= cold_bent < 30:
        obj.TrueColor = color_green
        color_string = 'Green'
    elif 10 <= cold_bent < 20:
        obj.TrueColor = color_blue
        color_string = 'Blue'
    elif 0 <= cold_bent < 10:
        obj.TrueColor = color_violet
        color_string = 'Pink'
    return color_string


def main():
    # ss_obj = doc.SelectionSets.Add("test")
    #
    # point1 = array.array("d", [0, 0, 0])
    # point2 = array.array("d", [0, 0, 0])
    #
    # point1 = doc.Utility.GetPoint(point1, "Specify first corner: ")
    # point2 = doc.Utility.GetPoint(point2, "Specify opposite corner: ")
    # ss_obj.Select(0, array.array("d", list(point1)), array.array("d", list(point2)))
    polylines = get_objects("AcDb3dPolyline")
    for i, polyline in enumerate(polylines):
        doc.StartUndoMark()
        height, width, cold_bent = get_height_width_coldbent(polyline)
        doc.EndUndoMark()
        doc.SendCommand("_undo\n\n")
        set_object_color(polyline, cold_bent)
        print(polyline.Handle, height, width, cold_bent)


if __name__ == "__main__":
    main()
