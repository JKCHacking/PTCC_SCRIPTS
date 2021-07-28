import os
import array
from comtypes import client
from comtypes import COMError
from comtypes import automation
from ctypes import byref
from balloon_helper import BalloonHelper

# ENUMS
# View orientation enums
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
# Drawing style enum
kHiddenLineDrawingViewStyle = 32257
# Document Type enum
kDrawingDocumentObject = 12292
# structured level enum for parts list table generation
kStructuredAllLevels = 46595


class ViewsExtractor:
    def __init__(self, output_dir):
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
        margin = 10
        try:
            base_view = drawing_sheet.DrawingViews.AddBaseView(
                self.model_doc,
                self.inv_app.TransientGeometry.CreatePoint2d(0, 0),
                1,
                kTopViewOrientation,
                kHiddenLineDrawingViewStyle,
                "Top")
        except COMError:
            print("Failed to create base view")
            drawing_doc.Close(True)
            self.model_doc.Close(True)
            return None
        base_center_pt = base_view.Center
        back_projected = drawing_sheet.DrawingViews.AddProjectedView(
            base_view, self.inv_app.TransientGeometry.CreatePoint2d(
                base_center_pt.X,
                base_center_pt.Y + base_view.Height + margin),
            kHiddenLineDrawingViewStyle,
            1)
        front_projected = drawing_sheet.DrawingViews.AddProjectedView(
            base_view, self.inv_app.TransientGeometry.CreatePoint2d(
                base_center_pt.X,
                base_center_pt.Y - base_view.Height - margin),
            kHiddenLineDrawingViewStyle,
            1)
        left_projected = drawing_sheet.DrawingViews.AddProjectedView(
            base_view,
            self.inv_app.TransientGeometry.CreatePoint2d(
                base_center_pt.X - base_view.Width - margin,
                base_center_pt.Y),
            kHiddenLineDrawingViewStyle,
            1)
        right_projected = drawing_sheet.DrawingViews.AddProjectedView(
            base_view,
            self.inv_app.TransientGeometry.CreatePoint2d(
                base_center_pt.X + base_view.Width + margin,
                base_center_pt.Y),
            kHiddenLineDrawingViewStyle,
            1)

        # reposition the views again.
        range_box = drawing_sheet.Border.RangeBox
        border_min = range_box.MinPoint
        border_max = range_box.MaxPoint
        sheet_center = self.inv_app.TransientGeometry.CreatePoint2d((border_max.X - border_min.X) / 2,
                                                                    (border_max.Y - border_min.Y) / 2)
        base_view.Center = sheet_center
        back_projected.Center = self.inv_app.TransientGeometry.CreatePoint2d(
            base_view.Center.X,
            base_view.Center.Y + base_view.Height / 2 + margin + back_projected.Height / 2)
        front_projected.Center = self.inv_app.TransientGeometry.CreatePoint2d(
            base_view.Center.X,
            base_view.Center.Y - base_view.Height / 2 - margin - front_projected.Height / 2)
        left_projected.Center = self.inv_app.TransientGeometry.CreatePoint2d(
            base_view.Center.X - base_view.Width / 2 - margin - left_projected.Width / 2,
            base_view.Center.Y
        )
        right_projected.Center = self.inv_app.TransientGeometry.CreatePoint2d(
            base_view.Center.X + base_view.Width / 2 + margin + right_projected.Width / 2,
            base_view.Center.Y
        )
        if model_path.endswith(".iam"):
            print("[ViewsExtractor] Adding PartsList Table and Balloon...")
            # add parts list table
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
        drawing_doc.SaveAs(dwg_path, True)
        drawing_doc.Close(True)
        self.model_doc.Close(True)
        return dwg_path

    def fix_inventor_dwg(self, dwg_path):
        print("[ViewsExtractor] Fixing things in DWG...")
        # fix objects in modelspace
        # open dwg file
        dwg_doc = self.bs_app.Documents.Open(dwg_path)
        # delete default title blocks
        for obj in dwg_doc.ModelSpace:
            if obj.ObjectName.lower() == "acdbblockreference":
                obj.Delete()
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
