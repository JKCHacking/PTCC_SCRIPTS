import os
import re
import array
import numpy as np
from scipy import spatial
from math import sqrt
from src.factory.applicationfactory import ApplicationFactory
from src.util.exec_timer import timeit
from src.util.constants import Constants
from src.util.logger import get_logger
from src.util.util import Utilities

logger = get_logger("DWGTableExtractor")


def add_table_column(ws, wb):
    wb.add_worksheet_contents(ws, "NO.", (1, 1))
    wb.add_worksheet_contents(ws, "DRAWING NUMBER", (1, 2))
    wb.add_worksheet_contents(ws, "DRAWING TITLE", (1, 3))
    wb.add_worksheet_contents(ws, "SUBMISSION 1", (1, 4))
    wb.add_worksheet_contents(ws, "REV. NO", (2, 4))
    wb.add_worksheet_contents(ws, "DATE", (2, 5))
    wb.add_worksheet_contents(ws, "SUBMISSION 2", (1, 6))
    wb.add_worksheet_contents(ws, "REV. NO", (2, 6))
    wb.add_worksheet_contents(ws, "DATE", (2, 7))
    wb.add_worksheet_contents(ws, "SUBMISSION 3", (1, 8))
    wb.add_worksheet_contents(ws, "REV. NO", (2, 8))
    wb.add_worksheet_contents(ws, "DATE", (2, 9))
    wb.add_worksheet_contents(ws, "SUBMISSION 4", (1, 10))
    wb.add_worksheet_contents(ws, "REV. NO", (2, 10))
    wb.add_worksheet_contents(ws, "DATE", (2, 11))
    wb.add_worksheet_contents(ws, "SUBMISSION 5", (1, 12))
    wb.add_worksheet_contents(ws, "REV. NO", (2, 12))
    wb.add_worksheet_contents(ws, "DATE", (2, 13))
    wb.add_worksheet_contents(ws, "SUBMISSION 6", (1, 14))
    wb.add_worksheet_contents(ws, "REV. NO", (2, 14))
    wb.add_worksheet_contents(ws, "DATE", (2, 15))
    wb.add_worksheet_contents(ws, "SUBMISSION 7", (1, 16))
    wb.add_worksheet_contents(ws, "REV. NO", (2, 16))
    wb.add_worksheet_contents(ws, "DATE", (2, 17))


def is_inside_box(min, max, point):
    min_x = min[0]
    min_y = min[1]
    max_x = max[0]
    max_y = max[1]
    point_x = point[0]
    point_y = point[1]
    return min_x <= point_x <= max_x and min_y <= point_y <= max_y


def is_between_line(left, right, point):
    left_x = left[0]
    left_y = left[1]
    right_x = right[0]
    right_y = right[1]
    point_x = point[0]
    point_y = point[1]

    if left_x == right_x:
        is_between = left_y <= point_y <= right_y
    else:
        is_between = left_x <= point_x <= right_x
    return is_between


def get_entities_within_box(entities, entity_type_ls, min, max):
    entity_list = []
    for entity in entities:
        entity_type = entity.ObjectName
        if entity_type in entity_type_ls:
            if re.search('text', entity_type_ls[0], re.IGNORECASE):  # text type entity
                point = entity.InsertionPoint
                if is_inside_box(min, max, point):
                    entity_list.append(entity)
            elif re.search('line', entity_type_ls[0], re.IGNORECASE) and entity.Visible:  # line type of entity
                try:
                    point = entity.Coordinate(0)
                    if is_inside_box(min, max, point):
                        entity_list.append(entity)
                except NameError:
                    point = entity.StartPoint
                    if is_inside_box(min, max, point):
                        entity_list.append(entity)
    return entity_list


def get_entities_between_line(entities, entity_type_ls, left, right):
    entity_list = []
    for entity in entities:
        if entity.ObjectName in entity_type_ls:
            text_string = entity.TextString
            if is_between_line(left, right, entity.InsertionPoint):
                ins_point = entity.InsertionPoint
                ins_point_x = ins_point[0]
                ins_point_y = ins_point[1]
                text_string = entity.TextString
                entity_list.append((text_string, ins_point_x, ins_point_y))
    return entity_list


def sort_pt_lst(pt_list, target_point):
    sorted_res = sorted(pt_list, key=lambda p: sqrt((p[1] - target_point[0])**2 + (p[2] - target_point[1])**2))
    return sorted_res


def get_nearest_pt(pt_list, target):
    node = list(target)
    nodes = np.asarray(pt_list)
    dist, index = spatial.KDTree(nodes).query(node)
    return index


