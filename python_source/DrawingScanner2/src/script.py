import ezdxf
import ezdxf.math
import os
import csv
from src.util.constants import Constants


class Script:
    """
        Gets all polylines from a dxf file and records the handle, width, and height of each polyline.
    """
    def iter_input(self):
        input_dir = Constants.INPUT_DIR
        for dir_path, dir_names, file_names in os.walk(input_dir):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(Constants.DXF_FILE_EXT):
                    self.create_output(file_full_path)

    def create_output(self, filename_fp):
        dxf_file = ezdxf.readfile(filename_fp)
        filename_ext = os.path.basename(filename_fp)
        filename = os.path.splitext(filename_ext)[0]
        output_dir = os.path.join(Constants.OUTPUT_DIR, filename + '.csv')
        ms = dxf_file.modelspace()
        fieldnames = ['handle', 'width', 'height']

        with open(output_dir, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for ent in ms:
                if ent.dxftype() == "LWPOLYLINE" or ent.dxftype() == "POLYLINE":
                    ent_points = ent.get_points('xy')
                    bbox = ezdxf.math.BoundingBox2d(ent_points)
                    extmin = bbox.extmin
                    extmax = bbox.extmax

                    xmax, ymax = extmax
                    xmin, ymin = extmin

                    w = xmax - xmin
                    h = ymax - ymin
                    handle = ent.dxf.handle

                    row_dict = {"handle": handle, 'width': w, 'height': h}
                    writer.writerow(row_dict)
