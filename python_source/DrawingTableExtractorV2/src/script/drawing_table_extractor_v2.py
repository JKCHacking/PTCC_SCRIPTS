import os
import re
import operator
from math import degrees, floor
from src.factory.applicationfactory import ApplicationFactory
from src.util.exec_timer import timeit
from src.util.constants import Constants
from src.util.logger import get_logger
from src.util.util import Utilities

logger = get_logger("DWGTableExtractor")


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
    elif left_y == right_y:
        is_between = left_x <= point_x <= right_x
    else:  # TODO: line are not the same length
        is_between = False
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


def get_entities_between_points(entities, entity_type_ls, left, right):
    entity_list = []
    for entity in entities:
        if entity.ObjectName in entity_type_ls:
            ins_point = entity.InsertionPoint
            if is_between_line(left, right, ins_point):
                ins_point_x = ins_point[0]
                ins_point_y = ins_point[1]
                text_string = entity.TextString
                entity_list.append((ins_point_x, ins_point_y, text_string))
    return entity_list


def add_table_column(ws):
    ws.cell(row=1, column=1, value="NO.")
    ws.cell(row=1, column=2, value="DRAWING NUMBER")
    ws.cell(row=1, column=3, value="DRAWING TITLE")
    ws.cell(row=1, column=4, value="SUBMISSION 1")
    ws.cell(row=2, column=4, value="REV. NO")
    ws.cell(row=2, column=5, value="DATE")
    ws.cell(row=1, column=6, value="SUBMISSION 2")
    ws.cell(row=2, column=6, value="REV. NO")
    ws.cell(row=2, column=7, value="DATE")
    ws.cell(row=1, column=8, value="SUBMISSION 3")
    ws.cell(row=2, column=8, value="REV. NO")
    ws.cell(row=2, column=9, value="DATE")
    ws.cell(row=1, column=10, value="SUBMISSION 4")
    ws.cell(row=2, column=10, value="REV. NO")
    ws.cell(row=2, column=11, value="DATE")
    ws.cell(row=1, column=12, value="SUBMISSION 5")
    ws.cell(row=2, column=12, value="REV. NO")
    ws.cell(row=2, column=13, value="DATE")
    ws.cell(row=1, column=14, value="SUBMISSION 6")
    ws.cell(row=2, column=14, value="REV. NO")
    ws.cell(row=2, column=15, value="DATE")
    ws.cell(row=1, column=16, value="SUBMISSION 7")
    ws.cell(row=2, column=16, value="REV. NO")
    ws.cell(row=2, column=17, value="DATE")
    ws.cell(row=1, column=18, value="SUBMISSION 8")
    ws.cell(row=2, column=18, value="REV. NO")
    ws.cell(row=2, column=19, value="DATE")
    ws.cell(row=1, column=20, value="SUBMISSION 9")
    ws.cell(row=2, column=20, value="REV. NO")
    ws.cell(row=2, column=21, value="DATE")
    ws.cell(row=1, column=22, value="SUBMISSION 10")
    ws.cell(row=2, column=22, value="REV. NO")
    ws.cell(row=2, column=23, value="DATE")


def add_excel_data(worksheet, data):
    # add data to worksheet
    for row, row_list in enumerate(data):
        row = row + 3
        for column, row_data in enumerate(row_list):
            worksheet.cell(row=row, column=column + 1, value=row_data[2])


