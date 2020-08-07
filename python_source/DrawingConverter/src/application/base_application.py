from abc import ABC, abstractmethod
from comtypes import client
from comtypes import COMError


class Application(ABC):

    @abstractmethod
    def factory_method(self, application):
        pass

    def __initialize_app(self, app_name):
        cad_application = None
        if app_name:
            try:
                application = client.GetActiveObject(app_name, dynamic=True)
                application.Visible = True
            except(OSError, COMError):
                cad_application = client.CreateObject(app_name, dynamic=True)
                cad_application.Visible = True
        return cad_application

    def get_script(self, app_name=None):
        application = self.__initialize_app(app_name)
        return self.factory_method(application)
