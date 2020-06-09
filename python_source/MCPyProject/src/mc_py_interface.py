#!/usr/bin/env python
from comtypes import client
from comtypes import COMError
from comtypes import automation
from comtypes.client import Constants as ct_constants
from src.constants import Constants
from src.logger import Logger

logger = Logger()


class MCPyScript:
    def __init__(self):
        self.logger = logger.get_logger()
        try:
            self.mathcad = client.GetActiveObject(Constants.APP_NAME, dynamic=True)
            self.mathcad.Visible = True
        except (OSError, COMError):
            self.logger.info(f"{Constants.APP_NAME} is not Running...")
            self.logger.info(f"Opening {Constants.APP_NAME}...")
            self.mathcad = client.CreateObject(Constants.APP_NAME, dynamic=True)
            self.mathcad.Visible = True

        self.mc_constants = ct_constants(self.mathcad)

    def evaluate_mathcad(self, worksheet_path):
        ws_collection = self.mathcad.Worksheets
        ws = ws_collection.Open(worksheet_path)

        try:
            ina_val = automation.VARIANT(1000)
            inb_val = automation.VARIANT(500)

            ws.SetValue("ina", ina_val)
            ws.SetValue("inb", inb_val)
            ws.Recalculate()

            value_a = ws.GetValue("a")
            value_b = ws.GetValue("b")
            value_ina = ws.GetValue("ina")
            value_inb = ws.GetValue("inb")

            res = ws.GetValue("answer")

            self.logger.info(f'a: {value_a.AsString}')
            self.logger.info(f'a: {value_a.GetElement(0,0).AsString}')
            self.logger.info(f'a: {value_a.GetElement(1, 0).AsString}')
            self.logger.info(f'a: {value_a.GetElement(2, 0).AsString}')
            self.logger.info(f'b: {value_b.AsString}')
            self.logger.info(f'ina: {value_ina.AsString}')
            self.logger.info(f'inb: {value_inb.AsString}')
            self.logger.info(f'Answer: {res.AsString}')
        except COMError as e:
            self.logger.info(str(e))

        save_changes_enum = self.mc_constants.mcSaveChanges
        self.logger.info(save_changes_enum)
        # ws.Save()
