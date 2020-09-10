import numpy as np
import sectionproperties.pre.sections as sections
from math import ceil
from ezdxf import readfile
from ezdxf import math


class PreProcessor:
    def __init__(self, segment_size, has_hole):
        self.seg_siz_mult = segment_size / 100
        self.has_hole = has_hole

    def __get_child_entities_within(self, parent_polyline, modelspace):
        ent_child_list = []
        parent_handle = parent_polyline.dxf.handle
        parent_points = parent_polyline.get_points()
        bbox_parent = math.BoundingBox2d(parent_points)

        for ent in modelspace:
            handle = ent.dxf.handle
            entity_type = ent.dxftype()
            bbox_child = None
            if parent_handle == handle:
                continue
            if entity_type == "LWPOLYLINE":
                points = ent.get_points()
                bbox_child = math.BoundingBox2d(points)
            elif entity_type == "CIRCLE":
                bbox_child = math.ConstructionCircle(math.Vec2(ent.dxf.center[:-1]), ent.dxf.radius).bounding_box

            if bbox_child:
                child_min = bbox_child.extmin
                child_max = bbox_child.extmax
                if bbox_parent.inside(child_min) and bbox_parent.inside(child_max):
                    ent_child_list.append(ent)
        return ent_child_list

    def __get_polylines(self, modelspace):
        pl_list = []
        for ent in modelspace:
            if ent.dxftype() == "LWPOLYLINE" or ent.dxftype == "POLYLINE":
                pl_list.append(ent)
        return pl_list

    def __get_points_and_facets(self, parent_pl, child_ent_list):
        profile_points = []
        profile_facets = []

        parent_bbox = math.BoundingBox2d(parent_pl.get_points('xy'))
        bbox_x = parent_bbox.size[0]
        bbox_y = parent_bbox.size[1]
        shape_size = min(bbox_x, bbox_y)

        for ent in parent_pl.virtual_entities():
            self.__add_to_lists(ent, profile_points, profile_facets, shape_size)
        if child_ent_list:
            for child_ent in child_ent_list:
                if child_ent.dxftype() == "LWPOLYLINE":
                    for ent in child_ent.virtual_entities():
                        self.__add_to_lists(ent, profile_points, profile_facets, shape_size)
                elif child_ent.dxftype() == "CIRCLE":
                    self.__add_to_lists(child_ent, profile_points, profile_facets, shape_size)
        return profile_points, profile_facets

    def __add_to_lists(self, ent, profile_points, profile_facets, shape_size):
        if ent.dxftype() == "LINE":
            profile_points.append(list(ent.dxf.start[:-1]))
            profile_points.append(list(ent.dxf.end[:-1]))
            profile_facets.append([len(profile_points) - 2, len(profile_points) - 1])
        elif ent.dxftype() == "CIRCLE" or ent.dxftype() == "ARC":
            seg_arc_points = self.calculate_arc_segmentation(ent, shape_size)
            try:
                for ind, _ in enumerate(seg_arc_points):
                    profile_points.append(seg_arc_points[ind])
                    profile_points.append(seg_arc_points[ind + 1])
                    profile_facets.append([len(profile_points) - 2, len(profile_points) - 1])
            except IndexError:
                pass

    def calculate_arc_segmentation(self, circular_ent, shape_size):
        seg_arc_pts = []

        if circular_ent.dxftype() == "ARC":
            s_point = circular_ent.start_point[:-1]
            # e_point = arc_ent.end_point[:-1]
            center_point = circular_ent.dxf.center[:-1]
            center_point_x, center_point_y = center_point
            s_point_x, s_point_y = s_point
            # e_point_x, e_point_y = e_point

            radius = circular_ent.dxf.radius
            s_ang = round(circular_ent.dxf.start_angle)
            e_ang = round(circular_ent.dxf.end_angle)

            if e_ang < s_ang:
                e_ang += 360
        else:  # CIRCLE
            center_point = circular_ent.dxf.center[:-1]
            center_point_x, center_point_y = center_point
            radius = circular_ent.dxf.radius
            s_ang = 0
            e_ang = 360
            s_point_x = center_point_x + radius
            s_point_y = center_point_y

        tot_ang = e_ang - s_ang
        seg_size = self.seg_siz_mult * shape_size
        arc_len = abs(radius * np.radians(tot_ang))
        arc_div = ceil(arc_len / seg_size)

        s_ang_rad = np.radians(s_ang)
        e_ang_rad = np.radians(e_ang)
        arc_T = np.linspace(s_ang_rad, e_ang_rad, arc_div)
        list_x = center_point_x + radius * np.cos(arc_T)
        list_y = center_point_y + radius * np.sin(arc_T)

        seg_arc_pts.append([s_point_x, s_point_y])
        for x, y in zip(list_x, list_y):
            seg_arc_pts.append([x, y])
        return seg_arc_pts

    def __get_holes(self, child_ent_list):
        hole_points = []
        for child_ent in child_ent_list:
            if child_ent.dxftype() == "LWPOLYLINE":
                points = child_ent.get_points()
                bbox = math.BoundingBox2d(points)
                hole_points.append(list(bbox.center))
            else:  #CIRCLE
                center_x, center_y = child_ent.dxf.center[:-1]
                hole_points.append([center_x, center_y])
        return hole_points

    def __get_control_points(self, parent_pl, child_ent_list):
        control_point = []
        parent_points = self.__convert_to_vec2s(parent_pl.get_points('xy'))
        parent_bbox = math.BoundingBox2d(parent_points)
        min_pt = parent_bbox.extmin
        max_pt = parent_bbox.extmax

        # boundary of the parent polyline
        x_min = min_pt[0]
        y_min = min_pt[1]
        x_max = max_pt[0]
        y_max = max_pt[1]

        cp_found = False
        # get the candidate X,Y
        for y in np.arange(y_min, y_max, 0.05):
            for x in np.arange(x_min, x_max, 0.05):
                pt_list = [x, y]
                possible_c_point = math.Vec2(pt_list)
                if child_ent_list:  # if there are holes
                    for child_ent in child_ent_list:
                        if child_ent.dxftype() == "LWPOLYLINE":
                            child_points = self.__convert_to_vec2s(child_ent.get_points('xy'))
                            if math.is_point_in_polygon_2d(possible_c_point, parent_points) == 1:
                                if math.is_point_in_polygon_2d(possible_c_point, child_points) == -1:
                                    control_point.append(pt_list)
                                    cp_found = True
                                    break
                        else:  # CIRCLE
                            bbox_child = math\
                                .ConstructionCircle(math.Vec2(child_ent.dxf.center[:-1]), child_ent.dxf.radius)\
                                .bounding_box
                            if bbox_child.inside(possible_c_point):
                                control_point.append(pt_list)
                                cp_found = True
                                break
                else:  # when there are no holes
                    if math.is_point_in_polygon_2d(possible_c_point, parent_points) == 1:
                        control_point.append(pt_list)
                        cp_found = True
                        break
                if cp_found:
                    break
            if cp_found:
                break
        return control_point

    def __convert_to_vec2s(self, pt_list):
        vec2_list = []
        if pt_list:
            for pt in pt_list:
                vec2_pt = math.Vec2(pt)
                vec2_list.append(vec2_pt)
        return vec2_list

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
            child_ent_list = []
            hole_points = []
            if self.has_hole:
                # if theres a hole there should always be child poly-lines inside.
                child_ent_list = self.__get_child_entities_within(parent_pl, mod_space)
                hole_points = self.__get_holes(child_ent_list)

            profile_points, profile_facets = self.__get_points_and_facets(parent_pl, child_ent_list)
            control_points = self.__get_control_points(parent_pl, child_ent_list)

            if (self.has_hole and child_ent_list) or not self.has_hole:
                geometry = sections.CustomSection(
                    profile_points,
                    profile_facets,
                    hole_points,
                    control_points
                )
                geometry_list.append(geometry)
        return geometry_list

    def create_mesh(self, mesh_size):
        '''
            creates the mesh of each geometry inside the drawing file
        '''
        pass

    def create_materials(self, material_list):
        pass