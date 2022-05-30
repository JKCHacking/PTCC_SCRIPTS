import ctypes
import array
from comtypes import automation
from src.document.document import Document


class CadDocument(Document):
    def __init__(self, document):
        self.document = document

    def get_layouts(self):
        return self.document.Layouts

    def get_document_fp(self):
        return self.document.FullName

    def get_modelspace(self):
        return self.document.ModelSpace

    def close(self):
        self.document.Close(False)

    def get_bounding_box(self, entity):
        min_point = automation.VARIANT(array.array('d', [0, 0, 0]))
        max_point = automation.VARIANT(array.array('d', [0, 0, 0]))
        ref_min_point = ctypes.byref(min_point)
        ref_max_point = ctypes.byref(max_point)
        entity.GetBoundingBox(ref_min_point, ref_max_point)
        min_point = min_point.value
        max_point = max_point.value

        return min_point, max_point

    def add_line(self, start_point, end_point):
        return self.document.ModelSpace.AddLine(start_point, end_point)
