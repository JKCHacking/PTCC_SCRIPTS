import ezdxf
import ezdxf.math
from src.util.constants import Constants


class CadManager:
    def __init__(self, cad_file_name):
        self.doc = ezdxf.readfile(cad_file_name)
        ins_unit_num = self.doc.header["$INSUNITS"]
        self.unit = Constants.INS_UNITS[ins_unit_num]

    def get_modelspace(self):
        modelspace = self.doc.modelspace()
        return modelspace

    def get_paperspace(self):
        layout_list = self.doc.layout_names_in_taborder()
        for layout_name in layout_list:
            if layout_name != "Model":
                yield self.doc.layout(layout_name)

    def get_mtext(self, space):
        for ent in space:
            if ent.dxftype() == "MTEXT":
                yield ent

    def get_blockreference(self, space):
        for ent in space:
            if ent.dxftype() == "INSERT":
                yield ent

    def get_polylines(self, space):
        for ent in space:
            if ent.dxftype() == "LWPOLYLINE":
                yield ent
