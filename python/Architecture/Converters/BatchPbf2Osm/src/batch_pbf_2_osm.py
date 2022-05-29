import os
import subprocess
from src.util.constants import Constants


class Script:
    def iter_input(self):
        input_dir = Constants.INPUT_DIR
        for dir_path, dir_names, file_names in os.walk(input_dir):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(Constants.PBF_FILE_EXT):
                    print(f"Working on PBF File: {file_name}")
                    osm_file = os.path.splitext(file_name)[0]
                    output_file = os.path.join(Constants.OUTPUT_DIR, osm_file)
                    subprocess.run(['pbftoosm.exe', '<', file_full_path, '>', output_file], shell=True, check=True)
