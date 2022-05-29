import os
import ezdxf
import ezdxf.math
from openpyxl import Workbook
from src.util.constants import Constants


class Script:
    def iter_input(self):
        """
            gets every file in the output folder and process the necessary data
        """
        input_dir = Constants.INPUT_DIR
        for dir_path, dir_names, file_names in os.walk(input_dir):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(Constants.DXF_FILE_EXT):
                    # for every dxf file you create 1 excel file
                    workbook = Workbook()
                    # getting each paperspace layout
                    for paperspace in self.__get_paperspace(file_full_path):
                        mtext_list = []
                        for mtext_ent in self.__get_mtext(paperspace):
                            found = False
                            count = 1
                            text = mtext_ent.plain_text()

                            for mtext in mtext_list:
                                if mtext['A'] == text:
                                    mtext['B'] += 1
                                    found = True
                                    break
                            if not found:
                                mtext_data_dict = self.__compose_data_dict(text, count)
                                mtext_list.append(mtext_data_dict)
                        ps_name = paperspace.name
                        # for every paperspace layout you create 1 worksheet
                        self.__create_spreadsheet(workbook, ps_name, mtext_list)
                    filename_ext = os.path.basename(file_full_path)
                    filename = os.path.splitext(filename_ext)[0]
                    output_dir = os.path.join(Constants.OUTPUT_DIR, filename + '.xlsx')
                    if len(workbook.worksheets) > 1:
                        default_ws = workbook["Sheet"]
                        workbook.remove(default_ws)
                        workbook.save(output_dir)
                    else:
                        print(f"No BlockReference Found inside file: {file_full_path}")

    def __create_spreadsheet(self, workbook, ws_name, ent_list):
        # add unit conversions that are necessary
        fieldnames = ['Text', 'Count']
        worksheet = workbook.create_sheet(f"{ws_name}")
        worksheet.append(fieldnames)
        for ent_prop in ent_list:
            worksheet.append(ent_prop)

    def __compose_data_dict(self, text, count):
        ent_prop_dict = {
            'A': text,
            'B': count,
        }
        return ent_prop_dict

    def __get_paperspace(self, dxf_fp):
        dxf_file = ezdxf.readfile(dxf_fp)
        layout_list = dxf_file.layout_names_in_taborder()
        for layout_name in layout_list:
            yield dxf_file.layout(layout_name)

    def __get_mtext(self, paperspace):
        for ent in paperspace:
            if ent.dxftype() == "MTEXT":
                yield ent
