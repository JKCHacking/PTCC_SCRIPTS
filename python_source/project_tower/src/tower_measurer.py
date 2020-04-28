#!/usr/bin/env python
import os
from comtypes import client
from comtypes import COMError
from constants import Constants
from logger import Logger
import array
import math
import csv

logger = Logger()


class TowerMeasurer:
    def __init__(self):
        self.logger = logger.get_logger()

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
                    data_list.append({"Handle": obj.Handle, "ColdBent": cold_bent})
                    self.logger.info(f"Cold Bent: {cold_bent}")
                    self.delete_all_objects(new_doc)
                    panel_count = panel_count + 1
                    self.logger.info(f"Computed panels: {panel_count}")

            try:
                self.logger.info("Writing to CSV File...")
                with open(os.path.join(Constants.OUTPUT_DIR, output_csv), mode='w') as csvfile:
                    field_names = ['Handle', 'ColdBent']
                    csv_writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    csv_writer.writeheader()
                    for data in data_list:
                        csv_writer.writerow(data)
                csvfile.close()
            except IOError:
                self.logger.error(IOError.strerror)

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


if __name__ == "__main__":
    tm_object = TowerMeasurer()
    # open drawing
    drw_fname = "input.dwg"
    drw_path = os.path.join(Constants.INPUT_DIR, drw_fname)
    document = tm_object.open_file(drw_path)
    tm_object.write_csv(document)
