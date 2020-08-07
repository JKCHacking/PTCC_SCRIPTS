from src.application import Application
from src.script.cad_script import CadScript


class CadApplication(Application):

    def factory_method(self, cad_application):
        return CadScript(cad_application)
