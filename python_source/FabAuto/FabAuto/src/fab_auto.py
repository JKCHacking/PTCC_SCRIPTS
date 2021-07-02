import os
import numpy as np
from FabAuto.src.app_creator import AppCreator
from FabAuto.src.util.constants import Constants


def main():
    # initializing enums
    # source: https://help.autodesk.com/view/INVNTOR/2020/ENU/?guid=GUID-BDCE0141-B5F6-4FD4-8300-F305277423DE
    k_drawing_doc_object_enum = 12292
    front_view_enum = 10764
    top_view_enum = 10754
    left_view_enum = 10758
    hidden_line_enum = 32257

    ipt_file = os.path.join(Constants.INPUT_DIR, "testdata001.ipt")
    app_creator = AppCreator("Inventor.Application")
    inventor_app = app_creator.get_app()
    inventor_app.Visible = True

    # creating document objects
    # inventor has separate object for model and paperspace.
    # modelspace = parts document
    # paperspace = drawing document

    drawing_doc = inventor_app.Documents.Add(k_drawing_doc_object_enum,
                                             inventor_app.FileManager.GetTemplateFile(k_drawing_doc_object_enum))
    part_doc = inventor_app.Documents.Open(ipt_file, True)

    # creating sheets where to place different views
    # for now we use the default sheet
    drawing_sheet = drawing_doc.Sheets.Item(1)

    # creating the views
    # front
    front_view = drawing_sheet.DrawingViews.AddBaseView(part_doc,
                                                        inventor_app.TransientGeometry.CreatePoint2d(15, 30),
                                                        0.5,
                                                        front_view_enum,
                                                        hidden_line_enum)
    # top
    top_view = drawing_sheet.DrawingViews.AddBaseView(part_doc,
                                                      inventor_app.TransientGeometry.CreatePoint2d(40, 30),
                                                      0.25,
                                                      top_view_enum,
                                                      hidden_line_enum)
    # left
    left_view = drawing_sheet.DrawingViews.AddBaseView(part_doc,
                                                       inventor_app.TransientGeometry.CreatePoint2d(40, 50),
                                                       0.25,
                                                       left_view_enum,
                                                       hidden_line_enum)
    # rotate views in degrees
    front_view.RotateByAngle(np.deg2rad(90))
    left_view.RotateByAngle(np.deg2rad(180))
    top_view.RotateByAngle(np.deg2rad(90))
