import os
import ezdxf
from src.util.constants import Constants


class DXF2Gcode:
    def iter_input(self):
        for dir_path, dir_names, file_names in os.walk(Constants.INPUT_DIR):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(Constants.DXF_FILE_EXT):
                    yield file_full_path

    def read_dxf(self, file):
        dxf_file = ezdxf.readfile(file)
        mod_space = dxf_file.modelspace()
        for ent in mod_space:
            yield ent

    def compose_gcode(self, ent):
        if ent.dxftype() == "LWPOLYLINE":
            pass


