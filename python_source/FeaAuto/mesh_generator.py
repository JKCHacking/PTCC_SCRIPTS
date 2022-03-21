import ezdxf
import ezdxf.math
import gmsh


class Line:
    """
        Wrapper class for ezdxf Line for uniformity
    """
    def __init__(self, handle, start_point, end_point):
        self.handle = handle
        self.start_point = ezdxf.math.Vec3(round(start_point.x, 3), round(start_point.y, 3), round(start_point.z, 3))
        self.end_point = ezdxf.math.Vec3(round(end_point.x, 3), round(end_point.y, 3), round(end_point.z, 3))

    def __str__(self):
        return "LINE(#{})".format(self.handle)


class Arc:
    """
        Wrapper class for ezdxf Arc for uniformity
    """
    def __init__(self, handle, center, radius, start_angle, end_angle, start_point, end_point):
        self.handle = handle
        self.center = center
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.start_point = ezdxf.math.Vec3(round(start_point.x, 3), round(start_point.y, 3), round(start_point.z, 3))
        self.end_point = ezdxf.math.Vec3(round(end_point.x, 3), round(end_point.y, 3), round(end_point.z, 3))

    def __str__(self):
        return "ARC(#{})".format(self.handle)


class MeshGenerator:
    def __init__(self):
        gmsh.initialize()
        gmsh.model.add("m1")
        self.model = None
        self.lc = 1e-2

    def polygonize(self, edges):
        groups = []
        for edge1 in edges:
            group = [edge1]
            print("============edge1 changed=============")
            for edge2 in edges:
                if edge1 != edge2 and edge2 not in group and self.is_connected(edge2, group):
                    group.append(edge2)
            if len(group) > 1:
                groups.append(group)
        return groups

    def is_connected(self, edge, group):
        connected = False
        for e in group:
            if edge.start_point in [e.start_point, e.end_point] or \
                    edge.end_point in [e.start_point, e.end_point]:
                connected = True
                break
            print("Edge1 Start:", e.start_point)
            print("Edge1 End:", e.end_point)
            print("Edge2 Start:", edge.start_point)
            print("Edge2 End:", edge.end_point)
            print(connected)
            print("")
        return connected

    def polygonize_test(self, edge1, edges, group):
        for edge2 in edges:
            if edge1 != edge2 and edge2 not in group and self.is_connected_test(edge1, edge2):
                group.append(edge2)
                group = self.polygonize_test(edge2, edges, group)
                break
        return group

    def is_connected_test(self, edge1, edge2):
        connected = False
        if edge1.start_point in [edge2.start_point, edge2.end_point] or \
                edge1.end_point in [edge2.start_point, edge2.end_point]:
            connected = True
        return connected

    def create_geometry(self, dxf_path):
        dxf_doc = ezdxf.readfile(dxf_path)
        model_space = dxf_doc.modelspace()

        edges = []
        for ent in model_space.query("LINE and ARC"):
            if ent.dxftype() == "LINE":
                line = Line(ent.dxf.handle, ent.dxf.start, ent.dxf.end)
                edges.append(line)
            elif ent.dxftype() == "ARC":
                arc = Arc(ent.dxf.handle, ent.dxf.center, ent.dxf.radius, ent.dxf.start_angle, ent.dxf.end_angle,
                          ent.dxf.start_point, ent.dxf.end_point)
                edges.append(arc)
        # poly_groups = self.polygonize(edges)
        poly_groups = self.polygonize_test(edges[0], edges, [edges[0]])
        print(len(poly_groups))


if __name__ == "__main__":
    mg = MeshGenerator()
    mg.create_geometry("H://Desktop//projects//code_aster//test.dxf")
