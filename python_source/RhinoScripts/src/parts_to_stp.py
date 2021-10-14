import os
import datetime
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg


def get_min_bb(obj_id):
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


def get_lying_plane_xform(bb_points):
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
    rs.DeleteObject(box)
    rs.DeleteObjects(surfaces)
    return xform


def tranform_objects(obj_ids, xform):
    xform_obj_ids = []
    for obj_id in obj_ids:
        xform_obj_ids.append(rs.TransformObject(obj_id, matrix=xform, copy=True))
    return xform_obj_ids


def export_to_stp(stp_filename, obj_ids):
    rs.SelectObjects(obj_ids)
    rs.Command("_-Export {} _Enter".format(stp_filename), False)
    rs.UnselectObjects(obj_ids)


def get_specific_part_name(obj_id):
    layer = rs.ObjectLayer(obj_id)
    spec_pname = layer.split("::")[-1].split("...")[0].strip()
    return spec_pname


def get_engravings(part_id):
    position_list = get_specific_part_name(part_id).split("-")[1:]
    position = " ".join(position_list)
    all_obj_ids = rs.AllObjects()
    txt_ids = []
    for obj_id in all_obj_ids:
        if rs.IsText(obj_id) and rs.TextObjectText(obj_id) == position:
            txt_ids.append(obj_id)
    if txt_ids:
        part_cent_pt = rs.SurfaceVolumeCentroid(part_id)[0]
        txt_pt_list = [rs.TextObjectPoint(txt_id) for txt_id in txt_ids]
        pt_ids = rs.AddPoints(txt_pt_list)
        closest_pt_id, pt_obj = rs.PointClosestObject(part_cent_pt, pt_ids)
        txt_id = txt_ids[txt_pt_list.index(pt_obj)]
        rs.DeleteObjects(pt_ids)
    else:
        txt_id = None
    return txt_id


def get_other_texts(bb_points):
    other_text_ids = []
    all_obj_ids = rs.AllObjects()
    for obj_id in all_obj_ids:
        obj_name = rs.ObjectLayer(obj_id).split("::")[-1]
        if rs.IsText(obj_id) and rs.TextObjectText(obj_id) not in obj_name and rs.IsObjectInBox(obj_id, bb_points):
            other_text_ids.append(obj_id)
    return other_text_ids


def get_threads(bb_points):
    thread_ids = []
    # find all threads that's inside the part
    all_obj_ids = rs.AllObjects()
    for obj_id in all_obj_ids:
        obj_name = rs.ObjectLayer(obj_id).split("::")[-1]
        if rs.IsPolysurface(obj_id) and "threaded" in obj_name and rs.IsObjectInBox(obj_id, bb_points):
            thread_ids.append(obj_id)
    return thread_ids


def convert_parts_to_stp(holoplot_num, sel_obj_ids):
    for obj_id in sel_obj_ids:
        part_name = get_specific_part_name(obj_id)
        print("Working on: {}".format(part_name))
        if rs.IsPolysurface(obj_id) and "threaded" not in part_name:
            bb_points = get_min_bb(obj_id)
            engraving_id = get_engravings(obj_id)
            thread_ids = get_threads(bb_points)
            other_text_ids = get_other_texts(bb_points)
            if engraving_id:
                lying_xform = get_lying_plane_xform(bb_points)
                xform_part_id = tranform_objects([obj_id], lying_xform)[0]
                xform_eng_id = tranform_objects([engraving_id], lying_xform)[0]
                xform_thread_ids = tranform_objects(thread_ids, lying_xform)
                xform_oth_txt_ids = tranform_objects(other_text_ids, lying_xform)
                xform_eng_curve_ids = rs.ExplodeText(xform_eng_id)
                xform_oth_txt_curve_ids = list()
                for xform_oth_txt_id in xform_oth_txt_ids:
                    curve_ids = rs.ExplodeText(xform_oth_txt_id)
                    xform_oth_txt_curve_ids.extend(curve_ids)
                ids_to_export = list()
                ids_to_export.append(xform_part_id)
                ids_to_export.extend(xform_thread_ids)
                ids_to_export.extend(xform_eng_curve_ids)
                ids_to_export.extend(xform_oth_txt_curve_ids)
                filename = "{}.stp".format(get_specific_part_name(obj_id))
                full_path = "H:\\Desktop\\projects\\holoplot\\{}\\{}".format("H" + holoplot_num, filename)
                export_to_stp(full_path, ids_to_export)
                rs.DeleteObject(xform_part_id)
                rs.DeleteObject(xform_eng_id)
                rs.DeleteObjects(xform_thread_ids)
                rs.DeleteObjects(xform_oth_txt_ids)
                rs.DeleteObjects(xform_eng_curve_ids)
                rs.DeleteObjects(xform_oth_txt_curve_ids)
            else:
                log_error("Cannot find engraving for {}".format(part_name), holoplot_num)


def log_error(message, holo_num):
    error_file = "parts2stp_err_H{}.txt".format(holo_num)
    if os.path.exists(error_file):
        mode = "a"
    else:
        mode = "w"
    with open(error_file, mode=mode) as err_f:
        err_f.write("[{}]: {}\n".format(datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S"), message))


def main():
    holoplot_num = rs.GetString("Holoplot Number")
    sel_obj_ids = rs.GetObjects("Select parts to export stp")
    convert_parts_to_stp(holoplot_num, sel_obj_ids)


if __name__ == "__main__":
    main()
