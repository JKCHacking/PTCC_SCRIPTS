#!/usr/bin/env python
from src.cad_script import CadScript
import array
from comtypes import automation
from comtypes import COMError
from ctypes import byref
import math


class DrawingScanner(CadScript):

    def __init__(self):
        super().__init__()

    def search_blocks(self, modelspace):
        data_dict = {}
        length_list = []
        try:
            for obj in modelspace:
                if obj.ObjectName == 'AcDbBlockReference':
                    is_rotate = False
                    block_name = obj.Name
                    handle = obj.Handle
                    origin = automation.VARIANT(array.array('d', [0, 0, 0]))

                    length = self.get_length(obj)
                    if length < 1:
                        cpy_block = obj.Copy()

                        exploded_object = cpy_block.Explode()
                        solid = exploded_object[0]
                        position = array.array('d', list(solid.Position))
                        cpy_block.Move(position, origin)

                        rot_pt1 = automation.VARIANT(array.array('d', [1, 0, 0]))
                        rot_pt2 = automation.VARIANT(array.array('d', [1, 1, 0]))
                        angle = math.radians(90)

                        cpy_block.Rotate3D(rot_pt1, rot_pt2, angle)
                        length = self.get_length(cpy_block)
                        cpy_block.Delete()
                        solid.Delete()
                        is_rotate = True
                    length = round(length, 3)
                    print(f'Length: {length} Handle:{handle} Is Rotate: {is_rotate}')

                    quantity_str = f'{1}-{length}'
                    if data_dict:
                        if block_name in data_dict:
                            quantity = int(data_dict[block_name].split('-')[0]) + 1
                            quantity_str = f'{quantity}-{length}'
                    data_dict.update({block_name: quantity_str})
        except COMError:
            pass
        return data_dict

    @staticmethod
    def get_length(obj):
        max_point = automation.VARIANT(array.array('d', [0, 0, 0]))
        min_point = automation.VARIANT(array.array('d', [0, 0, 0]))

        ref_max_point = byref(max_point)
        ref_min_point = byref(min_point)

        obj.GetBoundingBox(ref_min_point, ref_max_point)

        max_point = max_point.value
        min_point = min_point.value
        print(f'{max_point}\t{min_point}')
        length = max_point[0] - min_point[0]
        return length

