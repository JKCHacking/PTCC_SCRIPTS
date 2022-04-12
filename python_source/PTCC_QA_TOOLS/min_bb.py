import numpy
import math
import ctypes
import array
from comtypes import client
from comtypes import COMError


def get_min_3d_bb(obj, step_ang):
    """
    Description
    ===========
    Get the minimum bounding box of the object.
    This bounding box algorithm is implemented from the paper proposed by
    C K Chan and S T Tan.

    Parameters
    ==========
    obj: the object to get the minimum bounding box.
    step_ang: the angle step to be used for the model when rotating along an axis.

    Return
    ======
    min, max: minimum point and maximum of the minimum bounding box.
    """
    planes = ["xy", "xz", "yz"]
    for plane in planes:
        reorient_obj(obj, step_ang, plane)
    # from this point the object is already aligned in the world axis.
    min_pt, max_pt = obj.GetBoundingBox()
    return min_pt, max_pt


def reorient_obj(obj, step_ang, plane):
    """
    Description
    ===========
    This function re-orients the model to be align with the plane inputted.

    Parameters
    ==========
    obj: the object to be re orient.
    step_ang: the increment angle of the object during rotation.

    Returns
    =======
    None
    """
    start_angle = 0
    end_angle = math.pi / 2
    min_area = math.inf
    best_angle = 0
    start_axis = array.array("d", obj.Centroid)
    end_axis = []
    index = [0] * 3

    if plane == "xy":
        index = [1, 1, 0]
        end_axis = array.array("d", [obj.Centroid[0], obj.Centroid[1], obj.Centroid[2] + 1])
    elif plane == "xz":
        index = [1, 0, 1]
        end_axis = array.array("d", [obj.Centroid[0], obj.Centroid[1] + 1, obj.Centroid[2]])
    elif plane == "yz":
        index = [0, 1, 1]
        end_axis = array.array("d", [obj.Centroid[0] + 1, obj.Centroid[1], obj.Centroid[2]])

    min_pt, max_pt = obj.GetBoundingBox()
    # projecting the points to the plane
    project_points_to_plane(min_pt, max_pt, index)
    while start_angle <= end_angle:
        obj.Rotate3D(start_axis, end_axis, step_ang)
        # compute the area
        dims = [(max_pt[0] - min_pt[0]), (max_pt[1] - min_pt[1]), (max_pt[2] - min_pt[2])]
        curr_area = 1
        for dim in dims:
            if dim > 0:
                curr_area *= dim
        if curr_area < min_area:
            min_area = curr_area
            best_angle = start_angle
        start_angle += step_ang
        min_pt, max_pt = obj.GetBoundingBox()
        # projecting the points to the plane
        project_points_to_plane(min_pt, max_pt, index)
    # rotate the object using the best angle
    obj.Rotate3D(start_axis, end_axis, best_angle)


def project_points_to_plane(pt1, pt2, plane_index):
    # projecting the points to the plane
    pt1 = [pt1[0] * plane_index[0], pt1[1] * plane_index[1], pt1[2] * plane_index[2]]
    pt2 = [pt2[0] * plane_index[0], pt2[1] * plane_index[1], pt2[2] * plane_index[2]]
    return pt1, pt2


def get_volume_from_points(min_pt, max_pt):
    """
    Description
    ===========
    Function that computes the volume of a 3D object based from 2 points.

    Parameters
    ==========
    min_pt: minimum point of the bounding box of the object.
    max_pt: maximum point of the bounding box of the object.

    Returns
    =======
    vol: Computed volume
    """
    vol = (max_pt[0] - min_pt[0]) * (max_pt[1] - min_pt[1]) * (max_pt[2] - min_pt[2])
    return vol


def get_3d_bb(doc, obj, step_ang):
    """
    Description
    ===========
    Generic function that gets the bounding box of a 3D object. Specifically solid objects

    Parameters
    ==========
    doc: Document object where the 3D object resides.
    obj: 3D object to get its bounding box.
    step_ang: the step angle to be used during computation of the minimum bounding box object.

    Return
    ======
    min_pt: minimum point of the computed bounding box.
    max_pt: maximum point of the computed bounding box.
    """
    # get the aligned bounding box first for checking later
    a_min_pt, a_max_pt = obj.GetBoundingBox()
    # compute the minimum bounding box.
    doc.StartUndoMark()
    na_min_pt, na_max_pt = get_min_3d_bb(obj, step_ang)
    doc.EndUndoMark()
    doc.SendCommand("_undo\n\n")

    a_vol = get_volume_from_points(a_min_pt, a_max_pt)
    na_vol = get_volume_from_points(na_min_pt, na_max_pt)
    if a_vol < na_vol:
        min_pt = a_min_pt
        max_pt = a_max_pt
    else:
        min_pt = na_min_pt
        max_pt = na_max_pt
    return min_pt, max_pt


def main():
    cad_app = client.GetActiveObject("BricscadApp.AcadApplication")
    doc = cad_app.ActiveDocument
    step_ang = math.radians(2)
    for obj in doc.ModelSpace:
        if obj.ObjectName.lower() == "acdb3dsolid":
            min_pt, max_pt = get_3d_bb(doc, obj, step_ang)
            print(min_pt)
            print(max_pt)
            print("")


if __name__ == "__main__":
    main()
