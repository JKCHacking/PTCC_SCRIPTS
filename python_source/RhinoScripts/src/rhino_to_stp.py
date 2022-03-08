import os
import datetime
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

PRECISION = 3
HOLOPLOT_NUM = ""
IS_TEXT_MIRROR = False
STP_FOLDER = ""


def export_to_stp(stp_filename, obj_ids):
    rs.SelectObjects(obj_ids)
    rs.Command("_-Export {} _Enter".format(stp_filename), False)
    rs.UnselectObjects(obj_ids)


def get_specific_part_name(obj_id):
    layer = rs.ObjectLayer(obj_id)
    spec_pname = layer.split("::")[-1].split("...")[0].strip()
    return spec_pname


def get_engravings(part_id, all_obj_ids=None):
    position_list = get_specific_part_name(part_id).split("-")[1:]
    position = " ".join(position_list)
    txt_ids = []
    if not all_obj_ids:
        all_obj_ids = rs.AllObjects()

    for obj_id in all_obj_ids:
        if rs.IsText(obj_id) and \
                "".join(rs.TextObjectText(obj_id).split()).lower() == "".join(position.split()).lower():
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


# def get_other_texts(bb_points, local_objs):
#     other_text_ids = []
#     for obj_id in local_objs:
#         if rs.IsText(obj_id) and rs.IsObjectInBox(obj_id, bb_points, test_mode=True):
#             other_text_ids.append(obj_id)
#     return other_text_ids


def get_threads(obj_id, local_objs):
    thread_ids = []
    obj_layer = rs.ObjectLayer(obj_id)
    # get the sub layers of the obj
    child_layers = rs.LayerChildren(obj_layer)
    for child_layer in child_layers:
        if child_layer.split("::")[-1].startswith("threaded"):
            # search within the local objects.
            for obj in local_objs:
                if child_layer == rs.ObjectLayer(obj):
                    thread_ids.append(obj)
    return thread_ids


def unmirror(text_id):
    # mirrored
    start = rs.TextObjectPoint(text_id)
    mid = start + (rs.TextObjectPlane(text_id).YAxis * (rs.TextObjectHeight(text_id) / 2) * -1)
    rs.RotateObject(text_id, mid, 180, rs.TextObjectPlane(text_id).YAxis)
    rs.RotateObject(text_id,
                    mid,
                    180,
                    rs.TextObjectPlane(text_id).Normal)


def reset_rhino_view():
    # reset views
    rs.Command("_4View")
    rs.Command("_4View")
    rs.Command("_-Zoom _E")


def rhino_to_stp(obj_ids):
    already_done = []
    for obj_id in obj_ids:
        part_name = get_specific_part_name(obj_id)
        print("Working with {}".format(part_name))
        if part_name.startswith("1421") and part_name not in already_done:
            if rs.IsPolysurface(obj_id):
                convert_part(obj_id, obj_ids)
            elif rs.IsBlockInstance(obj_id):
                rhino_to_stp(rs.BlockObjects(rs.BlockInstanceName(obj_id)))
                convert_block(obj_id)


