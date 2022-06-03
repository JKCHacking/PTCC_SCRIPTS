import gmsh
import os
import sys
from comtypes import client


ROUND_PRECISION = 11


class MeshGenerator3D:
    def __init__(self, doc):
        gmsh.initialize()
        gmsh.model.add("m1")
        self.doc = doc
        self.lc = 0.05
        self.factory = gmsh.model.occ

    def create_mesh(self, obj):
        points = {}
        gmsh_surf = []
        curve_loops = []
        self.doc.StartUndoMark()
        # explode the 3D solid
        self.explode(obj)
        # we should get the exploded parts of the 3d solid which should consists of regions and surfaces
        obj_parts = self.get_objects(["acdbregion", "acdbsurface"])
        for part in obj_parts:
            self.doc.StartUndoMark()
            # explode part to get the 3d lines or arcs.
            self.explode(part)
            entities = self.get_objects(["acdbline", "acdbarc"])
            gmsh_curves = []
            for e in entities:
                curve_tag = None
                if e.ObjectName.lower() == "acdbline":
                    s_tag = self.add_point(e.StartPoint)
                    e_tag = self.add_point(e.EndPoint)
                    curve_tag = self.factory.addLine(s_tag, e_tag)
                elif e.ObjectName.lower() == "acdbarc":
                    c_pt = e.Center
                    curve_tag = self.factory.addCircle(c_pt[0], c_pt[1], c_pt[2],
                                                       e.Radius,
                                                       -1,
                                                       e.StartAngle, e.EndAngle,
                                                       zAxis=list(e.Normal))
                if curve_tag:
                    gmsh_curves.append(curve_tag)
            curve_loop_tag = self.factory.addCurveLoop(gmsh_curves)
            curve_loops.append(curve_loop_tag)
            self.doc.EndUndoMark()
            self.doc.SendCommand("_undo\n\n")
        # unexplode the 3D solid object
        self.doc.EndUndoMark()
        self.doc.SendCommand("_undo\n\n")
        # create the 3d in gmsh
        self.factory.addThruSections(curve_loops)
        self.factory.synchronize()
        # gmsh.model.mesh.generate(3)
        # gmsh.write(os.path.join(self.doc.Path,
        #                         os.path.splitext(self.doc.Name)[0] + ".med"))
        if "-nopopup" not in sys.argv:
            gmsh.fltk.run()
        gmsh.finalize()

    def add_point(self, pt):
        tag = self.factory.addPoint(round(pt[0], ROUND_PRECISION),
                                    round(pt[1], ROUND_PRECISION),
                                    round(pt[2], ROUND_PRECISION), self.lc)
        return tag

    # def create_gmsh_point(self, pt, points):
    #     # create the key for storing in the drawing space
    #     key = self.gen_key(pt)
    #     # check for start point if it exists in the drawing space
    #     if not self.is_pt_exists(pt, points):
    #         tag = self.factory.addPoint(pt[0], pt[1], pt[2], self.lc)
    #         points.update({key: tag})
    #     else:
    #         tag = points[key]
    #     return tag
    #
    # def gen_key(self, pt):
    #     key = "{}-{}-{}".format(pt[0], pt[1], pt[2])
    #     return key
    #
    # def is_pt_exists(self, pt, pt_dict):
    #     exists = False
    #     # create a key from coordinate list
    #     key = self.gen_key(pt)
    #     if key in pt_dict:
    #         exists = True
    #     return exists

    def get_objects(self, obj_names):
        objs = []
        for obj in self.doc.ModelSpace:
            if obj.ObjectName.lower() in [obj_name.lower() for obj_name in obj_names]:
                objs.append(obj)
        return objs

    def explode(self, obj):
        try:
            obj.Explode()
        except AttributeError:
            self.doc.SendCommand("EXPLODE\n(handent \"{}\")\n\n".format(obj.Handle))


def main():
    app = client.GetActiveObject("BricscadApp.AcadApplication")
    doc = app.ActiveDocument
    mg = MeshGenerator3D(doc)
    solids = mg.get_objects(["acdb3dsolid"])
    for solid in solids:
        mg.create_mesh(solid)


if __name__ == "__main__":
    main()
