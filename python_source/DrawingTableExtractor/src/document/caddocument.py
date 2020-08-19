import time
from src.document.document import Document
from src.util.util import Utilities


class CadDocument(Document):
    def __init__(self, document):
        self.document = document

    def get_layouts(self):
        return self.document.Layouts

    def get_document_fp(self):
        return self.document.FullName

    def __export_to_pdf(self, filename):
        paste_command = '^v'
        enter_command = '~'

        Utilities.copy_to_cb(filename)
        self.document.SendCommand("_exportpdf")
        time.sleep(1)
        Utilities.send_command(paste_command)
        Utilities.send_command(enter_command)

    def layout_to_pdf(self):
        layouts = self.get_layouts()
        layout_name_list = []
        for layout in layouts:
            layout.Active = True
            layout_name = layout.Name
            if layout_name != 'Model':
                self.__export_to_pdf(layout_name)
                layout_name_list.append(layout_name)
        return layout_name_list
