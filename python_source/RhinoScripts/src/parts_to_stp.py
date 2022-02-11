import os
import datetime
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

PRECISION = 3


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


def convert_parts_to_stp(holoplot_num, sel_obj_ids, sel_thread_ids, sel_other_text_ids, mirror_text):
    already_done = []
    for obj_id in sel_obj_ids:
        part_name = get_specific_part_name(obj_id)
        print("Working on: {}".format(part_name))
        if rs.IsPolysurface(obj_id) and\
                "threaded" not in part_name and\
                part_name not in already_done:
            engraving_id = get_engravings(obj_id)
            if engraving_id:
                bb_points = rs.BoundingBox(obj_id, rs.TextObjectPlane(engraving_id))
                thread_ids = get_threads(sel_thread_ids, bb_points)
                other_text_ids = get_other_texts(sel_other_text_ids, bb_points)
                # unmirror all text objects if they are mirrored.
                copy_obj_id = rs.CopyObject(obj_id)
                copy_thread_ids = rs.CopyObjects(thread_ids)
                copy_engraving_id = rs.CopyObject(engraving_id)
                copy_oth_txt_ids = rs.CopyObjects(other_text_ids)
                if mirror_text:
                    unmirror(copy_engraving_id)
                    for other_text_id in copy_oth_txt_ids:
                        unmirror(other_text_id)
                # transform plane
                xform_plane = rg.Transform.PlaneToPlane(rs.TextObjectPlane(copy_engraving_id),
                                                        rs.WorldXYPlane())
                rs.TransformObject(copy_obj_id, xform_plane)
                rs.TransformObject(copy_engraving_id, xform_plane)
                rs.TransformObjects(copy_oth_txt_ids, xform_plane)
                rs.TransformObjects(copy_thread_ids, xform_plane)

                # make the XAxis point to the right and make the YAxis point up
                while round(rs.TextObjectPlane(copy_engraving_id).XAxis[0], PRECISION) <= 0 and \
                        round(rs.TextObjectPlane(copy_engraving_id).YAxis[1], PRECISION) <= 0:
                    rs.RotateObject(copy_obj_id, rs.WorldXYPlane().Origin, 90, rs.WorldXYPlane().Normal)
                    rs.RotateObject(copy_engraving_id, rs.WorldXYPlane().Origin, 90, rs.WorldXYPlane().Normal)
                    rs.RotateObjects(copy_thread_ids, rs.WorldXYPlane().Origin, 90, rs.WorldXYPlane().Normal)
                    rs.RotateObjects(copy_oth_txt_ids, rs.WorldXYPlane().Origin, 90, rs.WorldXYPlane().Normal)

                eng_curve_ids = rs.ExplodeText(copy_engraving_id)
                oth_txt_curve_ids = list()
                for oth_txt_id in copy_oth_txt_ids:
                    curve_ids = rs.ExplodeText(oth_txt_id)
                    oth_txt_curve_ids.extend(curve_ids)
                ids_to_export = list()
                ids_to_export.append(copy_obj_id)
                ids_to_export.extend(copy_thread_ids)
                ids_to_export.extend(eng_curve_ids)
                ids_to_export.extend(oth_txt_curve_ids)
                filename = "{}_00.stp".format(get_specific_part_name(obj_id))
                full_path = "H:\\Desktop\\projects\\holoplot\\HOLOPLOTS\\{}\\{}".format("H" + holoplot_num, filename)
                export_to_stp(full_path, ids_to_export)
                rs.DeleteObject(copy_obj_id)
                rs.DeleteObject(copy_engraving_id)
                rs.DeleteObjects(copy_thread_ids)
                rs.DeleteObjects(copy_oth_txt_ids)
                rs.DeleteObjects(eng_curve_ids)
                rs.DeleteObjects(oth_txt_curve_ids)
            else:
                log_error("Cannot find engraving for {}".format(part_name), holoplot_num)
            already_done.append(part_name)


def unmirror(text_id):
    # mirrored
    start = rs.TextObjectPoint(text_id)
    mid = start + (rs.TextObjectPlane(text_id).YAxis * (rs.TextObjectHeight(text_id) / 2) * -1)
    rs.RotateObject(text_id, mid, 180, rs.TextObjectPlane(text_id).YAxis)
    rs.RotateObject(text_id,
                    mid,
                    180,
                    rs.TextObjectPlane(text_id).Normal)


def log_error(message, holo_num):
    error_file = "H:\\Desktop\\projects\\holoplot\\HOLOPLOTS\\H{holo_num}\\parts2stp_err_H{holo_num}.txt".format(
        holo_num=holo_num)
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
    items = ("Threads", "No", "Yes"), ("OtherTexts", "No", "Yes"), ("MirrorTexts", "No", "Yes")
    result = rs.GetBoolean("Options", items, (False, False, False))
    sel_obj_ids = rs.GetObjects("Select parts to export stp")

    thread_ids = []
    other_text_ids = []
    if result[0]:
        thread_ids = rs.GetObjects("Select threads")
    if result[1]:
        other_text_ids = rs.GetObjects("Select other texts")
    convert_parts_to_stp(holoplot_num, sel_obj_ids, thread_ids, other_text_ids, result[2])


if __name__ == "__main__":
    main()
