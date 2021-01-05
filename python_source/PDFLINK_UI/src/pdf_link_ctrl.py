import os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QObject


class PDFLinkCtrl(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.connect_signals()

    @pyqtSlot()
    def create_links(self):
        print("Creating Links...")
        keyword = self.view.keyword_line_edit.text()
        page = self.view.page_line_edit.text()
        pdf_file_path = self.view.pdf_file_path

        pdf_file_dirname = os.path.dirname(pdf_file_path)
        pdf_file_name_modified = os.path.splitext(os.path.basename(pdf_file_path))[0] + "_modified.pdf"
        pdf_file_path_modified = os.path.join(pdf_file_dirname, pdf_file_name_modified)

        model = self.model(pdf_file_path, keyword, int(page) - 1)  # subtract 1 to be a zero-based page number
        model.add_link()
        model.save_document(pdf_file_path_modified)

    def connect_signals(self):
        self.view.browse_button.clicked.connect(self.view.open_file)
        self.view.ok_button.connect(self.create_links)
        self.view.cancel_button.connect(self.view.close)
