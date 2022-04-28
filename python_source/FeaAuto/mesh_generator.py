import os
import sys
import ezdxf
import ezdxf.math
import gmsh

GROUP_APP = "GROUPS"


class Curve:
    def __init__(self, handle, start_point, end_point):
        self.handle = handle
        self.start_point = [round(start_point.x, 3), round(start_point.y, 3), round(start_point.z, 3)]
        self.end_point = [round(end_point.x, 3), round(end_point.y, 3), round(end_point.z, 3)]
        self.group = ""

    def set_group(self, group_name):
        self.group = group_name

    def get_group(self):
        return self.group


class Line(Curve):
    """
        Wrapper class for ezdxf Line for uniformity
    """
    def __init__(self, handle, start_point, end_point):
        super().__init__(handle, start_point, end_point)

    def __str__(self):
        return "LINE(#{})".format(self.handle)


class Arc(Curve):
    """
        Wrapper class for ezdxf Arc for uniformity
    """
    def __init__(self, handle, center, radius, start_angle, end_angle, start_point, end_point):
        super().__init__(handle, start_point, end_point)
        self.center = center
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle

    def __str__(self):
        return "ARC(#{})".format(self.handle)


class MeshGenerator:
    def __init__(self):
        gmsh.initialize()
        gmsh.model.add("m1")
        self.model = None
        self.lc = 1e-2
        self.dxf_path = ""
        self.pts = {}

    def is_connected(self, edge1, edge2):
        connected = False
        if edge1.start_point in [edge2.start_point, edge2.end_point] or \
                edge1.end_point in [edge2.start_point, edge2.end_point]:
            connected = True
        return connected

    def polygonize(self, edge1, edges, polygon):
        for edge2 in edges:
            if edge1 != edge2 and edge2 not in polygon and self.is_connected(edge1, edge2):
                polygon.append(edge2)
                polygon = self.polygonize(edge2, edges, polygon)
                break
        return polygon

    def get_polygons(self, dxf_path):
        self.dxf_path = dxf_path
        dxf_doc = ezdxf.readfile(self.dxf_path)
        model_space = dxf_doc.modelspace()
        edges = []
        for ent in model_space.query("LINE and ARC"):
            try:
                data = ent.get_xdata(GROUP_APP)
            except ezdxf.lldxf.const.DXFValueError:
                data = []
            if ent.dxftype() == "LINE":
                line = Line(ent.dxf.handle, ent.dxf.start, ent.dxf.end)
                if data:
                    # we can add the group name from the extended data
                    line.set_group(data[0][1])
                edges.append(line)
            elif ent.dxftype() == "ARC":
                arc = Arc(ent.dxf.handle, ent.dxf.center, ent.dxf.radius, ent.dxf.start_angle, ent.dxf.end_angle,
                          ent.start_point, ent.end_point)
                if data:
                    # we can add the group name from the extended data
                    arc.set_group(data[0][1])
                edges.append(arc)
        polygons = []
        for edge in edges:
            polygon = self.polygonize(edge, edges, [edge])
            if not any([True if set(p) == set(polygon) else False for p in polygons]):
                polygons.append(polygon)
        return polygons

    def create_mesh(self, polygons):
        # create gmsh model from groups of entity objects
        loops = []
        groups = {}
        # loop to every polygon group
        for polygon in polygons:
            curves = []
            # loop to every line or arc.
            for curve in polygon:
                curve_tag = None
                start_pt = curve.start_point
                end_pt = curve.end_point
                group_name = curve.get_group()
                if start_pt not in self.pts.values():
                    s_tag = gmsh.model.geo.addPoint(start_pt[0], start_pt[1], start_pt[2], self.lc)
                    self.pts.update({s_tag: start_pt})
                if end_pt not in self.pts.values():
                    e_tag = gmsh.model.geo.addPoint(end_pt[0], end_pt[1], end_pt[2], self.lc)
                    self.pts.update({e_tag: end_pt})
                s_tag = self.get_key(start_pt)
                e_tag = self.get_key(end_pt)
                if isinstance(curve, Line):
                    if s_tag and e_tag:
                        curve_tag = gmsh.model.geo.addLine(s_tag, e_tag)
                        curves.append(curve_tag)
                elif isinstance(curve, Arc):
                    c_pt = curve.center
                    if c_pt not in self.pts.values():
                        c_tag = gmsh.model.geo.addPoint(c_pt[0], c_pt[1], c_pt[2], self.lc)
                        self.pts.update({c_tag: c_pt})
                        if s_tag and e_tag and c_tag:
                            curve_tag = gmsh.model.geo.addCircleArc(s_tag, c_tag, e_tag)
                            curves.append(curve_tag)
                # add the group and the curve tag to the dictionary
                if group_name and curve_tag:
                    try:
                        groups[group_name].append(curve_tag)
                    except KeyError:
                        groups.update({group_name: [curve_tag]})
            loop = gmsh.model.geo.addCurveLoop(curves, reorient=True)
            loops.append(loop)
        # create the groups in GMSH
        for gn, tags in groups.items():
            gmsh.model.geo.addPhysicalGroup(1, tags, name=gn)
        gmsh.model.geo.addPlaneSurface(loops)
        gmsh.model.geo.synchronize()
        gmsh.model.mesh.generate(2)
        gmsh.write(os.path.splitext(os.path.basename(self.dxf_path))[0] + ".msh")
        if "-nopopup" not in sys.argv:
            gmsh.fltk.run()
        gmsh.finalize()

    def get_key(self, value):
        key_list = list(self.pts.keys())
        val_list = list(self.pts.values())
        try:
            key = key_list[val_list.index(value)]
        except ValueError:
            key = None
        return key


if __name__ == "__main__":
    mg = MeshGenerator()
    poly_groups = mg.get_polygons("H://Desktop//projects//code_aster//test.dxf")
    mg.create_mesh(poly_groups)
