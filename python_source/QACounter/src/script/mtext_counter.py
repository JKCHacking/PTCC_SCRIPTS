import os
from openpyxl.workbook import Workbook
from src.util.constants import Constants
from src.cad.cad_manager import CadManager


class MTextCounter:
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
                    cad_manager = CadManager(file_full_path)
                    # getting each paperspace layout
                    for space in cad_manager.get_all_layout_space():
                        mtext_list = []
                        for mtext_ent in cad_manager.get_mtext(space):
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
                        ps_name = space.name
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
