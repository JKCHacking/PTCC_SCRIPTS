import os
import array
from comtypes import client
from comtypes import COMError
from comtypes import automation
from ctypes import byref


class ViewsExtractor:
    def __init__(self, output_dir, view_list):
        self.view_list = view_list
        self.output_dir = output_dir
        self.model_doc = None

        # initializing the Inventor application
        inv_progid = "Inventor.Application"
        try:
            self.inv_app = client.GetActiveObject(inv_progid, dynamic=True)
        except OSError:
            self.inv_app = client.CreateObject(inv_progid, dynamic=True)

        # initializing the Bricscad application
        bs_progid = "BricscadApp.AcadApplication"
        try:
            self.bs_app = client.GetActiveObject(bs_progid, dynamic=True)
        except OSError:
            self.bs_app = client.CreateObject(bs_progid, dynamic=True)

    def extract_views(self, model_path):
        # open the model file
        self.model_doc = self.inv_app.Documents.Open(model_path)
        drawing_doc = self.__create_drawing_doc()
        drawing_sheet = drawing_doc.Sheets.Item(1)
        # create 2d views from model and place on the drawing sheet.
        x = 0
        y = drawing_sheet.Height
        for view_name in self.view_list:
            view = self.__create_view(view_name, drawing_sheet, x, y)
            x = x + view.width
        # if the file is an assembly file we need to add part list table and balloons.
        if model_path.endswith(".iam"):
            # add partlist table
            border = drawing_sheet.Border
            if border:
                placement_point = border.RangeBox.MinPoint
            else:
                placement_point = self.inv_app.TrnasientGeomtry.CreatePoint2d(0, 0)
            drawing_view = drawing_sheet.DrawingViews.Item(1)
            drawing_sheet.PartsLists.Add(drawing_view, placement_point)
            # TODO add balloons
        # save as dwg and close
        file_name_output = "{}.dwg".format(os.path.basename(model_path).split(".")[0])
        dir_output = os.path.join(self.output_dir, os.path.basename(os.path.dirname(model_path)))
        drawing_doc.SaveAsInventorDWG(os.path.join(dir_output, file_name_output), True)
        drawing_doc.Close(True)
        self.model_doc.Close(True)

        # open dwg file
        dwg_doc = self.bs_app.Documents.Open(os.path.join(dir_output, file_name_output))
        # copy acid blocks from paperspace to modelspace
        for obj in dwg_doc.PaperSpace:
            if obj.ObjectName.lower() == "acidblockreference":
                try:
                    dwg_doc.CopyObjects(obj, dwg_doc.ModelSpace)
                except COMError:
                    pass
        # group them closely together for better viewing.
        starting_position = array.array("d", [0, 0, 0])
        for obj in dwg_doc.ModelSpace:
            if obj.ObjectName.lower() == "acidblockreference" or obj.ObjectName.lower() == "acdbblockreference":
                max_point, min_point = self.__get_bounding_box(obj)
                obj.Move(array.array("d", min_point), starting_position)
                starting_position[0] += abs(max_point[0] - min_point[0])
        # convert all acid blocks to "viewable" objects in bricscad in modelspace by exploding.
        for obj in dwg_doc.ModelSpace:
            if obj.ObjectName.lower() == "acidblockreference":
                obj.Explode()
                obj.Delete()
        # apply zoom extents
        self.bs_app.ZoomExtents()
        # close and save dwg file.
        dwg_doc.Close(True)

    def __create_drawing_doc(self):
        # create drawing document
        k_drawing_doc_object_enum = 12292
        drawing_doc = self.inv_app.Documents.Add(k_drawing_doc_object_enum, self.inv_app.FileManager.
                                                 GetTemplateFile(k_drawing_doc_object_enum), True)
        return drawing_doc

    def __create_view(self, view_name, drawing_sheet, x, y):
        view_dict = {
            "front": 10764,
            "back": 10756,
            "right": 10754,
            "left": 10757,
            "top": 10758,
            "bottom": 10755,
            "bottom_left": 10762,
            "bottom_right": 10761,
            "top_left": 10760,
            "top_right": 10759,
        }
        view_enum = view_dict[view_name]
        hidden_line_enum = 32257
        view = drawing_sheet.DrawingViews.AddBaseView(self.model_doc,
                                                      self.inv_app.TransientGeometry.CreatePoint2d(x, y),
                                                      1,
                                                      view_enum,
                                                      hidden_line_enum)
        return view

    def __get_bounding_box(self, obj):
        max_point = automation.VARIANT(array.array('d', [0, 0, 0]))
        min_point = automation.VARIANT(array.array('d', [0, 0, 0]))

        ref_max_point = byref(max_point)
        ref_min_point = byref(min_point)

        obj.GetBoundingBox(ref_min_point, ref_max_point)

        max_point = max_point.value
        min_point = min_point.value

        return max_point, min_point
