import shutil
import os


if __name__ == "__main__":
    current_dir = "H:\\Desktop\\fixed_student_version\\"
    storage_file_name = "dwg_list.txt"
    txt_file = os.path.join(current_dir, storage_file_name)

    with open(txt_file, "r") as file:
        list_path = file.read().splitlines()
        for path in list_path:
            src = path
            temp_path = path
            # remove H: / Desktop / projects / student_version_check / nbk / incyte_1703\
            new_path = temp_path.replace("H:/Desktop/projects/student_version_check/nbk/incyte_1703\\", '')
            head_tail = os.path.split(new_path)
            directory_str = head_tail[0]
            file_name = head_tail[1]
            folder_str = ''

            directory_list = directory_str.split(os.path.sep)
            for directory in directory_list:
                folder_str = os.path.join(folder_str, directory)
                folder = os.path.join(current_dir, folder_str)
                if not os.path.exists(folder):
                    os.mkdir(folder)
            dst = os.path.join(current_dir, new_path)
            print(f"{current_dir} + {new_path} = {dst}")
            shutil.copyfile(src, dst)
