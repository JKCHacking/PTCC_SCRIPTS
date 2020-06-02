#!/usr/bin/env python
import os
from comtypes import client
from comtypes import COMError
from src.constants import Constants
from src.logger import Logger
from shutil import copyfile
import array
import math
import csv

logger = Logger()


class TowerMeasurer:
    def __init__(self):
        self.logger = logger.get_logger()
        self.color_red_panels = 0
        self.color_orange_panels = 0
        self.color_yellow_panels = 0
        self.color_yellow_green_panels = 0
        self.color_green_panels = 0
        self.color_blue_panels = 0
        self.color_violet_panels = 0
        try:
            self.cad_application = client.GetActiveObject(Constants.APP_NAME, dynamic=True)
            self.cad_application.Visible = True
        except(OSError, COMError):
            self.logger.info(f"{Constants.APP_NAME} is not Running...")
            self.logger.info(f"Opening {Constants.APP_NAME}...")
            self.cad_application = client.CreateObject(Constants.APP_NAME, dynamic=True)
            self.cad_application.Visible = True

    def get_cold_bent(self, document):
        self.logger.info(f"Getting Cold Bent...")
        self.cad_application.ZoomExtents()
        self.cad_application.ActiveDocument = document

        command_str = f"_explode all\n\n"
        document.SendCommand(command_str)

        panel_vertices = self.get_spline_vertices(document)
        pt1 = array.array('d', panel_vertices[0:3])
        pt2 = array.array('d', panel_vertices[3:6])
        pt3 = array.array('d', panel_vertices[6:9])
        pt4 = array.array('d', panel_vertices[9:12])

        bottom_side = document.ModelSpace.AddLine(pt4, pt3)
        top_side = document.ModelSpace.AddLine(pt1, pt2)
        in_between_angle = abs(top_side.Angle - bottom_side.Angle)
        dist_top_side = self.get_distance_between_points(pt1, pt2)
        cold_bent = round(dist_top_side * math.sin(in_between_angle), 4)

        return cold_bent

    def get_length_width(self, document):
        panel_vertices = self.get_spline_vertices(document)
        pt1 = array.array('d', panel_vertices[0:3])
        pt2 = array.array('d', panel_vertices[3:6])
        pt3 = array.array('d', panel_vertices[6:9])
        pt4 = array.array('d', panel_vertices[9:12])

        length1 = self.get_distance_between_points(pt1, pt4)
        length2 = self.get_distance_between_points(pt3, pt2)

        width1 = self.get_distance_between_points(pt1, pt2)
        width2 = self.get_distance_between_points(pt3, pt4)

        length = length1 if length1 <= length2 else length2
        width = width1 if width1 >= width2 else width2

        return length, width

    def write_csv(self, document):
        new_doc = self.cad_application.Documents.Add()
        output_csv = "cold_bent_panels.csv"
        data_list = []
        panel_count = 0
        if document:
            for obj in document.ModelSpace:
                self.logger.info(f"Handle: {obj.Handle}")
                if obj.ObjectName == "AcDbSurface" and obj.Layer == "TYPICAL CURTAIN WALL PANEL":
                    try:
                        document.CopyObjects(obj, new_doc.ModelSpace)
                    except COMError:
                        pass
                    cold_bent = self.get_cold_bent(new_doc)
                    length, width = self.get_length_width(new_doc)
                    color_str = self.set_object_color(obj, cold_bent)
                    handle = f'"{obj.Handle}"'
                    data_list.append({"Handle": handle, "Length": length, "Width": width, "ColdBent": cold_bent,
                                      "Color": color_str})

                    self.logger.info(f"Cold Bent: {cold_bent}")
                    self.delete_all_objects(new_doc)
                    panel_count = panel_count + 1
                    self.logger.info(f"Computed panels: {panel_count}")

            try:
                self.logger.info("Writing to CSV File...")
                with open(os.path.join(Constants.OUTPUT_DIR, output_csv), mode='w') as csvfile:
                    field_names = ['Handle', 'Length', 'Width', 'ColdBent', 'Color']
                    csv_writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    csv_writer.writeheader()
                    for data in data_list:
                        csv_writer.writerow(data)
                csvfile.close()
            except IOError:
                self.logger.error(IOError.strerror)

            self.save_document(document)
            self.copy_file()
            self.clean_up_files()
            self.logger.info(f'color_red_panels: {self.color_red_panels}')
            self.logger.info(f'color_orange_panels: {self.color_orange_panels}')
            self.logger.info(f'color_yellow_panels: {self.color_yellow_panels}')
            self.logger.info(f'color_yellow_green_panels: {self.color_yellow_green_panels}')
            self.logger.info(f'color_green_panels: {self.color_green_panels}')
            self.logger.info(f'color_blue_panels: {self.color_blue_panels}')
            self.logger.info(f'color_violet_panels: {self.color_violet_panels}')

    def set_object_color(self, obj, cold_bent):
        color_red = self.cad_application.GetInterfaceObject("BricscadDb.AcadAcCmColor")
        color_orange = self.cad_application.GetInterfaceObject("BricscadDb.AcadAcCmColor")
        color_yellow = self.cad_application.GetInterfaceObject("BricscadDb.AcadAcCmColor")
        color_yellow_green = self.cad_application.GetInterfaceObject("BricscadDb.AcadAcCmColor")
        color_green = self.cad_application.GetInterfaceObject("BricscadDb.AcadAcCmColor")
        color_blue = self.cad_application.GetInterfaceObject("BricscadDb.AcadAcCmColor")
        color_violet = self.cad_application.GetInterfaceObject("BricscadDb.AcadAcCmColor")

        color_red.SetRGB(255, 0, 0)
        color_orange.SetRGB(255, 165, 0)
        color_yellow.SetRGB(255, 255, 0)
        color_yellow_green.SetRGB(60, 80, 20)
        color_green.SetRGB(0, 128, 0)
        color_blue.SetRGB(0, 0, 255)
        color_violet.SetRGB(238, 130, 238)

        color_string = ''

        if 60 <= cold_bent < 70:
            obj.TrueColor = color_red
            self.color_red_panels += 1
            color_string = 'Red'
        elif 50 <= cold_bent < 60:
            obj.TrueColor = color_orange
            self.color_orange_panels += 1
            color_string = 'Magenta'
        elif 40 <= cold_bent < 50:
            obj.TrueColor = color_yellow
            self.color_yellow_panels += 1
            color_string = 'Yellow'
        elif 30 <= cold_bent < 40:
            obj.TrueColor = color_yellow_green
            self.color_yellow_green_panels += 1
            color_string = 'Yellow Green'
        elif 20 <= cold_bent < 30:
            obj.TrueColor = color_green
            self.color_green_panels += 1
            color_string = 'Green'
        elif 10 <= cold_bent < 20:
            obj.TrueColor = color_blue
            self.color_blue_panels += 1
            color_string = 'Blue'
        elif 0 <= cold_bent < 10:
            obj.TrueColor = color_violet
            self.color_violet_panels += 1
            color_string = 'Pink'

        return color_string
    @staticmethod
    def get_distance_between_points(pt1, pt2):
        distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(pt1, pt2)]))
        return round(distance, 4)

    def open_file(self, drawing_full_path):
        self.logger.info(f"Opening File: {drawing_full_path}")

        document = None
        if os.path.exists(drawing_full_path):
            try:
                self.cad_application.Documents.Open(drawing_full_path)
                document = self.cad_application.ActiveDocument
            except COMError:
                self.logger.error("[ERROR]Invalid Drawing File!: {}".format(drawing_full_path))
        return document

    @staticmethod
    def delete_all_objects(document):
        for obj in document.ModelSpace:
            obj.Delete()

    @staticmethod
    def get_spline_vertices(document):
        panel_vertices = []
        count = 0
        for spline in document.ModelSpace:
            if spline.ObjectName == "AcDbSpline":
                if count % 2 != 0:
                    start_end_points = spline.ControlPoints
                    if len(start_end_points) == 6:
                        panel_vertices = panel_vertices + list(start_end_points)
                count = count + 1

        for index, vertices in enumerate(panel_vertices):
            panel_vertices[index] = round(vertices, 4)
        return panel_vertices

    def save_document(self, document):
        self.logger.info(f"Saving document input.dwg")
        if not document.Saved:
            self.logger.info("There are unsaved changes in the Drawing")
            document.Save()
            self.cad_application.Documents.Close()
        self.logger.info("Saving done and Closed...")

    def copy_file(self):
        src = os.path.join(Constants.INPUT_DIR, "input.dwg")
        dst = os.path.join(Constants.OUTPUT_DIR, "output.dwg")

        try:
            copyfile(src, dst)
        except FileExistsError as e:
            self.logger.error(e)

    def clean_up_files(self):
        self.logger.info("Cleaning up files...")
        for dir_path, dir_names, file_names in os.walk(Constants.OUTPUT_DIR):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(Constants.BAK_FILES):
                    os.remove(os.path.join(dir_path, file_name))


if __name__ == "__main__":
    tm_object = TowerMeasurer()
    # open drawing
    drw_fname = "input.dwg"
    drw_path = os.path.join(Constants.INPUT_DIR, drw_fname)
    document = tm_object.open_file(drw_path)
    tm_object.write_csv(document)