def convert_part(obj_id, local_objs):
    engraving_id = get_engravings(obj_id, local_objs)
    if engraving_id:
        # bb_points = rs.BoundingBox(obj_id, rs.TextObjectPlane(engraving_id))
        thread_ids = get_threads(obj_id, local_objs)
        # other_text_ids = get_other_texts(bb_points, local_objs)
        # remove engraving_id in other text
        # try:
        #     other_text_ids.remove(engraving_id)
        # except ValueError:
        #     pass

        copy_obj_id = rs.CopyObject(obj_id)
        copy_thread_ids = rs.CopyObjects(thread_ids)
        copy_engraving_id = rs.CopyObject(engraving_id)
        # copy_oth_txt_ids = rs.CopyObjects(other_text_ids)

        ids_to_export = []
        ids_to_export.extend([copy_obj_id])
        ids_to_export.extend(copy_thread_ids)

        # unmirror all text objects if they are mirrored.
        if IS_TEXT_MIRROR:
            unmirror(copy_engraving_id)
            # for other_text_id in copy_oth_txt_ids:
            #     unmirror(other_text_id)

        text_objs = [copy_engraving_id]
        # text_objs.extend(copy_oth_txt_ids)

        # transform plane
        xform_plane = rg.Transform.PlaneToPlane(rs.TextObjectPlane(copy_engraving_id), rs.WorldXYPlane())
        rs.TransformObjects(ids_to_export, xform_plane)
        rs.TransformObjects(text_objs, xform_plane)

        # make the XAxis point to the right and make the YAxis point up
        while round(rs.TextObjectPlane(copy_engraving_id).XAxis[0], PRECISION) <= 0 and \
                round(rs.TextObjectPlane(copy_engraving_id).YAxis[1], PRECISION) <= 0:
            rs.RotateObjects(ids_to_export, rs.WorldXYPlane().Origin, 90, rs.WorldXYPlane().Normal)
            rs.RotateObjects(text_objs, rs.WorldXYPlane().Origin, 90, rs.WorldXYPlane().Normal)

        # explode all text objects before converting to STP
        for text_id in text_objs:
            exploded = rs.ExplodeText(text_id)
            ids_to_export.extend(exploded)

        filename = "{}_00.stp".format(get_specific_part_name(obj_id))
        full_path = os.path.join(STP_FOLDER, filename)
        export_to_stp(full_path, ids_to_export)
        rs.DeleteObjects(ids_to_export)
        rs.DeleteObjects(text_objs)
    else:
        print("Cannot find engraving for {}".format(get_specific_part_name(obj_id)))


def convert_block(block_id):
    copy_block_id = rs.CopyObject(block_id)
    obj_ref = None
    # find the reference object
    for obj_id in rs.BlockObjects(rs.BlockInstanceName(copy_block_id)):
        part_name = get_specific_part_name(obj_id)
        if part_name.startswith("1421") and rs.IsPolysurface(obj_id):
            if "TC" in part_name:
                obj_ref = obj_id
                break
    # get the engraving object for reference.
    engraving_id = get_engravings(obj_ref, rs.BlockObjects(rs.BlockInstanceName(copy_block_id)))
    if engraving_id:
        # transform plane
        xform_plane = rg.Transform.PlaneToPlane(rs.TextObjectPlane(engraving_id), rs.WorldXYPlane())
        rs.TransformObject(copy_block_id, xform_plane)
        copy_engraving_id = rs.TransformObject(engraving_id, xform_plane, copy=True)
        # make the XAxis point to the right and make the YAxis point up
        while round(rs.TextObjectPlane(copy_engraving_id).XAxis[0], PRECISION) <= 0 and \
                round(rs.TextObjectPlane(copy_engraving_id).YAxis[1], PRECISION) <= 0:
            rs.RotateObjects(copy_block_id, rs.WorldXYPlane().Origin, 90, rs.WorldXYPlane().Normal)

        # we need to explode the block instance
        ids_to_export = []
        block_objs = rs.ExplodeBlockInstance(copy_block_id)
        for block_obj in block_objs:
            if rs.IsText(block_obj):
                # need to explode all the text objects inside the block.
                curves = rs.ExplodeText(block_obj)
                ids_to_export.extend(curves)
            else:
                ids_to_export.append(block_obj)

        filename = "{}_00.stp".format(get_specific_part_name(block_id))
        full_path = os.path.join(STP_FOLDER, filename)
        export_to_stp(full_path, ids_to_export)
        rs.DeleteObjects(ids_to_export)
        rs.DeleteObject(copy_engraving_id)
    else:
        print("Cannot find engraving for {}".format(get_specific_part_name(obj_ref)))


def main():
    reset_rhino_view()
    global HOLOPLOT_NUM
    global IS_TEXT_MIRROR
    global STP_FOLDER

    HOLOPLOT_NUM = rs.GetString("Holoplot Number")
    STP_FOLDER = rs.BrowseForFolder(message="Select folder to save STP files")
    items = (("MirrorTexts", "No", "Yes"),)
    result = rs.GetBoolean("Options", items, (False,))
    IS_TEXT_MIRROR = result[0]
    sel_obj_ids = rs.GetObjects("Select parts to export stp")
    rhino_to_stp(sel_obj_ids)
    rs.MessageBox("STP Done")


if __name__ == "__main__":
    main()
