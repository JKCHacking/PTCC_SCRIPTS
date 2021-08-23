import ezdxf
import array
import math
from comtypes import client
import numpy as np

briscad_app = client.GetActiveObject("BricscadApp.AcadApplication", dynamic=True)
briscad_app.Visible = True

doc = briscad_app.ActiveDocument
modelspace = doc.ModelSpace


def main():
    block_count = 0
    blocks = get_objects("AcDbBlockReference")
    for i, block in enumerate(blocks):
        print("\rWorking with Block {}/{}".format(i+1, len(blocks)), end="", flush=True)
        doc.StartUndoMark()
        try:
            top_most_vertices, bot_most_vertices = get_top_bot_most_vertices(block)
            # getting the upper right point
            upper_right_point = max(top_most_vertices, key=lambda x: (x[0]))
            # getting the upper left point
            upper_left_point = min(top_most_vertices, key=lambda x: (x[0]))
            # getting the lower right point
            lower_right_point = max(bot_most_vertices, key=lambda x: (x[0]))
            # getting the lower left point
            lower_left_point = min(bot_most_vertices, key=lambda x: (x[0]))
        except ValueError:
            continue
        doc.EndUndoMark()
        doc.SendCommand("_undo\n\n")
        block.Delete()
        poly_line = modelspace.Add3Dpoly(
            array.array("d", [upper_right_point[0], upper_right_point[1], upper_right_point[2],
                              upper_left_point[0], upper_left_point[1], upper_left_point[2],
                              lower_left_point[0], lower_left_point[1], lower_left_point[2],
                              lower_right_point[0], lower_right_point[1], lower_right_point[2],
                              upper_right_point[0], upper_right_point[1], upper_right_point[2]])
        )
    print("")
    # flatten all 3d poly lines
    poly_3d_list = get_objects("AcDb3dPolyline")
    for i, poly_3d in enumerate(poly_3d_list):
        print("\rFlattening 3D Polyline {}/{}".format(i+1, len(poly_3d_list)), end="", flush=True)
        hand = poly_3d.Handle
        doc.SendCommand('FLATTEN\n(handent "{}")\n\n'.format(hand))
    print("")
    # convert all 2d poly lines to region
    poly_2d_list = get_objects("AcDb2dPolyline")
    for i, poly_2d in enumerate(poly_2d_list):
        print("\rConverting 2D Polyline to Region {}/{}".format(i + 1, len(poly_2d_list)), end="", flush=True)
        hand = poly_2d.Handle
        doc.SendCommand('REGION\n(handent "{}")\n\n'.format(hand))


def get_objects(object_name):
    objs = []
    for obj in modelspace:
        if obj.ObjectName == object_name:
            objs.append(obj)
    return objs


def get_top_bot_most_vertices(block):
    top_most_vertices = []
    top_most_centroid = ()
    bot_most_vertices = []
    bot_most_centroid = ()
    sub_objs = block.Explode()
    for sub_obj in sub_objs:
        if sub_obj.ObjectName == "AcDbPolyFaceMesh":
            point = []
            vertices = []
            for i, coordinate in enumerate(sub_obj.Coordinates):
                point.append(coordinate)
                if (i + 1) % 3 == 0:
                    point_tup = tuple(point)
                    vertices.append(point_tup)
                    point = []
            centroid = get_centroid(vertices)
            if not top_most_centroid:
                top_most_vertices = vertices
                top_most_centroid = centroid
            else:
                if centroid[2] > top_most_centroid[2]:
                    top_most_vertices = vertices
                    top_most_centroid = centroid

            if not bot_most_centroid:
                bot_most_vertices = vertices
                bot_most_centroid = centroid
            else:
                if centroid[2] < bot_most_centroid[2]:
                    bot_most_vertices = vertices
                    bot_most_centroid = centroid
    return top_most_vertices, bot_most_vertices

def get_centroid(vertices):
    centroid = np.mean(vertices, axis=0)
    return centroid[0], centroid[1], centroid[2]





if __name__ == "__main__":
    main()
