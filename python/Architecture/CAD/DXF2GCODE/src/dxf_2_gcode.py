import os
import ezdxf
import numpy as np
from math import ceil


class DXF2Gcode:
    def __init__(self, gcode_file):
        self.x_max = 0
        self.x_min = 0
        self.y_max = 0
        self.y_min = 0
        self.gcode_file = gcode_file
        self.lines = []
        self.holes = []
        self.arcs = []

    def read_dxf(self, file):
        dxf_file = ezdxf.readfile(file)
        mod_space = dxf_file.modelspace()
        # every entity in the drawing we need to:
        # 1. get all the points that defines the entity
        # 2. store the entity in a list
        for ent in mod_space:
            if ent.dxftype() == "LWPOLYLINE":
                points = ent.get_points("xy")
                for sub_ent in ent.virtual_entities():
                    self.store_ent(sub_ent)
            elif ent.dxftype() == "LINE":
                points = [ent.dxf.start, ent.dxf.end]
                self.store_ent(ent)
            else:
                points = self.__arc_2_points(ent)
                self.store_ent(ent)

            ent_bb = ezdxf.math.BoundingBox(points)
            x_min, y_min = ent_bb.extmin
            x_max, y_max = ent_bb.extmax

            if x_min < self.x_min:
                self.x_min = x_min
            if x_max > self.x_max:
                self.x_max = x_max
            if y_min < self.y_min:
                self.y_min = y_min
            if y_max > self.y_max:
                self.y_max = y_max

    def store_ent(self, ent):
        if ent.dxftype() == "LINE":
            self.lines.append(ent)
        elif ent.dxftype() == "CIRCLE":  # HOLE
            self.holes.append(ent)
        elif ent.dxftype() == "ARC":
            self.arcs.append(ent)

    def create_gcode(self):
        gcode = ""
        for line in self.lines:
            start_point = line.dxf.start
            end_point = line.dxf.end
            gcode += self.gcode_line(start_point, end_point)
        for hole in self.holes:
            center_point = hole.dxf.center
            radius = hole.dxf.radius
            gcode += self.gcode_hole(center_point, radius)
        for arc in self.arcs:
            start_point = arc.start_point
            end_point = arc.end_point
            center_point = arc.dxf.center
            gcode += self.gcode_arc(start_point, end_point, center_point)
        return gcode

    # TODO: ================================= IMPLEMENTATION TO BE ADDED =====================================
    def gcode_line(self, start_point, end_point):
        gcode_str = ""
        return gcode_str

    def gcode_hole(self, center_point, radius):
        gcode_str = ""
        return gcode_str

    def gcode_arc(self, start_point, end_point, center_point):
        gcode_str = ""
        return gcode_str
    # TODO: ===================================================================================================

    def __arc_2_points(self, circular_ent):
        seg_arc_pts = []

        if circular_ent.dxftype() == "ARC":
            center_point = circular_ent.dxf.center[:-1]
            center_point_x, center_point_y = center_point

            radius = circular_ent.dxf.radius
            s_ang = circular_ent.dxf.start_angle
            e_ang = circular_ent.dxf.end_angle

            if e_ang < s_ang:
                e_ang += 360
        else:  # CIRCLE
            center_point = circular_ent.dxf.center[:-1]
            center_point_x, center_point_y = center_point
            radius = circular_ent.dxf.radius
            s_ang = 0
            e_ang = 360

        arc_div = 10
        s_ang_rad = np.radians(s_ang)
        e_ang_rad = np.radians(e_ang)
        arc_T = np.linspace(s_ang_rad, e_ang_rad, arc_div)
        list_x = center_point_x + radius * np.cos(arc_T)
        list_y = center_point_y + radius * np.sin(arc_T)

        for x, y in zip(list_x, list_y):
            seg_arc_pts.append([x, y])
        return seg_arc_pts

    def write_gcode(self, gcode):
        pass
