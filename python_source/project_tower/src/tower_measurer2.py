import os
import csv
import numpy as np
from comtypes import client
from comtypes import COMError
from src.constants import Constants

ROUND_PRECISION = 4


class Script:
    def __init__(self):
        try:
            self.cad_application = client.GetActiveObject(Constants.APP_NAME, dynamic=True)
            self.cad_application.Visible = True
        except(OSError, COMError):
            self.cad_application = client.CreateObject(Constants.APP_NAME, dynamic=True)
            self.cad_application.Visible = True
        self.document = None

    def open_document(self, dwg_path):
        self.cad_application.Documents.Open(dwg_path)
        self.document = self.cad_application.ActiveDocument

    def get_unit_document(self):
        unit_dict = {
            0: "Unspecified(No units)",
            1: "Inches",
            2: "Feet",
            3: "Miles",
            4: "Millimeters",
            5: "Centimeters",
            6: "Meters",
            7: "Kilometers",
            8: "Microinches",
            9: "Mils",
            10: "Yards",
            11: "Angstroms",
            12: "Nanometers",
            13: "Microns",
            14: "Decimeters",
            15: "Dekameters",
            16: "Hectometers",
            17: "Gigameters",
            18: "Astronomical Units",
            19: "Light Years",
        }

        unit_num = self.document.GetVariable("INSUNITS")
        try:
            unit_name = unit_dict[unit_num]
        except KeyError:
            unit_name = unit_dict[0]
            print("Unsupported Unit number")
        return unit_name

    def __get_required_entities(self, object_name):
        entities = []
        modelspace = self.document.ModelSpace
        for obj in modelspace:
            if obj.ObjectName == object_name:
                entities.append(obj)
        return entities

    def get_total_area(self):
        total_area = 0
        panels = self.__get_required_entities("AcDb3dSolid")
        num_panels = len(panels)
        print("Number of Panels in the Drawing: {}".format(num_panels))
        self.__print_progress_bar(0, num_panels, prefix="Progress", suffix="Completed", length=50)
        for i, obj1 in enumerate(panels):
            self.document.StartUndoMark()
            area_list = []
            # explode 3dsolid object using explode command
            self.document.SendCommand('explode (handent "{}")\n\n'.format(obj1.Handle))
            for obj2 in self.__get_required_entities("AcDbRegion"):
                # add this area in array_area
                area_list.append(round(obj2.Area, ROUND_PRECISION))
            for obj2 in self.__get_required_entities("AcDbSurface"):
                self.document.StartUndoMark()
                # explode surface using explode command
                self.document.SendCommand('explode (handent "{}")\n\n")'.format(obj2.Handle))
                spline_control_pts = []
                splines = self.__get_required_entities("AcDbSpline")
                for obj3 in splines:
                    # loop every spline object
                    ctrl_points = obj3.ControlPoints
                    pt1 = (round(ctrl_points[0], ROUND_PRECISION),
                           round(ctrl_points[1], ROUND_PRECISION),
                           round(ctrl_points[2], ROUND_PRECISION))

                    pt2 = (round(ctrl_points[3], ROUND_PRECISION),
                           round(ctrl_points[4], ROUND_PRECISION),
                           round(ctrl_points[5], ROUND_PRECISION))

                    # add control points in the list
                    if pt1 not in spline_control_pts:
                        spline_control_pts.append(pt1)
                    if pt2 not in spline_control_pts:
                        spline_control_pts.append(pt2)

                # get the area from the list of spline control points
                area = self.__poly_area(spline_control_pts)
                # add this area in area_array
                area_list.append(round(area, ROUND_PRECISION))
                self.document.EndUndoMark()
                # call undo command
                self.document.SendCommand("_undo\n\n")
            # sort in descending order
            area_list = sorted(area_list, reverse=True)
            # get the 2 highest area from area_array and
            # get average of the of two area
            ave_area = (area_list[0] + area_list[1])/2
            # add area in the total area
            total_area += ave_area
            self.document.EndUndoMark()
            # call undo command
            self.document.SendCommand("_undo\n\n")
            self.__print_progress_bar(i + 1, num_panels, prefix="Progress", suffix="Completed", length=50)
        return round(total_area, ROUND_PRECISION)

    def close_document(self):
        self.document.Close()

    def write_csv(self, dwg_file_name, total_surface_area, output_path):
        mode = "w"
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            mode = "a"

        with open(output_path, mode=mode, newline='') as csv_file:
            field_names = ["DWG File Name", "Total Surface Area"]
            csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
            if mode == "w":
                csv_writer.writeheader()
            csv_writer.writerow({"DWG File Name": dwg_file_name, "Total Surface Area": total_surface_area})

    def iter_input(self):
        for dir_path, dir_names, file_names in os.walk(Constants.INPUT_DIR):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(Constants.DWG_FILES) or file_full_path.endswith(Constants.DXF_FILES):
                    yield file_full_path

    def __print_progress_bar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        to_print = f'\r{prefix} |{bar}| ({iteration}/{total}) {percent}% {suffix}'
        print(to_print, end="", flush=True)
        # Print New Line on Complete
        if iteration == total:
            print()

    def __unit_normal(self, a, b, c):
        x = np.linalg.det([[1, a[1], a[2]],
                           [1, b[1], b[2]],
                           [1, c[1], c[2]]])
        y = np.linalg.det([[a[0], 1, a[2]],
                           [b[0], 1, b[2]],
                           [c[0], 1, c[2]]])
        z = np.linalg.det([[a[0], a[1], 1],
                           [b[0], b[1], 1],
                           [c[0], c[1], 1]])
        magnitude = (x ** 2 + y ** 2 + z ** 2) ** .5
        return x / magnitude, y / magnitude, z / magnitude

    def __poly_area(self, poly):
        if len(poly) < 3:  # not a plane - no area
            return 0
        total = [0, 0, 0]
        N = len(poly)
        for i in range(N):
            vi1 = poly[i]
            vi2 = poly[(i + 1) % N]
            prod = np.cross(vi1, vi2)
            total[0] += prod[0]
            total[1] += prod[1]
            total[2] += prod[2]
        result = np.dot(total, self.__unit_normal(poly[0], poly[1], poly[2]))
        return abs(result / 2)


def main():
    script = Script()
    output_file = os.path.join(Constants.OUTPUT_DIR, "output.csv")
    for dwg_file_path in script.iter_input():
        script.open_document(dwg_file_path)
        area = script.get_total_area()
        file_name = os.path.basename(dwg_file_path)
        script.write_csv(file_name, area, output_file)
        script.close_document()


if __name__ == "__main__":
    main()
