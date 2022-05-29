from FabAuto.src.app_creator import AppCreator


class InventorController:
    def __init__(self):
        app_creator = AppCreator("Inventor.Application")
        self.inventor_app = app_creator.get_app()
        self.inventor_app.Visible = True

    def create_part_document(self, ipt_fp):
        part_doc = self.inventor_app.Documents.Open(ipt_fp, True)
        return part_doc

    def create_drawing_document(self):
        k_drawing_doc_object_enum = 12292
        drawing_doc = self.inventor_app.Documents.Add(k_drawing_doc_object_enum, self.inventor_app.FileManager.
                                                      GetTemplateFile(k_drawing_doc_object_enum))
        return drawing_doc

    def create_view(self, part_doc, drawing_doc, view_name, x, y):
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
        drawing_sheet = drawing_doc.Sheets.Item(1)
        view = drawing_sheet.DrawingViews.AddBaseView(part_doc,
                                                      self.inventor_app.TransientGeometry.CreatePoint2d(x, y),
                                                      1,
                                                      view_enum,
                                                      hidden_line_enum)
        return view

    def save_drawing_as_dwg(self, drawing_doc, dwg_fp):
        drawing_doc.SaveAsInventorDWG(dwg_fp, True)

    def close_document(self, document):
        document.Close(True)

    def quit_app(self):
        self.inventor_app.Quit()