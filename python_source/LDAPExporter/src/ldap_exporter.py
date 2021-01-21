import os
from src.util.constants import Constants
from src.document import WordDocument


class LdapExporter:
    def __init__(self):
        self.file_name = ""

    def convert_ldap_data(self, data_file_path):
        # get the filename only
        self.file_name = os.path.basename(data_file_path)
        data_dict = {}
        attrs = ["facsimileTelephoneNumber",
                 "st",
                 "street",
                 "email",
                 "mail",
                 "mobile",
                 "registeredAddress",
                 "telephoneNumber"]

        with open(data_file_path, "r") as data:
            data_lines = data.readlines()
            levels_split_cleaned = ""
            for line in data_lines:
                if line.startswith("dn"):
                    levels = line.split(":")[1].strip()
                    levels_split = levels.split(",")
                    levels_split_cleaned = list(
                        map(lambda x: x.replace("ou=", "").replace("dc=", "").replace("cn=", "").replace("o=", ""),
                            levels_split))

                    # this will create a dictionary from a list. it checks if the combination of keys
                    # in the list already exists inside the nested dictionary. if not it adds it
                    # inside the nested dictionary.
                    _data_dict = data_dict
                    for level in reversed(levels_split_cleaned):
                        try:
                            _data_dict = _data_dict[level]
                        except KeyError:
                            _data_dict[level] = {}
                            _data_dict = _data_dict[level]

                else:
                    for attr in attrs:
                        if line.startswith(attr):
                            value = line.split(attr + ":")[1]
                            key = attr.strip()
                            value = value.strip()

                            _data_dict = data_dict
                            for level in reversed(levels_split_cleaned):
                                _data_dict = _data_dict[level]
                            if key in _data_dict:
                                if not isinstance(_data_dict[key], list):
                                    _data_dict[key] = [_data_dict[key]]
                                _data_dict[key].append(value)
                            else:
                                _data_dict[key] = value
            return data_dict

    def sort_data(self, raw_data_dict):
        """
        sorts a nested dictionary with its key.
        source: https://gist.github.com/gyli/f60f0374defc383aa098d44cfbd318eb
        """
        return {k: self.sort_data(v) if isinstance(v, dict) else v for k, v in sorted(raw_data_dict.items())}

    def print_nested_dict(self, d):
        # prints all the keys and values of a dictionary
        for k, v in d.items():
            if isinstance(v, dict):
                yield k
                yield from self.print_nested_dict(v)
            else:
                yield k, v

    def export_data(self, data_dict):
        output_path = os.path.join(Constants.OUTPUT_DIR, os.path.splitext(self.file_name)[0] + ".docx")
        root_data_dict = data_dict['design']['ptcc']

        document = WordDocument()
        doc = document.create_document()
        par = document.add_paragraph(doc)
        for entry in self.print_nested_dict(root_data_dict):
            if isinstance(entry, tuple):
                key, value = entry
                if isinstance(value, list):
                    value = "/\n".join(value)
                    text = "{}:\n{}\n".format(key, value)
                else:
                    text = "{}: {}\n".format(key, value)
                bold = False
            else:
                text = "\n" + entry + "\n"
                bold = True
            document.add_paragraph_text(par, text, bold)
        document.save_document(doc, output_path)
