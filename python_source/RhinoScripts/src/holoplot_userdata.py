import re
import statistics
import math
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino.Geometry
import Rhino.RhinoApp
import Rhino

PROJECT_NUMBER = "1421"
UNIT = rs.UnitSystemName(abbreviate=True)
AL_DEN = 2710  # kg/m^3
SS_DEN = 7849.9764  # kg/m^3
DIM_ROUND_PRECISION = 2
W_ROUND_PRECISION = 4
BB_POINTS = []


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
                add_userdata(part_id, truss_part=True)
            if sc.escape_test(False):
                print("Aborted")
                break
        new_blk_id = create_block(part_ids, target_blk_name, blk_in_pt)
        add_userdata(new_blk_id)


def iter_objects(obj_type):
    obj_list = []
    if obj_type == "Block Instances":
        block_names = rs.BlockNames(True)
        for block_name in block_names:
            block_ids = rs.BlockInstances(block_name)
            for block_id in block_ids:
                obj_list.append(block_id)
    return obj_list


def add_userdata(obj_id, truss_part=False):
    spec_pname = get_specific_part_name(obj_id)
    position = get_position(obj_id)
    revision = get_revision(obj_id)
    article_at = get_article_at(spec_pname)
    # article_de = get_article_de(spec_pname)
    material = get_material(obj_id)
    surface = get_surface(obj_id)
    colour = get_colour(obj_id)
    screw_lock = get_screw_lock(obj_id)
    length, width, height = get_dimensions(obj_id)
    coating_area = get_coating_area(obj_id)
    gross_area = get_gross_area(length, width)
    # net_area = get_net_area(obj_id)
    net_area = coating_area
    profession = get_profession(obj_id)
    delivery = get_delivery(obj_id, truss_part)
    assembly = get_assembly(obj_id)
    group = get_group(obj_id)
    category = get_category(spec_pname)
    template_at = get_template_at(group, category)
    mass = get_weight(obj_id, group)
    template_de = get_template_de(group, category)
    template_name_de = get_template_name_de(obj_id)
    # rawmat_no_de = get_rawmat_no_de(obj_id)
    # rawmat_name_de = get_rawmat_name_de(obj_id)
    name = get_name(spec_pname, category)

    rs.SetUserText(obj_id, "01_POSITION", position)
    rs.SetUserText(obj_id, "02_REVISION", revision)
    rs.SetUserText(obj_id, "03_ARTICLE_AT", article_at)
    rs.SetUserText(obj_id, "04_TEMPLATE_AT", template_at)
    rs.SetUserText(obj_id, "05_ARTICLE_DE", article_at)
    rs.SetUserText(obj_id, "06_TEMPLATE_DE", template_de)
    rs.SetUserText(obj_id, "07_TEMPLATE_NAME_DE", template_name_de)
    rs.SetUserText(obj_id, "08_RAWMAT_NO_DE", template_de)
    rs.SetUserText(obj_id, "09_RAWMAT_NAME_DE", template_name_de)
    rs.SetUserText(obj_id, "10_NAME", name)
    rs.SetUserText(obj_id, "11_MATERIAL", material)
    rs.SetUserText(obj_id, "12_MASS", str(mass))
    # TODO no specification
    rs.SetUserText(obj_id, "13_SURFACE", surface)
    # TODO no specification
    rs.SetUserText(obj_id, "14_COLOUR", colour)
    rs.SetUserText(obj_id, "15_SCREW_LOCK", screw_lock)
    rs.SetUserText(obj_id, "21_LENGTH", str(length))
    rs.SetUserText(obj_id, "22_WIDTH", str(width))
    rs.SetUserText(obj_id, "23_HEIGHT", str(height))
    rs.SetUserText(obj_id, "31_COATING_AREA", coating_area)
    rs.SetUserText(obj_id, "32_GROSS_AREA", gross_area)
    rs.SetUserText(obj_id, "33_NET_AREA", net_area)
    rs.SetUserText(obj_id, "51_GROUP", group)
    rs.SetUserText(obj_id, "52_PROFESSION", profession)
    rs.SetUserText(obj_id, "53_DELIVERY", delivery)
    rs.SetUserText(obj_id, "54_CATEGORY", category)
    rs.SetUserText(obj_id, "55_ASSEMBLY", assembly)


