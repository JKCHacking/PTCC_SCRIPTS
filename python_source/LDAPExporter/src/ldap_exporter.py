import os
from src.util.constants import Constants


class LdapExporter:
    def iter_input(self):
        input_dir = Constants.INPUT_DIR
        for dir_path, dir_names, file_names in os.walk(input_dir):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(Constants.CSV_FILE_EXT):
                    pass

    def get_data(self, data_file_path):
        data_dict = {}
        attrs = ["facsimileTelephoneNumber", "cn", "st", "street", "email"]
        with open(data_file_path, "r") as data:
            data_lines = data.readlines()
            for line in data_lines:
                if line.startswith("dn"):
                    levels = line.split(":")[1].strip()
                    levels_split = levels.split(",")
                    for level in levels_split:
                        if level.startswith("ou"):
                            data_dict.update(
                                {
                                    level: {
                                        "member": []
                                    }
                                }
                            )

        print(data_dict)