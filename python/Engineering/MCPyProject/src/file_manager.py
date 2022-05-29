from src.logger import Logger
from src.constants import Constants
from shutil import copyfile, SameFileError
import os

logger = Logger()


class FileManager:
    def __init__(self):
        self.logger = logger.get_logger()
        self.input_dir_path = Constants.INPUT_DIR
        self.output_dir_path = Constants.OUTPUT_DIR

    def get_image_list(self):
        image_path_list = list()
        for dirpath, dirname, filenames in os.walk(self.input_dir_path):
            for filename in filenames:
                file_fullpath = os.path.join(dirpath, filename)
                if file_fullpath.endswith(Constants.JPG_FILE_EXT) or \
                        file_fullpath.endswith(Constants.BMP_FILE_EXT) or \
                        file_fullpath.endswith(Constants.PNG_FILE_EXT):
                    image_path_list.append(file_fullpath)

        return image_path_list

    def get_ws_fp_ls(self):
        ws_path_list = list()
        for dirpath, dirname, filenames in os.walk(self.input_dir_path):
            for filename in filenames:
                file_fullpath = os.path.join(dirpath, filename)
                src = file_fullpath
                dst = os.path.join(self.output_dir_path, filename)

                if file_fullpath.endswith(Constants.MC_FILE_EXT):
                    try:
                        copyfile(src, dst)
                        ws_path_list.append(dst)
                    except FileExistsError as e:
                        self.logger.warn(e)
                    except SameFileError as e:
                        self.logger.warn(e)
        return ws_path_list

    def get_template_ws(self):
        template_file_name = 'generated_worksheet.xmcd'
        template_ws_fp = os.path.join(Constants.TEMPLATE_DIR, template_file_name)
        src = template_ws_fp
        dst = os.path.join(self.output_dir_path, template_file_name)

        if os.path.exists(template_ws_fp):
            try:
                copyfile(src, dst)
                template_ws_fp = dst
            except FileExistsError as e:
                self.logger.warn(e)
            except SameFileError as e:
                self.logger.warn(e)
        else:
            template_ws_fp = None

        return template_ws_fp