def create_block(part_ids, blk_name, ins_point):
    temp_blk_name = rs.AddBlock(part_ids, ins_point, None, delete_input=True)
    new_blk_id = rs.InsertBlock(temp_blk_name, ins_point)
    if rs.IsBlock(blk_name):
        rs.DeleteBlock(blk_name)
    rs.RenameBlock(temp_blk_name, blk_name)
    return new_blk_id


def get_specific_part_name(obj_id):
    layer = rs.ObjectLayer(obj_id)
    spec_pname = layer.split("::")[-1].split("...")[0].strip()
    return spec_pname


def get_position(obj_id):
    position_list = get_specific_part_name(obj_id).split("-")[1:]
    position = "-".join(position_list)
    return position


def get_revision(obj_id):
    revision = "00"
    return revision


def get_article_at(spec_name):
    article_at = spec_name
    return article_at


def get_template_at(group, category):
    template_at = ""
    if group == "SS sheet":  # stainless steel
        if "Single" in category:
            template_at = "2106"
    else:  # aluminum
        if "Single" in category:
            template_at = "2065"
        elif "Assembly" in category:
            template_at = "2152"
    return template_at


def get_article_de(spec_name):
    article_de = spec_name
    return article_de


def get_template_de(group, category):
    template_de = ""
    if group == "AL sheet":
        if "Single" in category:
            template_de = "V-AL09"
        elif "Assembly" in category:
            template_de = "V-AL21"
    elif group == "AL profile":
        if "Single" in category:
            template_de = "V-AL35"
    elif group == "SS sheet":
        if "Single" in category:
            template_de = "V-VA09"
    return template_de


def get_template_name_de(group):
    template_name_de = ""
    if "AL" in group:
        template_name_de = "AL-Element"
    elif "SS" in group:
        template_name_de = "VA-Blechteil"
    return template_name_de


# def get_rawmat_no_de(obj_id):
#     rawmat_no_de = ""
#     return rawmat_no_de
#
#
# def get_rawmat_name_de(obj_id):
#     rawmat_name_de = ""
#     return rawmat_name_de


def get_name(spec_name, category):
    name_dict = {
        "": "",
        "T": "truss assembly",
        "B": "bracing",
        "F": "frame",
        "TC": "top chord",
        "BC": "bottom chord",
        "EX": "extension part",
        "DP": "diagonal part",
        "PR": "profile",
        "CP": "connection part",
        "EP": "end part",
        "VP": "vertical part",
        "HP": "horizontal part",
        "STC": "standard top chord",
        "SBC": "standard bottom chord",
        "SDP": "standard diagonal part",
        "SCP": "standard connection part"
    }
    p_type = ""
    if category == "Pre-Assembly":
        p_type = spec_name.split("-")[2][0]
    elif category == "Standard Parts Assembly" or category == "Single Part":
        p_type = spec_name.split("-")[3][:2]
    elif category == "Standard Parts Single":
        p_type = spec_name.split("-")[1][:3]
    name = "{} ... {}".format(spec_name, name_dict[p_type])
    return name


def get_material(group):
    material = ""
    if group == "AL sheet":
        material = "aluminum EN AW-5754"
    elif group == "AL profile":
        material = "aluminum EN AW-6060 T66"
    elif group == "SS sheet":
        material = "stainless steel 1.4571"
    return material


def get_weight(obj_id, group):
    tot_sv = 0
    if rs.IsBlockInstance(obj_id):
        blk_in_pt = rs.BlockInstanceInsertPoint(obj_id)
        orig_blk_name = rs.BlockInstanceName(obj_id)
        part_ids = rs.ExplodeBlockInstance(obj_id)
        for part_id in part_ids:
            if rs.IsPolysurface(part_id):
                sv = rs.SurfaceVolume(part_id)[0]
                if UNIT == "mm":
                    tot_sv += sv * 1e-09  # convert to meters3
                else:
                    tot_sv += sv
        create_block(part_ids, orig_blk_name, blk_in_pt)
    elif rs.IsPolysurface(obj_id):
        sv = rs.SurfaceVolume(obj_id)[0]
        if UNIT == "mm":
            tot_sv = sv * 1e-09  # convert to meters3
        else:
            tot_sv = sv
    if group == "SS sheet":
        weight = round(tot_sv * SS_DEN, W_ROUND_PRECISION)
    else:
        weight = round(tot_sv * AL_DEN, W_ROUND_PRECISION)
    return weight


