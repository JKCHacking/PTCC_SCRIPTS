import time
import os
from src.document.document import Document
from src.util.util import Utilities
from pywinauto.mouse import click


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
        delete_command = '{DELETE}'

        # click the command line
        click(button="left", coords=(2162, 1130))
        Utilities.send_command("{ESC}exportpdf~")
        Utilities.copy_to_cb(filename)
        time.sleep(1)
        Utilities.send_command(delete_command + paste_command + enter_command)

    def layout_to_pdf(self):
        layouts = self.get_layouts()
        dir_name = os.path.dirname(self.get_document_fp())
        layout_name_list = []
        for layout in layouts:
            self.document.ActiveLayout = layout
            layout_name = layout.Name
            if layout_name != 'Model':
                pdf_filepath = os.path.join(dir_name, f"{layout_name}.pdf")
                self.__export_to_pdf(pdf_filepath)
                layout_name_list.append(layout_name)
        return layout_name_list

    def close(self):
        self.document.Close()