def extract_cad_table(cad_doc):
    modelspace = cad_doc.get_modelspace()

    text_types = ['AcDbMText', 'AcDbText']
    line_types = ['AcDbPolyline', 'AcDbLine']
    reg_column_names = [
        re.compile("^NO."),
        re.compile("DRAWING...NUMBER"),
        re.compile("DRAWING TITLE"),
        re.compile("SUBMISSION [0-9]+"),
        re.compile("REV. NO."),
        re.compile("DATE")
    ]

    for entity in modelspace:
        # searching for the outside box of the table
        if entity.ObjectName == "AcDbPolyline" and entity.Layer != "Defpoints" and entity.Closed and entity.Visible:
            logger.info(f"Table found with Handle: {entity.Handle}")
            # getting the bounding box of the table
            min_point, max_point = cad_doc.get_bounding_box(entity)
            # getting all the text entities inside the table box
            text_entities = get_entities_within_box(modelspace, text_types, min_point, max_point)
            # getting all the line entities inside the table box
            line_entities = get_entities_within_box(modelspace, line_types, min_point, max_point)

            # start points of every horizontal lines
            h_s_pt_list = []
            for line in line_entities:
                if line.ObjectName == 'AcDbPolyline':
                    exploded_line = line.Explode()
                    for e_line in exploded_line:
                        if e_line.ObjectName == "AcDbLine":
                            angle = floor(degrees(e_line.Angle))
                            if angle == 0:
                                start_point = e_line.StartPoint
                                h_s_pt_list.append(start_point)
                            elif angle == 180:
                                end_point = e_line.EndPoint
                                h_s_pt_list.append(end_point)
            # sorted from top to bottom points within rows of the table (start points of every horizontal lines)
            sorted_h_s_pt_list = sorted(h_s_pt_list, key=operator.itemgetter(1), reverse=True)

            # remove all column entities in the table
            data_entity_list = []  # data entities only (no column entities)
            for text_ent in text_entities:
                text_string = text_ent.TextString
                if not any(regex.match(text_string) for regex in reg_column_names):
                    data_entity_list.append(text_ent)

            table_rows_list = []
            for index, h_s_pt in enumerate(sorted_h_s_pt_list):
                try:
                    top = h_s_pt
                    bottom = sorted_h_s_pt_list[index + 1]
                    # print(f"top: {top}, bottom: {bottom}")
                    row_entities_list = get_entities_between_points(data_entity_list, text_types, bottom, top)
                    if row_entities_list:
                        # sort according to x value (left to right)
                        sorted_row_entities_list = sorted(row_entities_list, key=operator.itemgetter(0))
                        table_rows_list.append(sorted_row_entities_list)
                except IndexError:
                    pass
            yield table_rows_list


def script_process(cad_app, excel_app, dir_path, file_name):
    post_fix = 65  # A
    file_full_path = os.path.join(dir_path, file_name)
    cad_doc = cad_app.open_document(file_full_path)
    file_name_only = os.path.splitext(file_name)[0]
    excel_file_path = os.path.join(dir_path, f'{file_name_only}.xlsx')
    workbook = excel_app.create_document(excel_file_path)
    for table_data in extract_cad_table(cad_doc):
        sheet_name = f"{file_name_only}{chr(post_fix)}"
        worksheet = workbook.create_worksheet(sheet_name)
        add_table_column(worksheet)
        add_excel_data(worksheet, table_data)
        post_fix += 1
    cad_doc.close()
    # if the sheets are only the default sheet don't save. (No tables found)
    # Workbook should always have at least 1 worksheet inside.
    if len(workbook.get_worksheets()) > 1:
        default_ws = workbook.get_worksheet_by_name("Sheet")
        workbook.remove_worksheet(default_ws)
        workbook.save()
    else:
        logger.info(f"No tables found in Drawing file: {file_full_path}")


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
                    script_process(cad_application, excel_application, dir_path, file_name)
        Utilities.clean_up_file(['.bak'], dir_or_file)
    elif os.path.isfile(dir_or_file):
        directory = os.path.dirname(dir_or_file)
        file_name = os.path.basename(dir_or_file)
        if dir_or_file.endswith(Constants.DWG_FILE_EXT):
            logger.info(f"Working with file: {file_name}")
            script_process(cad_application, excel_application, directory, file_name)
        Utilities.clean_up_file(['.bak'], directory)
    cad_application.stop_app()
    excel_application.stop_app()
