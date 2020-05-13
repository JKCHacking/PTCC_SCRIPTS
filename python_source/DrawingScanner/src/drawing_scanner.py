#!/usr/bin/env python
from src.cad_script import CadScript


class DrawingScanner(CadScript):

    def __init__(self):
        super().__init__()

    @staticmethod
    def search_blocks(modelspace):
        data_dict = {}
        for obj in modelspace:
            if obj.ObjectName == 'AcDbBlockReference':
                block_name = obj.Name
                quantity = 1
                if data_dict:
                    if block_name in data_dict:
                        quantity = data_dict[block_name] + 1
                data_dict.update({block_name: quantity})
        return data_dict

