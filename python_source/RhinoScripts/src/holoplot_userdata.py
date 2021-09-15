import statistics
import math
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino.Geometry
import Rhino.RhinoApp
import Rhino


class Min3DBoundingBox:
    """Algorithm to calculate the minimum bounding box of an object. Adapted from Mitch Heynick's algorithm"""
    def __get_obj_bbox(self, obj, xform, accurate):
        if isinstance(obj, Rhino.Geometry.Point):
            pt = obj.Location
            if xform:
                pt = xform * pt
            return Rhino.Geometry.BoundingBox(pt, pt)
        elif xform:
            return obj.GetBoundingBox(xform)
        else:
            return obj.GetBoundingBox(accurate)

    def __get_bounding_box_plane(self, objs, plane, ret_pts=False, accurate=True):
        """Returns a plane-aligned bounding box in world coordinates"""
        wxy_plane = Rhino.Geometry.Plane.WorldXY
        xform = Rhino.Geometry.Transform.ChangeBasis(wxy_plane, plane)
        bbox = Rhino.Geometry.BoundingBox.Empty
        if isinstance(objs, list) or isinstance(objs, tuple):
            for obj in objs:
                object_bbox = self.__get_obj_bbox(obj, xform, accurate)
                bbox = Rhino.Geometry.BoundingBox.Union(bbox, object_bbox)
        else:
            object_bbox = self.__get_obj_bbox(objs, xform, accurate)
            bbox = Rhino.Geometry.BoundingBox.Union(bbox, object_bbox)
        if not bbox.IsValid:
            return
        plane_to_world = Rhino.Geometry.Transform.ChangeBasis(plane, wxy_plane)
        if ret_pts:
            corners = list(bbox.GetCorners())
            for pt in corners:
                pt.Transform(plane_to_world)
            return corners
        else:
            box = Rhino.Geometry.Box(bbox)
            box.Transform(plane_to_world)
            return box

    def __rotate_copy_planes(self, tot_ang, count, init_planes, dir_vec):
        """takes a single plane or list of planes as input rotates/copies planes through
        angle tot_ang number of planes=count, number of angle division = count-1"""
        if isinstance(init_planes, Rhino.Geometry.Plane):
            init_planes = [init_planes]
        inc = tot_ang / (count - 1)
        origin = Rhino.Geometry.Point3d(0, 0, 0)
        planes = []
        for i in range(count):
            for init_plane in init_planes:
                new_plane = Rhino.Geometry.Plane(init_plane)
                new_plane.Rotate(inc * i, dir_vec, origin)
                planes.append(new_plane)
        return planes

    def __generate_octant_planes(self, count):
        tot_ang = math.pi * 5  # 90 degress
        # generates an array of count ** 3 planes in 3 axes covering xyz positive octant
        yz_plane = Rhino.Geometry.Plane.WorldYZ
        dir_vec = Rhino.Geometry.Vector3d(1, 0, 0)
        x_planes = self.__rotate_copy_planes(tot_ang, count, yz_plane, dir_vec)
        dir_vec = Rhino.Geometry.Vector3d(0, -1, 0)
        xy_planes = self.__rotate_copy_planes(tot_ang, count, x_planes, dir_vec)
        dir_vec = Rhino.Geometry.Vector3d(0, 0, 1)
        xyz_planes = self.__rotate_copy_planes(tot_ang, count, xy_planes, dir_vec)
        return xyz_planes

    def __rotate_plane_array(self, plane, tot_ang, divs, axis):
        out_planes = []
        plane.Rotate(-tot_ang * 0.5, axis)
        out_planes.append(Rhino.Geometry.Plane(plane))
        inc = tot_ang / (divs - 1)
        for _ in range(divs - 1):
            plane.Rotate(inc, axis)
            out_planes.append(Rhino.Geometry.Plane(plane))
        return out_planes

    def __rotate_plane_array_3d(self, view_plane, tot_ang, divs):
        """Used in 3D refinement calculation"""
        out_planes = []
        yaw_planes = self.__rotate_plane_array(view_plane, tot_ang, divs, view_plane.ZAxis)
        for y_plane in yaw_planes:
            roll_planes = self.__rotate_plane_array(y_plane, tot_ang, divs, y_plane.YAxis)
            for r_plane in roll_planes:
                pitch_planes = self.__rotate_plane_array(r_plane, tot_ang, divs, r_plane.XAxis)
                for p_plane in pitch_planes:
                    out_planes.append(p_plane)
        return out_planes

    def __get_min_bb_plane(self, objs, best_plane, planes, curr_box, curr_vol):
        for plane in planes:
            bb = self.__get_bounding_box_plane(objs, plane)
            if bb.Volume < curr_vol:
                curr_vol = bb.Volume
                best_plane = plane
                curr_box = bb
        return best_plane, curr_box, curr_vol

    def get_min_bb(self, objs, init_plane, count, rel_stop, im_rep):
        curr_bb = self.__get_bounding_box_plane(objs, init_plane)
        curr_vol = curr_bb.Volume

        tot_ang = math.pi * 0.5
        factor = 0.1
        max_passes = 20
        prec = sc.doc.ModelDistanceDisplayPrecision
        us = rs.UnitSystemName(abbreviate=True)

        xyz_planes = self.__generate_octant_planes(count)
        best_plane, curr_bb, curr_vol = self.__get_min_bb_plane(objs, init_plane, xyz_planes, curr_bb, curr_vol)
        if im_rep:
            print("Initial pass 0, volume: {} {}3".format(round(curr_vol, prec), us))

        passes = 0
        for i in range(max_passes):
            passes = i
            prev_vol = curr_vol
            tot_ang *= factor
            ref_planes = self.__rotate_plane_array_3d(best_plane, tot_ang, count)
            best_plane, curr_bb, curr_vol = self.__get_min_bb_plane(objs, best_plane, ref_planes, curr_bb, curr_vol)
            vol_diff = prev_vol - curr_vol
            if rel_stop:
                if vol_diff < 0.0001 * prev_vol:
                    break
            else:
                if vol_diff < sc.doc.ModelAbsoluteTolerance:
                    break
            Rhino.RhinoApp.Wait()
            if im_rep:
                print("Refine pass {}, volume: {} {}3".format(i + 1, round(curr_vol, prec), us))
            if sc.escape_test(False):
                print("Refinement aborted after {} passes.".format(i + 1))
                break
        return curr_bb, curr_vol, passes + 1