def get_surface(obj_id):
    surface = ""
    return surface


def get_colour(obj_id):
    colour = ""
    return colour


def get_screw_lock(obj_id):
    screw_lock = "NO"
    return screw_lock


def get_dimensions(obj_id):
    bb_list = []
    bb_points = []
    length = 0
    width = 0
    height = 0
    # setting for determining the accuracy of the minimum bounding box
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
        bb, curr_vol, passes = min_bb.get_min_bb(objs, wxy_plane, count, True, True)
        bb_points = bb.GetCorners()

    if bb_points:
        dim1 = rs.Distance(bb_points[0], bb_points[1])
        dim2 = rs.Distance(bb_points[0], bb_points[4])
        dim3 = rs.Distance(bb_points[1], bb_points[2])
        # im not sure how to label the actual dimension taken from the bounding box.
        # im just going to based on the fact that its dimension is Length > Width > Height.
        dims_list = [dim1, dim2, dim3]
        length = round(max(dims_list), DIM_ROUND_PRECISION)
        width = round(statistics.median(dims_list), DIM_ROUND_PRECISION)
        height = round(min(dims_list), DIM_ROUND_PRECISION)
    return length, width, height


def get_coating_area(obj_id):
    tot_c_area = 0
    if rs.IsPolysurface(obj_id):
        tot_c_area += rs.SurfaceArea(obj_id)[0]
        if UNIT == "mm":
            tot_c_area = tot_c_area * 1e-06
    elif rs.IsBlockInstance(obj_id):
        blk_in_pt = rs.BlockInstanceInsertPoint(obj_id)
        orig_blk_name = rs.BlockInstanceName(obj_id)
        part_ids = rs.ExplodeBlockInstance(obj_id)
        for part_id in part_ids:
            if rs.IsPolysurface(part_id):
                sa = rs.SurfaceArea(part_id)[0]
                if UNIT == "mm":
                    tot_c_area += sa * 1e-06  # convert to meters^2
                else:
                    tot_c_area += sa
        create_block(part_ids, orig_blk_name, blk_in_pt)
    tot_c_area = round(tot_c_area, 4)
    return tot_c_area


def get_gross_area(length, width):
    gross_area = length * width
    if UNIT == "mm":
        gross_area *= 1e-06  # convert to meters^2
    return gross_area


# def get_net_area(obj_id):
#     # coating area = net area
#     net_area = get_coating_area(obj_id)
#     return net_area


def get_group(obj_id):
    layer = rs.ObjectLayer(obj_id)
    group = "AL sheet"
    if "profile" in layer:
        group = "AL profile"
    elif "connection part" in layer:
        group = "SS sheet"
    return group


def get_profession(obj_id):
    profession = "HOL"
    return profession


def get_delivery(obj_id, truss_part=False):
    delivery = "S"
    if truss_part:
        delivery = "F"
    return delivery


def get_category(spec_name):
    category = ""
    spec_name_list = spec_name.split("-")
    # not a standard
    if spec_name_list[1].startswith("H"):
        # check if single or assembly
        if len(spec_name_list) == 4:  # single
            if "SP" in spec_name_list[2]:
                category = "Standard Parts Assembly"
            else:
                category = "Single Part"
        elif len(spec_name_list) == 3:  # assembly
            category = "Pre-Assembly"
    elif spec_name_list[1].startswith("S"):  # standard
        category = "Standard Parts Single"
    return category


def get_assembly(obj_id):
    full_path_layer = rs.ObjectLayer(obj_id)
    assembly = full_path_layer.split("::")[0].split("...")[0].split("-")[1].strip()
    return assembly


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


if __name__ == "__main__":
    main()