def extract_cad_table(cadapp, excelapp, drawing_filepath):
    curr_dir = os.path.dirname(drawing_filepath)
    drawing_file_name = os.path.basename(drawing_filepath)
    drawing_name = os.path.splitext(drawing_file_name)[0]

    cad_doc = cadapp.open_document(drawing_filepath)
    modelspace = cad_doc.get_modelspace()
    workbook = excelapp.create_document(os.path.join(curr_dir, f'{drawing_name}.xlsx'))

    text_types = ['AcDbMText', 'AcDbText']
    line_types = ['AcDbPolyline', 'AcDbLine']
    reg_column_names = [
        re.compile("^NO."),
        re.compile("DRAWING...NUMBER"),
        re.compile("DRAWING TITLE"),
        re.compile("SUBMISSION [0-9]+")
    ]

    for entity in modelspace:
        # searching for the outside box of the table
        if entity.ObjectName == "AcDbPolyline" and entity.Layer != "Defpoints" and entity.Closed and entity.Visible:
            print(entity.Handle)
            # getting the bounding box of the table
            min_point, max_point = cad_doc.get_bounding_box(entity)
            # getting all the text entities inside the table box
            text_entities = get_entities_within_box(modelspace, text_types, min_point, max_point)
            # getting all the line entities inside the table box
            line_entities = get_entities_within_box(modelspace, line_types, min_point, max_point)
            # searching for column names (which will match the text string inside regex list)
            for regex in reg_column_names:
                for ent_text in text_entities:
                    text_string = ent_text.TextString
                    # if a column name is found (matched the regex)
                    if regex.match(text_string):
                        print(f"{text_string} Matched in regex List")
                        inst_point = ent_text.InsertionPoint
                        inst_point_x = inst_point[0]
                        inst_point_y = inst_point[1]

                        # create a horizontal line at the insertion point of the text
                        # for getting all the intersecting lines
                        start_point = array.array('d', (inst_point_x + 0.125, inst_point_y, 0))
                        end_point = array.array('d', (inst_point_x - 0.125, inst_point_y, 0))
                        h_line = cad_doc.add_line(start_point, end_point)
                        # get all the intersecting lines
                        h_p_list = []
                        for ent_line in line_entities:
                            # horizontal
                            h_int_p = h_line.IntersectWith(ent_line, 1)
                            if h_int_p and h_int_p != inst_point:
                                if len(h_int_p) == 6:
                                    first_half = h_int_p[:3]
                                    second_half = h_int_p[3:]
                                    h_p_list.append(first_half)
                                    h_p_list.append(second_half)
                                else:
                                    h_p_list.append(h_int_p)
                        h_line.Delete()
                        # getting the point in a line that is nearest to the MText Entity
                        index = get_nearest_pt(h_p_list, inst_point)
                        right_v_pt = h_p_list.pop(int(index))
                        index = get_nearest_pt(h_p_list, inst_point)
                        left_v_pt = h_p_list.pop(int(index))

                        right = right_v_pt
                        left = left_v_pt
                        if right_v_pt[0] < left_v_pt[0]:
                            right = left_v_pt
                            left = right_v_pt

                        # getting the entities between the points nearest to the Column name
                        text_ent_list = get_entities_between_line(text_entities, text_types, left, right)
                        if not text_ent_list:
                            print(f"There are no texts found under column {text_string}")
                        sorted_list = sort_pt_lst(text_ent_list, inst_point)
                        for text_ent in sorted_list:
                            print(text_ent)
    workbook.save()


@timeit
def main(dir_or_file):
    cad_application = ApplicationFactory.create_application("CadApp")
    excel_application = ApplicationFactory.create_application("ExcelApp")

    cad_application.start_app()
    excel_application.start_app()

    if os.path.isdir(dir_or_file):
        for dir_path, dir_names, file_names in os.walk(dir_or_file):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(Constants.DWG_FILE_EXT):
                    logger.info(f"Working with file: {file_name}")
                    extract_cad_table(cad_application, excel_application, file_full_path)
        Utilities.clean_up_file(['.bak'], dir_or_file)
    elif os.path.isfile(dir_or_file):
        directory = os.path.dirname(dir_or_file)
        file_name = os.path.basename(dir_or_file)
        if dir_or_file.endswith(Constants.DWG_FILE_EXT):
            logger.info(f"Working with file: {file_name}")
            extract_cad_table(cad_application, excel_application, dir_or_file)
        Utilities.clean_up_file(['.bak'], directory)
    cad_application.stop_app()
    excel_application.stop_app()
