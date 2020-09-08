import numpy as np
from math import sqrt, ceil
from ezdxf import readfile
from ezdxf import math


class PreProcessor:
    def __init__(self, segment_size):
        self.seg_siz_mult = segment_size / 100

    def __get_polylines_within(self, parent_polyline, polylines):
        pl_child_list = []
        parent_handle = parent_polyline.dxf.handle
        parent_points = parent_polyline.get_points()
        bbox_parent = math.BoundingBox2d(parent_points)
        parent_min = bbox_parent.extmin
        parent_max = bbox_parent.extmax

        for polyline in polylines:
            handle = polyline.dxf.handle
            if parent_handle == handle:
                continue
            points = polyline.get_points()
            bbox_child = math.BoundingBox2d(points)
            child_min = bbox_child.extmin
            child_max = bbox_child.extmax
            if parent_min[0] < child_min[0] and parent_min[1] < child_min[1] and\
                parent_max[0] > child_max[0] and parent_max[1] > child_max[1]:
                pl_child_list.append(polyline)
        return pl_child_list

    def __get_polylines(self, modelspace):
        pl_list = []
        for ent in modelspace:
            if ent.dxftype() == "LWPOLYLINE" or ent.dxftype == "POLYLINE":
                pl_list.append(ent)
        return pl_list

    def __get_points_and_facets(self, parent_pl, child_pl_list):
        profile_points = []
        profile_facets = []

        parent_bbox = math.BoundingBox2d(parent_pl.get_points())
        bbox_x = parent_bbox.size[0]
        bbox_y = parent_bbox.size[1]
        shape_size = min(bbox_x, bbox_y)

        for ent in parent_pl.virtual_entities():
            self.__add_to_lists(ent, profile_points, profile_facets, shape_size)
        for child_pl in child_pl_list:
            for ent in child_pl.virtual_entities():
                self.__add_to_lists(ent, profile_points, profile_facets, shape_size)
        return profile_points, profile_facets

    def __add_to_lists(self, ent, profile_points, profile_facets, shape_size):
        if ent.dxftype() == "LINE":
            profile_points.append(list(ent.dxf.start[:-1]))
            profile_points.append(list(ent.dxf.end[:-1]))
            profile_facets.append([len(profile_points) - 2, len(profile_points) - 1])
        elif ent.dxftype() == "ARC":
            seg_arc_points = self.calculate_arc_segmentation(ent, shape_size)
            for ind, _ in enumerate(seg_arc_points):
                if ind % 2 == 0:
                    profile_points.append(seg_arc_points[ind])
                    profile_points.append(seg_arc_points[ind + 1])
                    profile_facets.append([len(profile_points) - 2, len(profile_points) - 1])

    def calculate_arc_segmentation(self, arc_ent, shape_size):
        seg_arc_pts = []
        s_point = arc_ent.start_point
        e_point = arc_ent.end_point
        center_point = arc_ent.dxf.center
        radius = arc_ent.dxf.radius
        s_ang = arc_ent.dxf.start_angle
        e_ang = arc_ent.dxf.end_angle
        center_point_x = center_point[0]
        center_point_y = center_point[1]
        s_point_x = s_point[0]
        # s_point_y = s_point[1]
        e_point_x = e_point[0]
        # e_point_y = e_point[1]

        start_t = np.arccos((s_point_x - center_point_x) / radius)
        end_t = np.arccos((e_point_x - center_point_x) / radius)

        seg_size = self.seg_siz_mult * shape_size
        tot_ang = e_ang - s_ang
        arc_len = abs(radius * np.radians(tot_ang))
        arc_div = ceil(arc_len / seg_size)
        arc_div = arc_div if arc_div % 2 == 0 else arc_div + 1  # to avoid out of range index later
        arc_T = np.linspace(start_t, end_t, arc_div)

        list_x = center_point_x + radius * np.cos(arc_T)
        list_y = center_point_y + radius * np.sin(arc_T)

        for x, y in zip(list_x, list_y):
            seg_arc_pts.append([x, y])
        return seg_arc_pts

    def __get_holes(self, child_pl_list):

        pass

    def __get_control_points(self):
        pass

    def create_geometry(self, file_fp):
        '''
            creates the geometry of each profile inside the drawing file
        '''
        # list of geometry objects
        geometry_list = []
        drawing_file = readfile(file_fp)
        mod_space = drawing_file.modelspace()
        polylines = self.__get_polylines(mod_space)

        for polyline in polylines:
            print(f"POLYLINE found: {polyline.dxf.handle}")
            parent_pl = polyline
            child_pl_list = self.__get_polylines_within(parent_pl, polylines)
            if child_pl_list:
                # we found a profile
                profile_points, profile_facets = self.__get_points_and_facets(parent_pl, child_pl_list)
                hole_points = self.__get_holes(child_pl_list)

        return geometry_list

    def create_mesh(self, mesh_size):
        '''
            creates the mesh of each geometry inside the drawing file
        '''
        pass

    def create_materials(self, material_list):
        pass