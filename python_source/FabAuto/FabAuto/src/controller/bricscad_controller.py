import array
import os
from FabAuto.src.app_creator import AppCreator
from comtypes import automation
from ctypes import byref


class BricscadController:
    def __init__(self):
        app_creator = AppCreator("BricscadApp.AcadApplication")
        self.bricscad_app = app_creator.get_app()
        self.bricscad_app.Visible = True
        self.dwg_document = None

    def open_dwg_file(self, dwg_fp):
        self.dwg_document = self.bricscad_app.Documents.Open(dwg_fp)
        return self.dwg_document

    def get_bounding_box(self, obj):
        max_point = automation.VARIANT(array.array('d', [0, 0, 0]))
        min_point = automation.VARIANT(array.array('d', [0, 0, 0]))

        ref_max_point = byref(max_point)
        ref_min_point = byref(min_point)

        obj.GetBoundingBox(ref_min_point, ref_max_point)

        max_point = max_point.value
        min_point = min_point.value

        return max_point, min_point

    def add_layout(self, layout_name, title_block_path):
        layout = self.dwg_document.Layouts.Add(layout_name)
        self.dwg_document.ActiveLayout = layout
        if title_block_path and os.path.exists(title_block_path):
            paperspace = self.dwg_document.PaperSpace
            # inserts the title block
            title_block = paperspace.InsertBlock(array.array("d", [0, 0, 0]), title_block_path, 1, 1, 1, 0, None)
        return layout

    def delete_layout(self, layout_name):
        layout = self.dwg_document.Layouts.Item(layout_name)
        layout.Delete()

    def save_and_close(self):
        self.dwg_document.Close(True)

    def quit_app(self):
        self.bricscad_app.Quit()

    def zoom_extents(self):
        self.dwg_document.ActiveLayout = self.dwg_document.Layouts.Item("Model")
        self.bricscad_app.ZoomExtents()
