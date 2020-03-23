#!/usr/bin/env python

from math import tan
from math import degrees
from math import sqrt
from math import acos
from math import radians
from comtypes import client
from comtypes import COMError
from logger import Logger
from constants import Constants
from shutil import copyfile
import array
import os
import csv

logger = Logger()


class BracketGenerator:
    def __init__(self, file_name):
        self.file_name = file_name
        self.logger = logger.get_logger()

        try:
            self.cad_application = client.GetActiveObject(Constants.APP_NAME, dynamic=True)
            self.cad_application.Visible = True
        except(OSError, COMError):
            self.logger.info(f"{Constants.APP_NAME} is not Running...")
            self.logger.info(f"Opening {Constants.APP_NAME}...")
            self.cad_application = client.CreateObject(Constants.APP_NAME, dynamic=True)
            self.cad_application.Visible = True

    def calculate_increments(self, tile_len, num_variation):
        self.logger.info(f"Calculating data for tile length: {tile_len} with {num_variation} variations")
        opposite = Constants.MAX_OPENING - Constants.TOP_TO_PIVOTAL
        hypotenuse = tile_len
        adjacent = round(sqrt((hypotenuse ** 2) - (opposite ** 2)), 1)

        angle = round(degrees(acos((adjacent**2 + hypotenuse**2 - opposite**2)/(2.0 * adjacent * hypotenuse))), 2)
        tile_ang_inc = round(angle / (num_variation - 1), 2)
        tan_tile_ang_inc = tan(radians(tile_ang_inc))

        r_pivot_dist = Constants.FIR_BRACK_DIST
        r_brack_len_inc = round(tan_tile_ang_inc * r_pivot_dist, 1)

        l_pivot_dist = tile_len - Constants.FIR_BRACK_DIST
        l_brack_len_inc = round(tan_tile_ang_inc * l_pivot_dist, 1)

        return tile_ang_inc, r_brack_len_inc, l_brack_len_inc

    def create_table(self, doc, tile_len, num_variation):
        self.logger.info("Creating table...")
        ps_obj_collection = doc.PaperSpace
        insertion_pt = array.array("d", [332.8507, 284.8947, 0.0000])
        total_row = ((num_variation - 1) * 2) + 2
        total_col = 5
        tbl_obj = ps_obj_collection.AddTable(insertion_pt, total_row, total_col, 1, 10)
        tbl_obj.DeleteRows(0, 1)

        tbl_obj.SetCellValue(0, 0, "PART NO.")
        tbl_obj.SetCellValue(0, 1, "LENGTH")
        tbl_obj.SetCellValue(0, 2, "ANGLE")
        tbl_obj.SetCellValue(0, 3, "DIM A")
        tbl_obj.SetCellValue(0, 4, "QUANTITY")

        tile_angle_inc, r_brack_len_inc, l_brack_len_inc = self.calculate_increments(tile_len, num_variation)
        r_brack_len = Constants.R_BRACK_ORIG_LEN
        r_brack_ang = Constants.R_BRACK_ORIG_ANG
        l_brack_len = Constants.L_BRACK_ORIG_LEN
        l_brack_ang = Constants.L_BRACK_ORIG_ANG

        rows = tbl_obj.Rows
        cols = tbl_obj.Columns

        for row in range(1, rows):
            tbl_obj.SetCellValue(row, 0, f"AB{str(num_variation).zfill(2)}-{str(row).zfill(2)}")
            if row % 2 != 0:
                # right
                r_brack_len = round(r_brack_len + r_brack_len_inc, 1)
                r_brack_ang = round(r_brack_ang - tile_angle_inc, 2)
                tbl_obj.SetCellValue(row, 1, f"{str(r_brack_len)}")
                tbl_obj.SetCellValue(row, 2, f"{str(r_brack_ang)}\xb0")
            else:
                # left
                l_brack_len = round(l_brack_len + l_brack_len_inc, 1)
                l_brack_ang = round(l_brack_ang + tile_angle_inc, 2)
                tbl_obj.SetCellValue(row, 1, f"{str(l_brack_len)}")
                tbl_obj.SetCellValue(row, 2, f"{str(l_brack_ang)}\xb0")

        color_red = self.cad_application.GetInterfaceObject("BricscadDb.AcadAcCmColor")
        color_gray = self.cad_application.GetInterfaceObject("BricscadDb.AcadAcCmColor")
        color_black = self.cad_application.GetInterfaceObject("BricscadDb.AcadAcCmColor")
        color_gray.SetRGB(128, 128, 128)
        color_red.SetRGB(255, 0, 0)
        color_black.SetRGB(0, 0, 0)
        tbl_obj.SetContentColor(1, color_black)

        for row in range(0, rows):
            for col in range(0, cols):
                if row == 0:
                    tbl_obj.SetCellGridColor(row, col, Constants.LEFT_EDGE, color_red)
                    tbl_obj.SetCellGridColor(row, col, Constants.UPPER_RIGHT_LOWER_EDGE, color_red)
                else:
                    tbl_obj.SetCellGridColor(row, col, Constants.LEFT_EDGE, color_red)
                    tbl_obj.SetCellGridColor(row, col, Constants.RIGHT_EDGE, color_red)
                    tbl_obj.SetCellGridColor(row, col, Constants.LOWER_EDGE, color_gray)

                    if row == rows - 1:
                        tbl_obj.SetCellGridColor(row, col, Constants.LEFT_EDGE, color_red)
                        tbl_obj.SetCellGridColor(row, col, Constants.RIGHT_EDGE, color_red)
                        tbl_obj.SetCellGridColor(row, col, Constants.LOWER_EDGE, color_red)

                tbl_obj.SetCellTextHeight(row, col, 1.5)
                tbl_obj.SetCellTextHeight(row, col, 1.5)
                tbl_obj.SetCellTextHeight(row, col, 1.5)
                tbl_obj.SetCellTextHeight(row, col, 1.5)
                tbl_obj.SetCellTextHeight(row, col, 1.5)
                tbl_obj.SetColumnWidth(col, 17)
                tbl_obj.SetRowHeight(row, 5)

    def create_layout(self, doc_obj, file_name, tile_len, num_variation):
        self.logger.info("Creating layout...")
        layouts = doc_obj.Layouts
        layout_dict = self._put_in_dict(layouts)
        first_ps_layout = layout_dict[1]
        doc_obj.ActiveLayout = first_ps_layout
        first_ps_layout.Name = file_name
        self.create_table(doc_obj, tile_len, num_variation)

    def create_model_doc(self):
        self.logger.info("Creating Initial Document...")
        src = os.path.join(Constants.INPUT_DIR, self.file_name)
        dst = os.path.join(Constants.OUTPUT_DIR, "document_model.dwg")
        try:
            copyfile(src, dst)
        except FileExistsError as e:
            self.logger.error(e)

        doc_model_path = dst
        self.cad_application.Documents.Open(doc_model_path)
        document = self.cad_application.ActiveDocument

        for ps_obj in document.PaperSpace:
            if ps_obj.ObjectName == "AcDbMText" and\
                    ps_obj.TrueColor.Red == 255 and\
                    ps_obj.TrueColor.Green == 255 and\
                    ps_obj.TrueColor.Green == 255:
                ps_obj.Delete()

            elif ps_obj.ObjectName == "AcDbMText" and \
                    (ps_obj.TextString == "PART NO." or
                    ps_obj.TextString == "LENGTH" or
                    ps_obj.TextString == "ANGLE" or
                    ps_obj.TextString == "DIM A" or
                    ps_obj.TextString == "QUANTITY"):
                ps_obj.Delete()

            elif (ps_obj.ObjectName == "AcDbPolyline" or ps_obj.ObjectName == "AcDbLine") and \
                    ps_obj.Layer == "0":
                ps_obj.Delete()

        self.save_document(document, "document_model.dwg")

    def copy_file(self, file_name):
        src = os.path.join(Constants.OUTPUT_DIR, "document_model.dwg")
        dst = os.path.join(Constants.OUTPUT_DIR, file_name+".dwg")

        try:
            copyfile(src, dst)
        except FileExistsError as e:
            self.logger.error(e)

    def create_doc(self, file_name):
        self.logger.info("Creating document...")
        file = os.path.join(Constants.OUTPUT_DIR, file_name)
        self.cad_application.Documents.Open(file)
        new_doc = self.cad_application.ActiveDocument
        return new_doc

    def save_document(self, document, file_name):
        self.logger.info(f"Saving document {file_name}")
        if not document.Saved:
            self.logger.info("There are unsaved changes in the Drawing")
            self.__zoom_extends_first_layout(document)
            document.Save()
            self.cad_application.Documents.Close()
        self.logger.info("Saving done and Closed...")

    def __zoom_extends_first_layout(self, document):
        self.logger.info("Applying zoom extents...")
        layouts = document.Layouts
        layout_dict = self._put_in_dict(layouts)
        for tab_order, layout in sorted(layout_dict.items()):
            document.ActiveLayout = layout
            self.cad_application.ZoomExtents()
            document.SetVariable("TREEDEPTH", document.GetVariable("TREEDEPTH"))
            # command_str = "._ZOOM\nextents\n"
            # document.SendCommand(command_str)

    def clean_up_files(self):
        self.logger.info("Cleaning up files...")
        for dir_path, dir_names, file_names in os.walk(Constants.OUTPUT_DIR):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(Constants.BAK_FILES):
                    os.remove(os.path.join(dir_path, file_name))

    @staticmethod
    def _put_in_dict(layouts):
        layout_dict = {}

        for layout in layouts:
            key = layout.TabOrder
            layout_dict[key] = layout

        return layout_dict

    def begin_automation(self):
        self.logger.info("Starting script...")
        self.create_model_doc()
        in_data = os.path.join(Constants.INPUT_DIR, "tile_variations_test.csv")
        with open(in_data, 'r') as in_file:
            reader = csv.reader(in_file)
            next(in_file)
            for entry in reader:
                num = entry[0]
                tile_len = int(entry[1])
                num_variation = int(entry[2])
                file_name = f"{num}-{str(tile_len)}-{str(num_variation)}"
                self.copy_file(file_name)
                doc_obj = self.create_doc(file_name)
                self.create_layout(doc_obj,
                                   file_name,
                                   tile_len,
                                   num_variation)
                self.save_document(doc_obj, file_name+".dwg")
        self.clean_up_files()
        self.logger.info("Script done executing...")


if __name__ == "__main__":
    file_name = "1808-933_REV A.dwg"
    pp_gen = BracketGenerator(file_name)
    pp_gen.begin_automation()
