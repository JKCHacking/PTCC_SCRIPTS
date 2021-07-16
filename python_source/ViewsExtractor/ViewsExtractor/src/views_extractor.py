import os
import array
from comtypes import client
from comtypes import COMError
from comtypes import automation
from ctypes import byref
from balloon_helper import BalloonHelper

# ENUMS
kFrontViewOrientation = 10764
kBackViewOrientation = 10756
kLeftViewOrientation = 10758
kRightViewOrientation = 10755
kTopViewOrientation = 10754
kBottomViewOrientation = 10757
kIsoTopRightViewOrientation = 10759
kIsoTopLeftViewOrientation = 10760
kIsoBottomLeftViewOrientation = 10762
kIsoBottomRightViewOrientation = 10761
kHiddenLineDrawingViewStyle = 32257
kDrawingDocumentObject = 12292
kStructuredAllLevels = 46595


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
        # avoid dialogs when error occurs
        self.inv_app.SilentOperation = True
        self.inv_app.Visible = True
        self.bs_app.Visible = True

    def extract_2d_views(self, model_path):
        # open the model file
        try:
            self.model_doc = self.inv_app.Documents.Open(model_path)
        except COMError:
            print("[ViewsExtractor] Failed to open file: {}".format(os.path.basename(model_path)))
            return None
        drawing_doc = self.__create_drawing_doc()
        drawing_sheet = drawing_doc.Sheets.Item(1)
        # create 2d views from model and place on the drawing sheet.
        print("[ViewsExtractor] Creating Views...")
        x = 0
        y = 0
        prev_height = 0
        margin = 10
        for i, view_name in enumerate(self.view_list):
            if i == 0:
                view = self.__create_view(view_name, drawing_sheet, 0, 0)
            else:
                view = self.__create_view(view_name, drawing_sheet, 20, 0)
                y += prev_height / 2 + view.Height / 2 + margin
                view.Center = self.inv_app.TransientGeometry.CreatePoint2d(x, y)
            prev_height = view.Height
        # if the file is an assembly file we need to add parts list table and balloons.
        if model_path.endswith(".iam"):
            print("[ViewsExtractor] Adding PartsList Table and Balloon...")
            # add partlist table
            placement_point = self.inv_app.TransientGeometry.CreatePoint2d(0, 0)
            drawing_view = drawing_sheet.DrawingViews.Item(1)
            drawing_sheet.PartsLists.Add(drawing_view, placement_point, kStructuredAllLevels)
            # TODO add balloons to every view
            # balloon_helper = BalloonHelper(self.inv_app)
            # for drawing_view in drawing_sheet.DrawingViews:
            #     balloon_helper.add_balloon_to_view(drawing_view)
        # save as dwg and close
        print("[ViewsExtractor] Saving to DWG and Closing...")
        file_name_output = "{}.dwg".format(os.path.splitext(os.path.basename(model_path))[0])
        dwg_path = os.path.join(self.output_dir, file_name_output)
        drawing_doc.SaveAsInventorDWG(dwg_path, True)
        drawing_doc.Close(True)
        self.model_doc.Close(True)
        return dwg_path

    def fix_inventor_dwg(self, dwg_path):
        print("[ViewsExtractor] Fixing things in DWG...")
        # fix objects in modelspace
        # open dwg file
        dwg_doc = self.bs_app.Documents.Open(dwg_path)
        # copy acid blocks from paperspace to modelspace
        for obj in dwg_doc.PaperSpace:
            if obj.ObjectName.lower() == "acidblockreference":
                try:
                    dwg_doc.CopyObjects(obj, dwg_doc.ModelSpace)
                except COMError:
                    pass
        # group them closely together for better viewing.
        margin = 10
        starting_position = array.array("d", [0, 0, 0])
        for obj in dwg_doc.ModelSpace:
            if obj.ObjectName.lower() == "acidblockreference" or obj.ObjectName.lower() == "acdbblockreference":
                max_point, min_point = self.__get_bounding_box(obj)
                obj.Move(array.array("d", min_point), starting_position)
                # lay them out vertically
                # getting the height of the object to offset the new position for the next object
                starting_position[1] += abs(max_point[1] - min_point[1]) + margin
        # convert all acid blocks to "viewable" objects in bricscad in modelspace by exploding.
        for obj in dwg_doc.ModelSpace:
            if obj.ObjectName.lower() == "acidblockreference":
                obj.Explode()
                obj.Delete()
        # put the view name beside view block reference
        for obj in dwg_doc.ModelSpace:
            if obj.ObjectName.lower() == "acdbblockreference":
                max_point, min_point = self.__get_bounding_box(obj)
                block_margin = 5
                mtext_width = 25
                mtext_insertion_pt = array.array("d", [max_point[0] + block_margin, max_point[1], 0])
                # get the view name using the index from the view_list attribute
                view_number_idx = int(obj.Name.split("_")[-1].split("VIEW")[1]) - 1
                view_name = self.view_list[view_number_idx]
                # insert the view name beside the View block reference
                mtext_obj = dwg_doc.ModelSpace.AddMText(mtext_insertion_pt, mtext_width, view_name.capitalize())
                mtext_obj.Height = 10
        # apply zoom extents
        dwg_doc.ActiveLayout = dwg_doc.Layouts.Item("Model")
        self.bs_app.ZoomExtents()
        # close and save dwg file.
        dwg_doc.Close(True)

    def __create_drawing_doc(self):
        # create drawing document
        drawing_doc = self.inv_app.Documents.Add(kDrawingDocumentObject,
                                                 self.inv_app.FileManager.GetTemplateFile(kDrawingDocumentObject))
        return drawing_doc

    def __create_view(self, view_name, drawing_sheet, x, y):
        view_dict = {
            "front": kFrontViewOrientation,
            "back": kBackViewOrientation,
            "right": kRightViewOrientation,
            "left": kLeftViewOrientation,
            "top": kTopViewOrientation,
            "bottom": kBottomViewOrientation,
            "bottom_left": kIsoBottomLeftViewOrientation,
            "bottom_right": kIsoBottomRightViewOrientation,
            "top_left": kIsoTopLeftViewOrientation,
            "top_right": kIsoTopRightViewOrientation,
        }
        try:
            view_enum = view_dict[view_name]
            # this point represents the center of the drawing view
            view = drawing_sheet.DrawingViews.AddBaseView(self.model_doc,
                                                          self.inv_app.TransientGeometry.CreatePoint2d(x, y),
                                                          1,
                                                          view_enum,
                                                          kHiddenLineDrawingViewStyle,
                                                          view_name.capitalize())
        except KeyError:
            view = None
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
