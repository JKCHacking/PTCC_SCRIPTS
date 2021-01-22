import os
import ldif
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

        with open(data_file_path, "rb") as ldif_file:
            parser = ldif.LDIFRecordList(ldif_file)
            parser.parse()
            for dn, entry in parser.all_records:
                levels = dn.split(',')
                # level clean up, this will prevent from having invalid level name
                levels = [level for level in levels if "=" in level]
                object_header = levels[0]
                object_name_index = object_header.split("=")[0]
                parent_levels = list(
                    map(lambda x: x.replace("ou=", "").replace("dc=", "").replace("cn=", "").replace("o=", ""),
                        levels[1:]))

                # we need to get the legit name of the object to be a key in the dictionary from the entry data.
                # for some reasons the name in the dn sometimes has weird characters in it.
                object_name = entry[object_name_index][0].decode('utf-8').strip()
                parent_levels.insert(0, object_name)

                # this will create a dictionary from a list. it checks if the combination of keys
                # in the list already exists inside the nested dictionary. if not it adds it
                # inside the nested dictionary.
                _data_dict = data_dict
                for levels in reversed(parent_levels):
                    try:
                        _data_dict = _data_dict[levels]
                    except KeyError:
                        _data_dict[levels] = {}
                        _data_dict = _data_dict[levels]
                # add the entry data on the current level
                for attr in attrs:
                    try:
                        # check if it has more that one entry, we need to retain the list
                        # but items must be converted from binary to string.
                        if len(entry[attr]) > 1:
                            temp_list = []
                            for item in entry[attr]:
                                temp_list.append(item.decode('utf-8'))
                            _data_dict[attr] = temp_list
                        else:
                            _data_dict[attr] = entry[attr][0].decode('utf-8')
                    except KeyError:
                        pass
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
