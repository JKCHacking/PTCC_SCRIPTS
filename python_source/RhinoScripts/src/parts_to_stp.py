import rhinoscriptsyntax as rs
import Rhino.Geometry as rg


def get_bounding_box(obj_id):
    bb_points = []
    bb_list = []
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
        pass
    return bb_points


def orient_to_top(part_id, misc_ids):
    bb_points = get_bounding_box(part_id)
    box = rs.AddBox(bb_points)
    surfaces = rs.ExplodePolysurfaces(box)
    areas = []
    for surface in surfaces:
        areas.append(rs.SurfaceArea(surface))
    lying_plane = surfaces[areas.index(max(areas))]
    rs.Command("CPlane _O _SelID {}".format(lying_plane), echo=False)
    curr_cplane = rs.ViewCPlane()
    top_plane = rs.ViewCPlane("Top")
    xform = rg.Transform.PlaneToPlane(curr_cplane, top_plane)
    new_obj_id = rs.TransformObject(part_id, matrix=xform, copy=True)
    new_misc_ids = []
    for obj_id in misc_ids:
        new_misc_id = rs.TransformObject(obj_id, matrix=xform, copy=True)
        new_misc_ids.append(new_misc_id)
    rs.DeleteObjects(surfaces)
    rs.DeleteObject(box)
    return new_obj_id, new_misc_ids


def export_to_stp(stp_filename, obj_ids):
    rs.SelectObjects(obj_ids)
    rs.Command("_-Export {} _Enter".format(stp_filename), False)
    rs.UnselectObjects(obj_ids)


def get_specific_part_name(obj_id):
    layer = rs.ObjectLayer(obj_id)
    spec_pname = layer.split("::")[-1].split("...")[0].strip()
    return spec_pname


def search_nearest_text(part_id):
    position_list = get_specific_part_name(part_id).split("-")[1:]
    position = " ".join(position_list)
    all_obj_ids = rs.AllObjects()
    txt_ids = []
    for obj_id in all_obj_ids:
        if rs.IsText(obj_id) and rs.TextObjectText(obj_id) == position:
            txt_ids.append(obj_id)
    part_cent_pt = rs.SurfaceVolumeCentroid(part_id)[0]
    txt_pt_list = [rs.TextObjectPoint(txt_id) for txt_id in txt_ids]
    pt_ids = rs.AddPoints(txt_pt_list)
    closest_pt_id, pt_obj = rs.PointClosestObject(part_cent_pt, pt_ids)
    txt_id = txt_ids[txt_pt_list.index(pt_obj)]
    rs.DeleteObjects(pt_ids)
    return txt_id


def get_multiparts(holoplot_num):
    all_obj_ids = rs.GetObjects("Select parts to export stp")
    for obj_id in all_obj_ids:
        if rs.IsPolysurface(obj_id):
            ids_to_export = []
            full_path = "H:\\Desktop\\projects\\holoplot\\{}\\{}"
            txt_id = search_nearest_text(obj_id)
            misc_ids = [txt_id]
            or_part_id, or_misc_ids = orient_to_top(obj_id, misc_ids)
            or_txt_id = or_misc_ids[0]
            curve_ids = rs.ExplodeText(or_txt_id)
            ids_to_export.append(or_part_id)
            ids_to_export.extend(curve_ids)
            filename = "{}.stp".format(get_specific_part_name(or_part_id))
            full_path = full_path.format("H" + holoplot_num, filename)
            export_to_stp(full_path, ids_to_export)
            rs.DeleteObject(or_part_id)
            rs.DeleteObject(or_txt_id)
            rs.DeleteObjects(curve_ids)


def get_single_part_misc(holoplot_num):
    ids_to_export = []
    curve_ids = []
    part_id = rs.GetObject("Select part to export stp")
    misc_ids = rs.GetObjects("Select miscellaneous of part")
    txt_id = search_nearest_text(part_id)
    misc_ids.append(txt_id)
    or_part_id, or_misc_ids = orient_to_top(part_id, misc_ids)
    ids_to_export.append(or_part_id)
    for or_misc_id in or_misc_ids:
        if rs.IsText(or_misc_id):
            curve_ids = rs.ExplodeText(or_misc_id)
            ids_to_export.extend(curve_ids)
        else:
            ids_to_export.append(or_misc_id)
    filename = "H:\\Desktop\\projects\\holoplot\\{}\\{}.stp".format("H" + holoplot_num,
                                                                    get_specific_part_name(or_part_id))
    export_to_stp(filename, ids_to_export)
    rs.DeleteObject(or_part_id)
    rs.DeleteObjects(or_misc_ids)
    rs.DeleteObjects(curve_ids)


def main():
    holoplot_num = rs.GetString("Holoplot Number")
    user_choice = rs.GetString("multi or single")
    if user_choice == "multi":
        get_multiparts(holoplot_num)
    elif user_choice == "single":
        get_single_part_misc(holoplot_num)
    else:
        print("Incorrect input")


if __name__ == "__main__":
    main()
