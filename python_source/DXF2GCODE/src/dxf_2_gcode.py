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
            if ent.dxftype() == "LWPOLYLINE":
                for sub_ent in ent.virtual_entities():
                    yield sub_ent
            elif ent.dxftype() == "LINE":
                yield ent
            elif ent.dxftype() == "CIRCLE":
                yield ent
            elif ent.dxftype() == "ARC":
                yield ent

    def ent_2_gcode(self, ent):
        if ent.dxftype() == "LINE":
            pass
        elif ent.dxftype() == "CIRCLE":
            pass
        elif ent.dxftype() == "ARC":
            pass