def get_position(obj_id):
    pass


def get_revision(obj_id):
    pass


def get_article_at(obj_id):
    pass


def get_template_at(obj_id):
    pass


def get_article_de(obj_id):
    pass


def get_template_de(obj_id):
    pass


def get_template_name_de(obj_id):
    pass


def get_rawmat_no_de(obj_id):
    pass


def get_rawmat_name_de(obj_id):
    pass


def get_material(obj_id):
    pass


def get_weight(obj_id):
    pass


def get_surface(obj_id):
    pass


def get_colour(obj_id):
    pass


def get_screw_lock(obj_id):
    pass


def get_dimensions(obj_id):
    bb_list = []
    bb_points = []
    length = 0
    width = 0
    height = 0
    # setting for determining the
    count = 25
    if rs.IsPolysurface(obj_id):
        surface_ids = rs.ExplodePolysurfaces(obj_id)
        # collect all possible bounding box volumes through all surfaces of the model.
        for surface_id in surface_ids:
            if rs.IsSurfaceTrimmed(surface_id):
                rs.Command("CPlane _O _SelID {}".format(surface_id), echo=False)
                current_cplane = rs.ViewCPlane()
                bb = rs.BoundingBox(obj_id, view_or_plane=current_cplane)
                box_id = rs.AddBox(bb)
                volume = rs.SurfaceVolume(box_id)
                rs.DeleteObject(box_id)
                bb_list.append((volume, bb))
        rs.DeleteObjects(surface_ids)
        # determine the best bounding box for the profile by determining least volume.
        best_bb = min(bb_list, key=lambda x: (x[0][0], x[0][1]))
        bb_points = best_bb[1]
    elif rs.IsBlockInstance(obj_id):
        objs = [rs.coercegeometry(obj_id)]
        wxy_plane = Rhino.Geometry.Plane.WorldXY
        min_bb = Min3DBoundingBox()
        bb, curr_vol, passes = min_bb.get_min_bb(objs, wxy_plane, count, False, True)
        bb_points = bb.GetCorners()

    if bb_points:
        dim1 = rs.Distance(bb_points[0], bb_points[1])
        dim2 = rs.Distance(bb_points[0], bb_points[4])
        dim3 = rs.Distance(bb_points[1], bb_points[2])
        # im not sure how to label the actual dimension taken from the bounding box.
        # im just going to based on the fact that its dimension is Length > Width > Height.
        dims_list = [dim1, dim2, dim3]
        length = max(dims_list)
        width = statistics.median(dims_list)
        height = min(dims_list)

    return length, width, height


def get_coating_area(obj_id):
    pass


def get_gross_area(obj_id):
    pass


def get_net_area(obj_id):
    pass


def get_group(obj_id):
    pass


def get_profession(obj_id):
    pass


def get_delivery(obj_id):
    pass


def get_category(obj_id):
    pass


def get_assembly(obj_id):
    pass


def iter_objects(obj_type):
    obj_list = []
    if obj_type == "Block Instances":
        block_names = rs.BlockNames(True)
        for block_name in block_names:
            block_ids = rs.BlockInstances(block_name)
            for block_id in block_ids:
                obj_list.append(block_id)
    return obj_list


def add_userdata(obj_id):
    length, width, height = get_dimensions(obj_id)
    rs.SetUserText(obj_id, "21_LENGTH", str(round(length, 2)), attach_to_geometry=False)
    rs.SetUserText(obj_id, "22_WIDTH", str(round(width, 2)), attach_to_geometry=False)
    rs.SetUserText(obj_id, "23_HEIGHT", str(round(height, 2)), attach_to_geometry=False)


def main():
    # iterate to all block reference
    blk_ids = iter_objects("Block Instances")
    for blk_id in blk_ids:
        # save the current insertion point and the block name
        blk_in_pt = rs.BlockInstanceInsertPoint(blk_id)
        target_blk_name = rs.BlockInstanceName(blk_id)
        # explode the block instance and place userdata on each part component
        part_ids = rs.ExplodeBlockInstance(blk_id)
        for part_id in part_ids:
            if rs.IsPolysurface(part_id):
                add_userdata(part_id)
            if sc.escape_test(False):
                print("Aborted")
                break
        blk_name = rs.AddBlock(part_ids, blk_in_pt, None, delete_input=True)
        new_blk_id = rs.InsertBlock(blk_name, blk_in_pt)
        if rs.IsBlock(target_blk_name):
            rs.DeleteBlock(target_blk_name)
        rs.RenameBlock(blk_name, target_blk_name)
        add_userdata(new_blk_id)


if __name__ == "__main__":
    main()
