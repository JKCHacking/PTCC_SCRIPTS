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
        data_dict = temp_dict = {}
        attrs = ["facsimileTelephoneNumber",
                 "cn",
                 "st",
                 "street",
                 "email",
                 "mail",
                 "mobile",
                 "registeredAddress",
                 "telephoneNumber"]

        with open(data_file_path, "r") as data:
            data_lines = data.readlines()
            for line in data_lines:
                if line.startswith("dn"):
                    levels = line.split(":")[1].strip()
                    levels_split = levels.split(",")
                    levels_split_cleaned = list(map(lambda x: x.replace("ou=", "").replace("dc=", "").replace("cn=", ""), levels_split))
                    for level in reversed(levels_split_cleaned):
                        try:
                            _data_dict = data_dict[level]
                        except KeyError:
                            temp_dict[level] = {}
                            temp_dict = temp_dict[level]
        print(data_dict)

    def key_exists(self, d, ks):
        _d = d
        for k in ks:
            try:
                _d = _d[k]
            except KeyError:
                return False
        return True