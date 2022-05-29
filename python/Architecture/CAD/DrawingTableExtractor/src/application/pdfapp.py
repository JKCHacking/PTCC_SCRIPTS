from src.application.application import Application
from src.document.pdfdocument import PdfDocument
from src.util.logger import get_logger


class PdfApp(Application):
    def __init__(self):
        self.logger = get_logger("PdfAppLogger")

    def start_app(self):
        pass

    def stop_app(self):
        pass

    def open_document(self, filepath):
        pass

    def create_document(self, filepath):
        return PdfDocument(filepath)
