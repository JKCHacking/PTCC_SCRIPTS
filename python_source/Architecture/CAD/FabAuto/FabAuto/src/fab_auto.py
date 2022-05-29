import os
import pint
from comtypes import COMError
from FabAuto.src.app_creator import AppCreator
from FabAuto.src.util.constants import Constants

PINT_UNIT = pint.UnitRegistry()
PINT_UNIT.default_system = "SI"


def get_unit_document(document):
    unit_dict = {
        0: "dimensionless",
        1: "inches",
        2: "feet",
        3: "miles",
        4: "millimeters",
        5: "centimeters",
        6: "meters",
        7: "kilometers",
        8: "microinches",
        9: "mils",
        10: "yards",
        11: "angstroms",
        12: "nanometers",
        13: "microns",
        14: "decimeters",
        15: "dekameters",
        16: "hectometers",
        17: "gigameters",
        18: "astronomical Units",
        19: "light Years",
    }

    unit_num = document.GetVariable("INSUNITS")
    try:
        unit_name = unit_dict[unit_num]
    except KeyError:
        unit_name = unit_dict[0]
        print("Unsupported Unit number")
    return unit_name


def iter_input():
    for dir_path, dir_names, file_names in os.walk(Constants.INPUT_DIR):
        for file_name in file_names:
            if file_name.endswith(".ipt"):
                yield os.path.join(dir_path, file_name)


def main():
    app_creator = AppCreator("Inventor.Application")
    inventor_app = app_creator.get_app()
    UOM = inventor_app.UnitsOfMeasure
    app_creator = AppCreator("BricscadApp.AcadApplication")
    bs_app = app_creator.get_app()

    for ipt_file in iter_input():
        part_doc = inventor_app.Documents.Open(ipt_file)
        component_definition = part_doc.ComponentDefinition
        parameters = component_definition.Parameters
        surface_bodies = component_definition.SurfaceBodies

        print("There are {} Surface Bodies in the Model.".format(surface_bodies.Count))
        for surface_body in surface_bodies:
            surf_body_name = surface_body.Name
            template_path = None
            # searching for the appropriate template for the surface body
            for filename in os.listdir(os.path.join(Constants.TEMPLATE_DIR)):
                if filename.endswith(".dwg") and filename.split(".")[0] in surf_body_name:
                    template_path = os.path.join(Constants.TEMPLATE_DIR, filename)
                    break

            if template_path:
                print("Found template for {}".format(surf_body_name))
                dwg_template_doc = bs_app.Documents.Open(template_path)
                bs_unit = get_unit_document(dwg_template_doc)
                for parameter in parameters:
                    if parameter.ParameterType == 11524:
                        # the value that you get will always be converted based on the Database unit of the inventor
                        # document. we have to actually take the "ACTUAL" value of the parameter by converting
                        # it using the UOM.ConvertUnits()
                        parameter_unit = parameter.Units
                        try:
                            value = UOM.ConvertUnits(parameter.Value, UOM.GetTypeFromString(
                                UOM.GetDatabaseUnitsFromExpression(parameter.Expression, parameter_unit)),
                                                            parameter_unit)
                        except COMError:
                            continue
                        try:
                            normalized_inv_unit = str(PINT_UNIT(parameter_unit).units)
                        except pint.errors.UndefinedUnitError:
                            continue
                        normalized_bs_unit = str(PINT_UNIT(bs_unit).units)
                        if normalized_bs_unit != normalized_inv_unit:
                            # convert inventor unit to bricscad unit
                            converted_equation = PINT_UNIT("{}{}".format(value,
                                                                         parameter_unit)).to(normalized_bs_unit)
                            value = converted_equation.magnitude
                        command_str = "-PARAMETERS edit {} {}\n".format(parameter.Name, value)
                        dwg_template_doc.SendCommand(command_str)
                dwg_template_doc.SaveAs(os.path.join(Constants.OUTPUT_DIR, surf_body_name))
                dwg_template_doc.Close()
        part_doc.Close(True)
