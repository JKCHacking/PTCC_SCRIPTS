from src.application.cad_application import CadApplication
from src.constants import Constants


def script_factory(extension):
    script = None
    if extension == ".dwg":
        script = CadApplication().get_script(Constants.BRICSCAD_APP_NAME)
    return script
