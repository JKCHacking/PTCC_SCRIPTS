import os
from comtypes import COMError


class CadDocument:
    def __init__(self, cad_application):
        self.cad_application = cad_application

    def open_document(self, document_path):
        document = None
        if os.path.exists(document_path):
            try:
                self.cad_application.Documents.Open(document_path)
                document = self.cad_application.ActiveDocument
            except COMError:
                print("[ERROR]Invalid Drawing File!: {}".format(document_path))
        return document

    def save_document(self, document_obj):
        if not document_obj.Saved:
            document_obj.Save()

    def save_as_document(self, document_obj, file_name, file_type=None):
        file_type_enum = None
        secu_param = self.cad_application.GetInterfaceObject("BricscadApp.AcadSecurityParams")

        # converts according to the autocad enums
        if file_type == "ac2013_dxf":  # Autocad 2013 DWG
            file_type_enum = 61
        elif file_type == "ac2013_dwg":  # Autocad 2013 DXF
            file_type_enum = 60
        document_obj.SaveAs(file_name, file_type_enum, secu_param)

    def close_all_documents(self):
        self.cad_application.Documents.Close()

    def close_document(self, document_obj):
        document_obj.Close()

    def delete_document(self, document_path):
        os.remove(document_path)