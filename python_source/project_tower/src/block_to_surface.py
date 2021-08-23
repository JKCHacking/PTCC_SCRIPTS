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
            # pt_urf, pt_ulf, pt_lrf, pt_llf, pt_urb, pt_ulb, pt_lrb, pt_llb = get_bounding_box(block)
            # ur_distances = [get_distance_between_points(vertex, pt_urb) for vertex in top_most_vertices]
            # ul_distances = [get_distance_between_points(vertex, pt_ulb) for vertex in top_most_vertices]
            # lr_distances = [get_distance_between_points(vertex, pt_lrb) for vertex in bot_most_vertices]
            # ll_distances = [get_distance_between_points(vertex, pt_llb) for vertex in bot_most_vertices]

            # getting the upper right point
            # upper_right_point = top_most_vertices[ur_distances.index(min(ur_distances))]
            upper_right_point = max(top_most_vertices, key=lambda x: (x[0]))
            # getting the upper left point
            # upper_left_point = top_most_vertices[ul_distances.index(min(ul_distances))]
            upper_left_point = min(top_most_vertices, key=lambda x: (x[0]))
            # getting the lower right point
            # lower_right_point = bot_most_vertices[lr_distances.index(min(lr_distances))]
            lower_right_point = max(bot_most_vertices, key=lambda x: (x[0]))
            # getting the lower left point
            # lower_left_point = bot_most_vertices[ll_distances.index(min(ll_distances))]
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


# def get_distance_between_points(pt1, pt2):
#     distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(pt1, pt2)]))
#     return round(distance, 4)
#
#
# def get_bounding_box(block):
#     sub_objs = block.Explode()
#     vertices = []
#     point = []
#     for sub_obj in sub_objs:
#         if sub_obj.ObjectName == "AcDbLine":
#             vertices.append(sub_obj.StartPoint)
#             vertices.append(sub_obj.EndPoint)
#         elif sub_obj.ObjectName == "AcDbPolyFaceMesh":
#             for i, coordinate in enumerate(sub_obj.Coordinates):
#                 point.append(coordinate)
#                 if (i + 1) % 3 == 0:
#                     point_tup = tuple(point)
#                     vertices.append(point_tup)
#                     point = []
#     vertices = list(set(vertices))
#     bb = ezdxf.math.BoundingBox(vertices)
#     x_llf = bb.extmin[0]
#     y_llf = bb.extmin[1]
#     z_llf = bb.extmin[2]
#
#     x_urb = bb.extmax[0]
#     y_urb = bb.extmax[1]
#     z_urb = bb.extmax[2]
#
#     pt_urf = array.array("d", [x_urb, y_llf, z_urb])
#     pt_ulf = array.array("d", [x_llf, y_llf, z_urb])
#     pt_lrf = array.array("d", [x_urb, y_llf, z_llf])
#     pt_llf = array.array("d", [x_llf, y_llf, z_llf])
#
#     pt_urb = array.array("d", [x_urb, y_urb, z_urb])
#     pt_ulb = array.array("d", [x_llf, y_urb, z_urb])
#     pt_lrb = array.array("d", [x_urb, y_urb, z_llf])
#     pt_llb = array.array("d", [x_llf, y_urb, z_llf])
#
#     return pt_urf, pt_ulf, pt_lrf, pt_llf, pt_urb, pt_ulb, pt_lrb, pt_llb


if __name__ == "__main__":
    main()
