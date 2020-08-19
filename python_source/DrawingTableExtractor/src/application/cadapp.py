from comtypes import client
from comtypes import COMError
from src.application.application import Application
from src.document.caddocument import CadDocument
from src.util.constants import Constants
from src.util.logger import get_logger


class CadApp(Application):
    def __init__(self):
        self.logger = get_logger("CaddAppLogger")
        self.cad_application = None

    def start_app(self):
        self.logger.info(f"Starting {Constants.BRICS_APP_NAME}...")
        try:
            self.cad_application = client.GetActiveObject(Constants.BRICS_APP_NAME, dynamic=True)
            self.cad_application.Visible = False
        except(OSError, COMError):
            self.cad_application = client.CreateObject(Constants.BRICS_APP_NAME, dynamic=True)
            self.cad_application.Visible = False
        return self.cad_application

    def stop_app(self):
        self.logger.info(f"Stopping {Constants.BRICS_APP_NAME}...")
        self.cad_application.Quit()

    def open_document(self, filepath):
        doc = self.cad_application.Documents.Open(filepath)
        return CadDocument(doc)

    def create_document(self, filepath):
        pass
