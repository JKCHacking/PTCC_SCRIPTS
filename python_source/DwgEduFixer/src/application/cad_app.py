from comtypes import client
from comtypes import COMError

APP_NAME = "BricscadApp.AcadApplication"


class CadApp:
    def __init__(self):
        self.cad_application = None

    def start_app(self):
        try:
            self.cad_application = client.GetActiveObject(APP_NAME, dynamic=True)
            self.cad_application.Visible = False
        except(OSError, COMError):
            self.cad_application = client.CreateObject(APP_NAME, dynamic=True)
            self.cad_application.Visible = False
        return self.cad_application

    def get_cad_application(self):
        return self.cad_application

    def exit_app(self):
        self.cad_application.Quit()
