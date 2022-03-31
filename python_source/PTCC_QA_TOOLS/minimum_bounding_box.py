import math
import numpy
import ctypes
import array
from comtypes import client
from comtypes import automation
from comtypes import COMError


def get_cad_application():
    b_cad_guid = "BricscadApp.AcadApplication"
    try:
        b_cad_app = client.GetActiveObject(b_cad_guid, dynamic=True)
    except COMError:
        b_cad_app = client.CreateObject(b_cad_guid, dynamic=True)
    b_cad_app.Visible = True
    return b_cad_app


def get_bb(obj):
    min_pt = automation.VARIANT([0, 0, 0])
    max_pt = automation.VARIANT([0, 0, 0])
    obj.GetBoundingBox(ctypes.byref(min_pt), ctypes.byref(max_pt))
    return min_pt.value, max_pt.value


def get_min_bb(doc, obj, tol):
    fin_min = []
    fin_max = []
    if obj.ObjectName == "AcDb3dSolid":
        fin_min, fin_max = get_bb(obj)
        # compute volume
        fin_vol = (fin_max[0] - fin_min[0]) * (fin_max[1] - fin_min[1]) * (fin_max[2] - fin_min[2])
        pt1 = array.array("d", list(obj.Centroid))
        pt2_x = array.array("d", [obj.Centroid[0] + 1, obj.Centroid[1], obj.Centroid[2]])
        pt2_y = array.array("d", [obj.Centroid[0], obj.Centroid[1] + 1, obj.Centroid[2]])
        pt2_z = array.array("d", [obj.Centroid[0], obj.Centroid[1], obj.Centroid[2] + 1])

        doc.StartUndoMark()
        # rotate z axis
        for z_ang in numpy.linspace(0, math.pi, int(math.pi / tol)):
            obj.Rotate3d(pt1, pt2_z, z_ang)
            # rotate in y axis
            for y_ang in numpy.linspace(0, math.pi, int(math.pi / tol)):
                obj.Rotate3d(pt1, pt2_y, y_ang)
                # rotate in x axis
                for x_ang in numpy.linspace(0, math.pi, int(math.pi / tol)):
                    print("\rZ_ANG: {} Y_ANG: {} X_ANG: {}".format(z_ang, y_ang, x_ang), flush=True, end="")
                    obj.Rotate3d(pt1, pt2_x, x_ang)
                    temp_min, temp_max = get_bb(obj)
                    # compute volume
                    temp_vol = abs(temp_max[0] - temp_min[0]) * abs(temp_max[1] - temp_min[1]) * abs(temp_max[2] -
                                                                                                     temp_min[2])
                    if temp_vol < fin_vol:
                        fin_vol = temp_vol
                        fin_min = temp_min
                        fin_max = temp_max
    doc.EndUndoMark()
    doc.SendCommand("_U\n")
    return fin_min, fin_max


def main():
    bs_app = get_cad_application()
    doc = bs_app.ActiveDocument
    model_space = doc.ModelSpace
    tol = 0.01
    for obj in model_space:
        min_pt, max_pt = get_min_bb(doc, obj, tol)
        print("")
        print(min_pt, max_pt)


if __name__ == "__main__":
    main()
