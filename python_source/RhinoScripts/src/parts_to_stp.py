import os
import datetime
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

PRECISION = 3


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


def get_other_texts(sel_oth_txt_ids, bb_points):
    other_text_ids = []
    for obj_id in sel_oth_txt_ids:
        if rs.IsObjectInBox(obj_id, bb_points):
            other_text_ids.append(obj_id)
    return other_text_ids


def get_threads(sel_thread_ids, bb_points):
    thread_ids = []
    for obj_id in sel_thread_ids:
        if rs.IsObjectInBox(obj_id, bb_points):
            thread_ids.append(obj_id)
    return thread_ids


def convert_parts_to_stp(holoplot_num, sel_obj_ids, sel_thread_ids, sel_other_text_ids):
    already_done = []
    for obj_id in sel_obj_ids:
        part_name = get_specific_part_name(obj_id)
        print("Working on: {}".format(part_name))
        if rs.IsPolysurface(obj_id) and\
                "threaded" not in part_name and\
                part_name not in already_done:
            bb_points = get_min_bb(obj_id)
            engraving_id = get_engravings(obj_id)
            thread_ids = get_threads(sel_thread_ids, bb_points)
            other_text_ids = get_other_texts(sel_other_text_ids, bb_points)

            if engraving_id:
                # transform plane
                xform_plane = rg.Transform.PlaneToPlane(rs.TextObjectPlane(engraving_id), rs.WorldXYPlane())
                xform_part_id = rs.TransformObject(obj_id, xform_plane, True)
                xform_eng_id = rs.TransformObject(engraving_id, xform_plane, True)
                xform_thread_ids = rs.TransformObjects(thread_ids, xform_plane, True)
                xform_oth_txt_ids = rs.TransformObjects(other_text_ids, xform_plane, True)
                # rotate 180 degrees
                xform_rotate = rs.XformRotation2(180, rs.WorldXYPlane().XAxis,
                                                 rs.WorldXYPlane().Origin)
                rs.TransformObject(xform_part_id, xform_rotate)
                rs.TransformObject(xform_eng_id, xform_rotate)
                rs.TransformObjects(xform_thread_ids, xform_rotate)
                rs.TransformObjects(xform_oth_txt_ids, xform_rotate)

                # make it horizontal or make the X axis point to the right
                while round(rs.TextObjectPlane(xform_eng_id).XAxis[0], PRECISION) <= 0:
                    rs.RotateObject(xform_part_id, rs.WorldXYPlane().Origin, 90, rs.WorldXYPlane().Normal)
                    rs.RotateObject(xform_eng_id, rs.WorldXYPlane().Origin, 90, rs.WorldXYPlane().Normal)
                    rs.RotateObjects(xform_thread_ids, rs.WorldXYPlane().Origin, 90, rs.WorldXYPlane().Normal)
                    rs.RotateObjects(xform_oth_txt_ids, rs.WorldXYPlane().Origin, 90, rs.WorldXYPlane().Normal)
                # unmirror all text objects if they are in mirror form.
                unmirror(xform_eng_id)
                for xform_oth_txt_id in xform_oth_txt_ids:
                    unmirror(xform_oth_txt_id)
                # make the XAxis point to the right and make the YAxis point up
                while round(rs.TextObjectPlane(xform_eng_id).XAxis[0], PRECISION) <= 0 and \
                        round(rs.TextObjectPlane(xform_eng_id).YAxis[1], PRECISION) <= 0:
                    rs.RotateObject(xform_part_id, rs.WorldXYPlane().Origin, 90, rs.WorldXYPlane().Normal)
                    rs.RotateObject(xform_eng_id, rs.WorldXYPlane().Origin, 90, rs.WorldXYPlane().Normal)
                    rs.RotateObjects(xform_thread_ids, rs.WorldXYPlane().Origin, 90, rs.WorldXYPlane().Normal)
                    rs.RotateObjects(xform_oth_txt_ids, rs.WorldXYPlane().Origin, 90, rs.WorldXYPlane().Normal)

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
                filename = "{}_00.stp".format(get_specific_part_name(obj_id))
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
            already_done.append(part_name)


def unmirror(text_id):
    rs.Command("Top")
    # mirrored
    if (rs.TextObjectPlane(text_id).XAxis[0] <= 0 < rs.TextObjectPlane(text_id).YAxis[1]) or \
            (rs.TextObjectPlane(text_id).XAxis[0] > 0 >= rs.TextObjectPlane(text_id).YAxis[1]):
        start = rs.TextObjectPoint(text_id)
        end = start + (rs.TextObjectPlane(text_id).YAxis * rs.TextObjectHeight(text_id) * -1)
        mid = start + (rs.TextObjectPlane(text_id).YAxis * (rs.TextObjectHeight(text_id) / 2) * -1)
        rs.MirrorObject(text_id, start, end)
        rs.RotateObject(text_id,
                        mid,
                        180,
                        rs.WorldXYPlane().Normal)
    rs.Command("Perspective")


def log_error(message, holo_num):
    error_file = "H:\\Desktop\\projects\\holoplot\\H{holo_num}\\parts2stp_err_H{holo_num}.txt".format(holo_num=holo_num)
    if os.path.exists(error_file):
        mode = "a"
    else:
        mode = "w"
    with open(error_file, mode=mode) as err_f:
        err_f.write("[{}]: {}\n".format(datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S"), message))


def reset_rhino_view():
    # reset views
    rs.Command("_4View")
    rs.Command("_4View")
    rs.Command("_-Zoom _E")


def main():
    reset_rhino_view()
    holoplot_num = rs.GetString("Holoplot Number")
    items = ("Threads", "No", "Yes"), ("OtherTexts", "No", "Yes")
    result = rs.GetBoolean("Options", items, (False, False))
    sel_obj_ids = rs.GetObjects("Select parts to export stp")

    thread_ids = []
    other_text_ids = []
    if result[0]:
        thread_ids = rs.GetObjects("Select threads")
    if result[1]:
        other_text_ids = rs.GetObjects("Select other texts")
    convert_parts_to_stp(holoplot_num, sel_obj_ids, thread_ids, other_text_ids)


if __name__ == "__main__":
    main()
