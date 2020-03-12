#!/usr/bin/env python

from math import tan
from math import degrees
from math import sqrt
from math import acos
from math import radians
from comtypes import client
from comtypes import COMError
from logger import Logger
import array
import os
import csv

MAX_OPENING = 354.0
TOP_TO_PIVOTAL = 92.0
FIR_BRACK_DIST = 169.6

R_BRACK_ORIG_ANG = 90.0
R_BRACK_ORIG_LEN = 50.0
L_BRACK_ORIG_ANG = 90.0
L_BRACK_ORIG_LEN = 50.0

BRICSCAD_APP_NAME = "BricscadApp.AcadApplication"
AUTOCAD_APP_NAME = "AutoCAD.Application"
APP_NAME = BRICSCAD_APP_NAME  # switch to other app CAD here.

logger = Logger()
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJ_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJ_ROOT, "output")
INPUT_DIR = os.path.join(PROJ_ROOT, "input")


class PayPayGenerator:
    def __init__(self, file_name):
        self.file_name = file_name
        self.logger = logger.get_logger()

        try:
            self.cad_application = client.GetActiveObject(APP_NAME, dynamic=True)
            self.cad_application.Visible = True
        except(OSError, COMError):
            self.logger.info(f"{APP_NAME} is not Running...")
            self.logger.info(f"Opening {APP_NAME}...")
            self.cad_application = client.CreateObject(APP_NAME, dynamic=True)
            self.cad_application.Visible = True

    @staticmethod
    def calculate_increments(tile_len, num_variation):
        opposite = MAX_OPENING - TOP_TO_PIVOTAL
        hypotenuse = tile_len
        adjacent = round(sqrt((hypotenuse ** 2) - (opposite ** 2)), 1)

        angle = round(degrees(acos((adjacent**2 + hypotenuse**2 - opposite**2)/(2.0 * adjacent * hypotenuse))), 2)
        tile_ang_inc = round(angle / (num_variation - 1), 2)
        tan_tile_ang_inc = tan(radians(tile_ang_inc))

        r_pivot_dist = FIR_BRACK_DIST
        r_brack_len_inc = round(tan_tile_ang_inc * r_pivot_dist, 1)

        l_pivot_dist = tile_len - FIR_BRACK_DIST
        l_brack_len_inc = round(tan_tile_ang_inc * l_pivot_dist, 1)

        return tile_ang_inc, r_brack_len_inc, l_brack_len_inc

    def create_table(self, doc, tile_len, num_variation):
        ps_obj_collection = doc.PaperSpace
        insertion_pt = array.array("d", [1.60, 6.95, 0])
        total_row = ((num_variation - 1) * 2) + 2
        total_col = 3
        tbl_obj = ps_obj_collection.AddTable(insertion_pt, total_row, total_col, 0.0025, 2.5)
        tbl_obj.DeleteRows(0, 1)

        tbl_obj.SetCellValue(0, 0, "PART NO.")
        tbl_obj.SetCellValue(0, 1, "LENGTH")
        tbl_obj.SetCellValue(0, 2, "ANGLE")

        tile_angle_inc, r_brack_len_inc, l_brack_len_inc = self.calculate_increments(tile_len, num_variation)
        r_brack_len = R_BRACK_ORIG_LEN
        r_brack_ang = R_BRACK_ORIG_ANG
        l_brack_len = L_BRACK_ORIG_LEN
        l_brack_ang = L_BRACK_ORIG_ANG

        rows = tbl_obj.Rows
        for irow in range(1, rows):
            tbl_obj.SetCellTextHeight(irow, 0, 0.10)
            tbl_obj.SetCellTextHeight(irow, 1, 0.10)
            tbl_obj.SetCellTextHeight(irow, 2, 0.10)

            tbl_obj.SetCellValue(irow, 0, f"AB{str(num_variation).zfill(2)}-{str(irow).zfill(2)}")
            if irow % 2 != 0:
                # right
                r_brack_len = round(r_brack_len + r_brack_len_inc, 1)
                r_brack_ang = round(r_brack_ang - tile_angle_inc, 2)
                tbl_obj.SetCellValue(irow, 1, f"{str(r_brack_len)}")
                tbl_obj.SetCellValue(irow, 2, f"{str(r_brack_ang)}\xb0")
            else:
                # left
                l_brack_len = round(l_brack_len + l_brack_len_inc, 1)
                l_brack_ang = round(l_brack_ang + tile_angle_inc, 2)
                tbl_obj.SetCellValue(irow, 1, f"{str(l_brack_len)}")
                tbl_obj.SetCellValue(irow, 2, f"{str(l_brack_ang)}\xb0")
            tbl_obj.SetRowHeight(irow, 0.10)

    def create_layout(self, doc_obj):
        layouts = doc_obj.Layouts
        in_data = os.path.join(INPUT_DIR, "tile_variations.csv")
        with open(in_data, 'r') as in_file:
            reader = csv.reader(in_file)
            next(in_file)
            for entry in reader:
                num = entry[0]
                tile_len = int(entry[1])
                num_variation = int(entry[2])
                layout = layouts.Add(f"{num}-{str(tile_len)}-{str(num_variation)}")
                doc_obj.ActiveLayout = layout
                self.create_table(doc_obj, tile_len, num_variation)

    def create_doc(self):
        new_doc = self.cad_application.Documents.Add()
        return new_doc

    def save_document(self, document, file_name):
        self.logger.info("Saving changes to Drawing: {}".format(file_name))
        full_path_save = os.path.join(OUTPUT_DIR, file_name)
        if not document.Saved:
            self.logger.info("There are unsaved changes in the Drawing")
            document.SaveAs(full_path_save)
            self.cad_application.Documents.Close()
        self.logger.info("Saving done and Closed...")

    def delete_layouts(self, document):
        layouts = document.Layouts
        layout_dict = self._put_in_dict(layouts)
        layout_dict[1].Delete()
        layout_dict[2].Delete()
        document.ActiveLayout = layout_dict[1]

    @staticmethod
    def _put_in_dict(layouts):
        layout_dict = {}

        for layout in layouts:
            key = layout.TabOrder
            layout_dict[key] = layout

        return layout_dict

    def begin_automation(self):
        doc_obj = self.create_doc()
        self.create_layout(doc_obj)
        self.delete_layouts(doc_obj)
        self.save_document(doc_obj, self.file_name)


if __name__ == "__main__":
    file_name = "1808-933_many.dwg"
    pp_gen = PayPayGenerator(file_name)
    pp_gen.begin_automation()
