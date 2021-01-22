import os
from src.ldap_exporter import LdapExporter
from src.util.constants import Constants


def iter_input():
    input_dir = Constants.INPUT_DIR
    le = LdapExporter()
    for dir_path, dir_names, file_names in os.walk(input_dir):
        for file_name in file_names:
            file_full_path = os.path.join(dir_path, file_name)
            if file_full_path.endswith(Constants.LDIF_FILE_EXT):
                # convert ldap data to dictionary
                ldap_data_dict = le.convert_ldap_data(file_full_path)
                # sort data alphabetically
                ldap_data_dict = le.sort_data(ldap_data_dict)
                # export data to a document
                le.export_data(ldap_data_dict)


if __name__ == "__main__":
    iter_input()
