import os
from src.dxf_2_gcode import DXF2Gcode
from src.util.constants import Constants


def iter_input():
    for dir_path, dir_names, file_names in os.walk(Constants.INPUT_DIR):
        for file_name in file_names:
            file_full_path = os.path.join(dir_path, file_name)
            if file_full_path.endswith(Constants.DXF_FILE_EXT):
                yield file_full_path


if __name__ == "__main__":
    for file in iter_input():
        filename = os.path.splitext(os.path.basename(file))[0]
        gcode_file = os.path.join(Constants.OUTPUT_DIR, filename + Constants.TXT_FILE_EXT)
        script = DXF2Gcode(gcode_file)
        gcode = ""
        for ent in script.read_dxf(file):
            gcode += script.ent_2_gcode(ent)
        script.write_gcode(gcode)
