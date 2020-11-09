import os
import csv
import openpyxl
from src.util.constants import Constants
from src.util.watcher import Watcher


class LDAPGenerator:
    def __init__(self):
        pass

    def iter_input(self):
        input_dir = Constants.INPUT_DIR
        for dir_path, dir_names, file_names in os.walk(input_dir):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(Constants.CSV_FILE_EXT):
                    data = self.get_csv_data(file_full_path)
                    # sort data according to first element
                    data.sort()
                    filename_ext = os.path.basename(file_full_path)
                    filename = os.path.splitext(filename_ext)[0]
                    output_dir = os.path.join(Constants.OUTPUT_DIR, filename + '.xlsx')
                    self.create_workbook(data, output_dir)

    def get_csv_data(self, file_full_path):
        data = []
        with open(file_full_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if "cn=" in row[0]:
                    row_data = []
                    # get the name of the contact
                    try:
                        contact_name = row[0].split(',')[0].lstrip("cn=")
                        row_data.append(contact_name)
                        street = row[1]
                        row_data.append(street)
                        city = row[2]
                        row_data.append(city)
                        country = row[3]
                        row_data.append(country)
                        fax = row[4]
                        row_data.append(fax)
                        tel_num = row[5]
                        row_data.append(tel_num)
                        mobile = row[6]
                        row_data.append(mobile)
                        email = row[7]
                        row_data.append(email)
                    except IndexError:
                        pass
                    data.append(row_data)
        return data

    def create_workbook(self, data, output_path):
        wb = openpyxl.workbook.Workbook()
        ws = None
        current_char = ''
        for row in data:
            contact_name = row[0]
            street = row[1]
            city = row[2]
            country = row[3]
            fax = row[4]
            tel_num = row[5]
            mobile = row[6]
            email = row[7]

            # this represent the starting letter of each names.
            watcher = Watcher(current_char)
            current_char = contact_name[0]
            watcher.set_value(current_char)
            if watcher.has_changed():
                if current_char.isnumeric():
                    ws_name = "123"
                else:
                    ws_name = current_char
                ws = wb.create_sheet(ws_name)
                ws.append([ws_name])
                ws.append([""])
            if contact_name:
                ws.append([contact_name])
            if street:
                ws.append([street])
            if city:
                ws.append([city])
            if country:
                ws.append([country])
            if fax:
                fax_list = fax.split("|")
                fax_text = "/\n".join(fax_list)
                ws.append([f"Fax: {fax_text}"])
            if tel_num:
                tel_num_list = tel_num.split("|")
                tel_num_text = "/\n".join(tel_num_list)
                ws.append([f"Telephone: {tel_num_text}"])
            if mobile:
                mobile_list = mobile.split("|")
                mobile_text = "/\n".join(mobile_list)
                ws.append([f"Mobile: {mobile_text}"])
            if email:
                email_list = email.split("|")
                email_text = "/\n".join(email_list)
                ws.append([f"E-Mail: {email_text}"])
            ws.append([""])

        if len(wb.worksheets) > 1:
            default_ws = wb["Sheet"]
            wb.remove(default_ws)
            wb.save(output_path)
