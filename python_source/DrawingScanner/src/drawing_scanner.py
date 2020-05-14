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
                    y_axis = automation.VARIANT(array.array('d', [0, 1, 0]))

                    obj.Rotate3D(origin, y_axis, obj.Rotation)
                    max_point, min_point = self.get_bounding_box(obj)
                    self.create_box(max_point, min_point, modelspace)
                    length = self.get_length(max_point, min_point)
                    length = round(length, 3)
                    print(f'Length: {length} Handle:{handle} Is Rotate: {is_rotate} '
                          f'Rotation: {math.degrees(obj.Rotation)}')

                    quantity_str = f'{1}-{length}'
                    if data_dict:
                        if block_name in data_dict:
                            quantity = int(data_dict[block_name].split('-')[0]) + 1
                            quantity_str = f'{quantity}-{length}'
                    data_dict.update({block_name: quantity_str})
        except COMError:
            pass
        return data_dict

    def get_length(self, max_point, min_point):
        ul_point = array.array('d', [min_point[0], max_point[1], max_point[2]])
        ll_point = array.array('d', [min_point[0], min_point[1], min_point[2]])
        ur_point = array.array('d', [max_point[0], max_point[1], max_point[2]])

        ul_ll_dist = self.get_distance_between_points(ul_point, ll_point)
        ul_ur_dist = self.get_distance_between_points(ul_point, ur_point)

        length = ul_ll_dist if ul_ll_dist > ul_ur_dist else ul_ur_dist
        return length

    @staticmethod
    def get_bounding_box(obj):
        max_point = automation.VARIANT(array.array('d', [0, 0, 0]))
        min_point = automation.VARIANT(array.array('d', [0, 0, 0]))

        ref_max_point = byref(max_point)
        ref_min_point = byref(min_point)

        obj.GetBoundingBox(ref_min_point, ref_max_point)

        max_point = max_point.value
        min_point = min_point.value

        # print(f'maxpoint: {max_point} minpoint: {min_point}')
        return max_point, min_point

    @staticmethod
    def create_box(max_point, min_point, modelspace):
        ul_point = array.array('d', [min_point[0], max_point[1], max_point[2]])
        lr_point = array.array('d', [max_point[0], min_point[1], max_point[2]])
        ll_point = array.array('d', [min_point[0], min_point[1], max_point[2]])
        ur_point = array.array('d', [max_point[0], max_point[1], max_point[2]])

        modelspace.AddLine(ul_point, ur_point)
        modelspace.AddLine(ul_point, ll_point)
        modelspace.AddLine(ll_point, lr_point)
        modelspace.AddLine(lr_point, ur_point)

    @staticmethod
    def set_ucs(drawing):
        origin = array.array('d', [0, 0, 0])
        x_axis = array.array('d', [1, 0, 0])
        y_axis = array.array('d', [0, 0, 1])

        new_ucs = drawing.UserCoordinateSystems.Add(origin, x_axis, y_axis, 'new_ucs')
        drawing.ActiveUCS = new_ucs

        # drawing.SendCommand('UCS\n0,0,0\n1,0,0\n0,0,1\n')

    @staticmethod
    def rotate_all_objs(drawing):
        drawing.SendCommand('selgrip\nall\n\nrotate3d\n0,0,0\n1,0,0\n90\n')

    @staticmethod
    def get_distance_between_points(pt1, pt2):
        distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(pt1, pt2)]))
        return round(distance, 4)


