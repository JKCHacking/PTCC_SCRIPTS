import os
import re
import shutil


if __name__ == "__main__":
    # the directory that contains all the dwg files along with its directory.
    source_directory = os.path.join("X:\\Development\\CHRISTIAN POHL GmbH\\250 SOUTH ST\\05 SUBMISSION")
    destination_directory = os.path.join("H:\\Desktop\\projects\\dwg_table_extraction")

    str_pattern = ".*DL.*.dwg"  # change regex to the files you want to copy.
    file_reg_pattern = re.compile(str_pattern)
    for dir_path, dir_names, file_names in os.walk(source_directory):
        for file_name in file_names:
            file_fp = os.path.join(dir_path, file_name)
            if re.match(file_reg_pattern, file_name):
                temp_dir = dir_path
                new_path = temp_dir.replace(source_directory + os.path.sep, '')
                directory_list = new_path.split(os.path.sep)

                concat_dir = ''
                folder_str = ''
                for directory in directory_list:
                    concat_dir = os.path.join(concat_dir, directory)
                    folder_str = os.path.join(destination_directory, concat_dir)
                    if not os.path.exists(folder_str):
                        os.mkdir(folder_str)
                source_fp = file_fp
                dest_fp = os.path.join(folder_str, file_name)
                print(f"Copying: {file_name} to {folder_str}")
                shutil.copyfile(source_fp, dest_fp)
