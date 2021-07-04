import os
import argparse
import array
from FabAuto.src.util.constants import Constants
from FabAuto.src.controller.bricscad_controller import BricscadController
from FabAuto.src.controller.inventor_controller import InventorController


def iter_input():
    """
    iterates over the input folder
    :return:
    """
    for dir_path, dir_names, file_names in os.walk(Constants.INPUT_DIR):
        for file_name in file_names:
            if file_name.endswith(".ipt"):
                yield os.path.join(dir_path, file_name)


def extract_2d_views(inventor_ctrl, view_list, model_file_path):
    """
    This function "extracts" the views from the IPT model. then saves a DWG file containing the 2D views of the model.
    :param view_list:
    :param model_file_path:
    """
    part_doc = inventor_ctrl.create_part_document(model_file_path)
    drawing_doc = inventor_ctrl.create_drawing_document()

    x = 15
    y = 30
    for view_name in view_list:
        view = inventor_ctrl.create_view(part_doc, drawing_doc, view_name, x, y)
        # for the sake of separation
        x = x + view.width

    dwg_filename = "{}.dwg".format(os.path.basename(model_file_path).split(".")[0])
    dwg_full = os.path.join(Constants.OUTPUT_DIR, dwg_filename)
    inventor_ctrl.save_drawing_as_dwg(drawing_doc, dwg_full)
    inventor_ctrl.close_document(drawing_doc)
    inventor_ctrl.close_document(part_doc)
    return dwg_full


def convert_acid_to_block_refs(dwg_document):
    """
    Explodes ACIDBLOCKREFERENCES to BLOCKREFERENCES resulted from Inventory DWG generation
    :param dwg_document:
    :return:
    """
    modelspace = dwg_document.ModelSpace
    for ent in modelspace:
        if ent.ObjectName.lower() == "acidblockreference":
            ent.explode()
            ent.Delete()


def relayout_block_reference(bricscad_controller, dwg_document):
    modelspace = dwg_document.ModelSpace
    point1 = array.array("d", [0, 0, 0])
    point2 = array.array("d", [0, 0, 0])
    for ent in modelspace:
        if ent.ObjectName.lower() == "acdbblockreference":
            max_point, min_point = bricscad_controller.get_bounding_box(ent)
            width = abs(max_point[0] - min_point[0])
            ent.Move(point1, point2)
            point2[0] += width * 1.5


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v",
                        type=str,
                        choices=["top",
                                 "bottom",
                                 "left",
                                 "right",
                                 "front",
                                 "back",
                                 "bottom_left",
                                 "bottom_right",
                                 "top_left",
                                 "top_right"],
                        nargs="+")
    parser.add_argument("-tb",
                        type=str)
    args = parser.parse_args()
    tb_path = None
    if args.tb:
        tb_path = args.tb
    view_list = args.v
    inventor_ctrl = InventorController()
    bricscad_ctrl = BricscadController()
    for model_file_path in iter_input():
        # extracts 2d views from model and save as dwg file
        dwg_fp = extract_2d_views(inventor_ctrl, view_list, model_file_path)
        dwg_document = bricscad_ctrl.open_dwg_file(dwg_fp)
        # convert inventor block reference to autocad blockreference
        convert_acid_to_block_refs(dwg_document)
        # relayout block references to look nicer
        relayout_block_reference(bricscad_ctrl, dwg_document)
        bricscad_ctrl.zoom_extents()
        # create a new layout for the 2d views
        # automatically creates a viewport
        layout_name = os.path.basename(model_file_path).split(".")[0]
        bricscad_ctrl.add_layout(layout_name, tb_path)
        # delete the default layout
        bricscad_ctrl.delete_layout("Sheet")
        bricscad_ctrl.save_and_close()
    inventor_ctrl.quit_app()
    bricscad_ctrl.quit_app()
