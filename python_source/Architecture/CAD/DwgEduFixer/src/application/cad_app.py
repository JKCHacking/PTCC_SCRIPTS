from comtypes import client
from comtypes import COMError
from src.util.constants import Constants
from src.util.logger import get_logger
from src.document.cad_document import CadDocument


class CadApp:
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

    def create_document(self):
        doc = CadDocument(self.cad_application)
        return doc

    def exit_app(self):
        self.logger.info(f"Exiting {Constants.BRICS_APP_NAME}...")
        self.cad_application.Quit()
