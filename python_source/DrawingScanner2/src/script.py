import os
import csv
from openpyxl import Workbook
import ezdxf
import ezdxf.math
from ezdxf.tools.rgb import DXF_DEFAULT_COLORS, int2rgb
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
        output_dir = os.path.join(Constants.OUTPUT_DIR, filename + '.xlsx')
        ms = dxf_file.modelspace()
        ins_unit_num = dxf_file.header["$INSUNITS"]
        unit = Constants.INS_UNITS[ins_unit_num]
        fieldnames = ['RGBColor', f'Width ({unit})', f'Height ({unit})', 'Count']

        workbook = Workbook()
        for ent in ms:
            print("type:", ent.dxftype(), "handle:", ent.dxf.handle)
            if ent.dxftype() == "INSERT":
                ent_list = []
                handle = ent.dxf.handle
                worksheet = workbook.create_sheet(f"BlockReference #{handle}")
                worksheet.append(fieldnames)

                for blk_ent in ent.virtual_entities():
                    type = blk_ent.dxftype()
                    if type == "LWPOLYLINE" or type == "POLYLINE":
                        found = False
                        count = 1
                        ent_points = blk_ent.get_points('xy')
                        bbox = ezdxf.math.BoundingBox2d(ent_points)
                        extmin = bbox.extmin
                        extmax = bbox.extmax

                        xmax, ymax = extmax
                        xmin, ymin = extmin

                        w = round(xmax - xmin, 2)
                        h = round(ymax - ymin, 2)

                        ent_aci = blk_ent.dxf.color
                        ent_color_hex = DXF_DEFAULT_COLORS[ent_aci]
                        ent_color_rgb = int2rgb(ent_color_hex)
                        ent_color_rgb_str = f"({ent_color_rgb[0]}, {ent_color_rgb[1]}, {ent_color_rgb[2]})"

                        for ent_member in ent_list:
                            if ent_member['A'] == ent_color_rgb_str and ent_member['C'] == h:
                                ent_member['D'] += 1
                                found = True

                        if not found:
                            ent_prop_dict = {
                                'A': ent_color_rgb_str,
                                'B': w,
                                'C': h,
                                'D': count
                            }
                            ent_list.append(ent_prop_dict)
                        print(f"type: {type}, ACI: {ent_aci} hex color: #{ent_color_hex :06X} "
                              f"rgb color: {ent_color_rgb}")
                print(" ")
                for ent_prop in ent_list:
                    worksheet.append(ent_prop)
        workbook.save(output_dir)
