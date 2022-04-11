import numpy
import math
import ctypes
import array
from comtypes import client
from comtypes import COMError


def get_min_3d_bb(doc, obj, step_ang):
    """
    Description
    ===========
    Get the minimum bounding box of the object.
    This bounding box algorithm is implemented from the paper proposed by
    C K Chan and S T Tan.

    Parameters
    ==========
    doc: Bricscad document where the object is present.
    obj: the object to get the minimum bounding box.
    step_ang: the angle step to be used for the model when rotating along an axis.

    Return
    ======
    min, max: minimum point and maximum of the minimum bounding box.
    """
    # we should isolate the object first
    doc.SendCommand("SELECT\n(handent \"{}\")\n\n".format(obj.Handle))
    doc.SendCommand("ISOLATE\n")
    # create the 3 viewports of the object in the paperspace for planes XY, ZX, ZY
    # and then get each viewport reference along the way.
    offset = 100
    layout_name = "MinBBScript"
    doc.SendCommand("VIEWBASE\n(handent \"{}\")\n\n{}\n".format(obj.Handle, layout_name))
    doc.SendCommand("0,0,0\n")
    doc.SendCommand("{},0,0\n".format(offset))
    doc.SendCommand("0,{},0\n\n".format(offset))

    # get the viewport references.
    vp_xy = None
    vp_zy = None
    vp_zx = None
    for ps_obj in doc.PaperSpace:
        if ps_obj.ObjectName.lower() == "acdbviewport":
            if ps_obj.Center == (0, offset, 0):
                vp_xy = ps_obj
            elif ps_obj.Center == (offset, 0, 0):
                vp_zy = ps_obj
            elif ps_obj.Center == (0, 0, 0):
                vp_zx = ps_obj

    # create z axis normal to XY plane
    start_pt = array.array("d", list(obj.Centroid))
    end_pt = array.array("d", [obj.Centroid[0], obj.Centroid[1], obj.Centroid[2] + 1])
    # orient object according to minimum bounding of XY plane
    reorient_obj(doc, obj, vp_xy, start_pt, end_pt, step_ang)

    # create Y axis normal to ZX plane
    end_pt = array.array("d", [obj.Centroid[0], obj.Centroid[1] + 1, obj.Centroid[2]])
    # orient object according to minimum bounding of XY plane
    reorient_obj(doc, obj, vp_zx, start_pt, end_pt, step_ang)

    # create X axis normal to ZY plane
    end_pt = array.array("d", [obj.Centroid[0] + 1, obj.Centroid[1], obj.Centroid[2]])
    # orient object according to minimum bounding of XY plane
    reorient_obj(doc, obj, vp_zy, start_pt, end_pt, step_ang)

    # at this point, the model is already aligned in the principal axes
    # get the actual bounding box of the object
    min_pt, max_pt = obj.GetBoundingBox()
    # show the other objects
    doc.SendCommand("UNISOLATE\n")
    # delete the created layout
    doc.Layouts.Item(layout_name).Delete()
    return min_pt, max_pt


def reorient_obj(doc, obj, viewport, start_pt, end_pt, step_ang):
    """
    Description
    ===========
    This function re-orients the model to be align with the plane inputted.

    Parameters
    ==========
    doc: the document where the object resides.
    obj: the object to be re orient.
    viewport: the viewport that holds the projection of the obj to a plane.
    start_pt: the start point of the axis where to rotate.
    end_pt: the end point of the axis where to rotate.
    step_ang: the increment angle of the object during rotation.

    Returns
    =======
    None
    """
    start_angle = 0
    end_angle = math.pi / 2

    # initialize area and angle
    min_area = viewport.Height * viewport.Width
    best_ang = 0

    # getting the minimum bounding box of the plane
    while start_angle <= end_angle:
        # switch to modelspace
        doc.SendCommand("TILEMODE\n1\n")
        # rotate the object in axis
        obj.Rotate3D(start_pt, end_pt, step_ang)
        # switch to paperspace
        doc.SendCommand("TILEMODE\n0\n")
        # To get the minimized bounding box of the viewport we use the height and width to get the area
        # of the viewport and record the area.
        curr_area = viewport.Height * viewport.Width
        start_angle += step_ang
        # determining the minimum area
        if curr_area < min_area:
            min_area = curr_area
            best_ang = start_angle
    doc.SendCommand("TILEMODE\n1\n")
    # rotate the object according to the best angle
    obj.Rotate3D(start_pt, end_pt, best_ang)


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
    na_min_pt, na_max_pt = get_min_3d_bb(doc, obj, step_ang)
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
