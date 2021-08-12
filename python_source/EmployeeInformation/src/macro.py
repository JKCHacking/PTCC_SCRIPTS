# -*- coding: utf-8 -*-
import uno, unohelper
import msgbox as util
import datetime
from com.sun.star.awt import XActionListener


class AddEmployeeButtonListener(unohelper.Base, XActionListener):
    def __init__(self, dialog, controller):
        self.add_emp_dialog = dialog
        self.add_emp_controller = controller

    def actionPerformed(self, actionEvent):
        id_num_text_model = self.add_emp_dialog.dialog.getModel().getByName("id_num_text")
        surname_text_model = self.add_emp_dialog.dialog.getModel().getByName("surname_text")
        firstname_text_model = self.add_emp_dialog.dialog.getModel().getByName("firstname_text")
        middlename_text_model = self.add_emp_dialog.dialog.getModel().getByName("middlename_text")

        id_num = id_num_text_model.Text
        surname = surname_text_model.Text
        firstname = firstname_text_model.Text
        middlename = middlename_text_model.Text

        # setting Surname, Firstname, Middle name format
        name = "{}, {} {}".format(surname, firstname, middlename)
        if self.add_emp_controller.check_input(id_num, surname, firstname, middlename):
            self.add_emp_controller.create_new_employee_sheet(id_num, name)
            self.add_emp_controller.add_to_master(id_num, name)
            self.add_emp_dialog.dialog.endExecute()


class AddEmployeeDlg(unohelper.Base):
    def __init__(self, context):
        self.ctx = context
        self.dialog = None

    def create_dialog(self):
        label_width = 40
        label_height = 10
        text_height = 15
        text_width = 125
        label_x = 5  # start x
        label_y = 20  # start y
        label_text_margin = (text_height - label_height) / 2
        label_label_margin = 20
        label_labelnames = ["ID Number:", "Surname:", "First Name:", "Middle Name:"]
        label_idnames = ["id_number_label", "surname_label", "firstname_label", "middlename_label"]
        text_idnames = ["id_num_text", "surname_text", "firstname_text", "middlename_text"]

        smgr = self.ctx.ServiceManager
        self.dialog = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialog", self.ctx)
        dialog_model = smgr.createInstanceWithContext('com.sun.star.awt.UnoControlDialogModel', self.ctx)
        dialog_model.PositionX = 400
        dialog_model.PositionY = 200
        dialog_model.Width = 190
        dialog_model.Height = 170
        dialog_model.Title = "Add Employee"
        # creating labels and edit texts
        for index, (label_name, text_idname, label_idname) in enumerate(
                zip(label_labelnames, text_idnames, label_idnames)):
            # create label
            label = dialog_model.createInstance("com.sun.star.awt.UnoControlFixedTextModel")
            label.PositionX = label_x
            label_position_y = label_y + (label_height + label_label_margin) * index
            label.PositionY = label_position_y
            label.Width = label_width
            label.Height = label_height
            label.Name = label_idname
            label.Label = label_name
            # create edit text
            edit_text = dialog_model.createInstance("com.sun.star.awt.UnoControlEditModel")
            text_position_x = label.PositionX + label_width + label_text_margin
            text_position_y = label.PositionY - label_text_margin
            edit_text.PositionX = text_position_x
            edit_text.PositionY = text_position_y
            edit_text.Width = text_width
            edit_text.Height = text_height
            edit_text.Name = text_idname
            # insert control models into the dialog model
            dialog_model.insertByName(label_idname, label)
            dialog_model.insertByName(text_idname, edit_text)
        # button
        add_button = dialog_model.createInstance("com.sun.star.awt.UnoControlButtonModel")
        add_button.PositionX = 65
        add_button.PositionY = 140
        add_button.Width = 60
        add_button.Height = 20
        add_button.Label = "Add"
        add_button.Name = "add_button"
        dialog_model.insertByName("add_button", add_button)

        # set the dialog model
        self.dialog.setModel(dialog_model)
        # create a peer
        toolkit = smgr.createInstanceWithContext("com.sun.star.awt.ExtToolkit", self.ctx)
        self.dialog.createPeer(toolkit, None)


class AddEmployeeController(unohelper.Base):
    def __init__(self, dialog):
        self.add_emp_dialog = dialog

    def show(self):
        # create GUI
        self.add_emp_dialog.create_dialog()
        self.__add_listeners()
        self.add_emp_dialog.dialog.execute()
        self.add_emp_dialog.dialog.dispose()

    def __add_listeners(self):
        control = self.add_emp_dialog.dialog.getControl('add_button')
        listener = AddEmployeeButtonListener(self.add_emp_dialog, self)
        control.addActionListener(listener)

    def add_to_master(self, id_num, name):
        # assuming input data are valid.
        doc = XSCRIPTCONTEXT.getDocument()
        master_sheet = doc.Sheets['Master List']
        row = self.__get_last_used_row_by_col(master_sheet, 4, 0)

        # setting cell values with their formulas
        master_sheet.getCellByPosition(0, row).setString(id_num)
        master_sheet.getCellByPosition(1, row).setString(name)

    def create_new_employee_sheet(self, id_num, name):
        # copy template sheet
        doc = XSCRIPTCONTEXT.getDocument()
        new_employee_sheet_name = "{} {}".format(name, id_num)
        all_sheets = doc.Sheets
        # get the alphabetical position of the new sheet created
        position = self.__get_sheet_index(new_employee_sheet_name, all_sheets) + 4  # 4 permanent sheets
        # create a new sheet based on the template sheet.
        doc.Sheets.copyByName('Employee Information Template', new_employee_sheet_name, position)
        new_sheet = all_sheets[new_employee_sheet_name]
        # since by default the template sheet in protected we have to unprotect it.
        new_sheet.unprotect("")
        new_sheet.getCellByPosition(1, 3).setString(id_num)
        new_sheet.getCellByPosition(1, 4).setString(name)
        # we have to protect the sheet from unwanted changes to cells
        new_sheet.protect("")

    def __get_last_used_row_by_col(self, sheet, start_row, col):
        # detect last used row in a specific column.
        row = start_row
        while True:
            cell = sheet.getCellByPosition(col, row)
            if not cell.getString():
                break
            row += 1
        return row

    def __check_id_exists(self, id_num):
        # get the master sheet
        doc = XSCRIPTCONTEXT.getDocument()
        master_sheet = doc.Sheets["Master List"]
        id_num_col = 0
        id_num_row = 4
        found = False
        while True:
            cell = master_sheet.getCellByPosition(id_num_col, id_num_row)
            if id_num == cell.getString():
                found = True
                break
            elif not cell.getString():
                break
            id_num_row += 1
        return found

    def check_input(self, id_num, surname, firstname, middlename):
        ok = True
        # check if id_num already exists
        if not id_num or not surname or not firstname or not middlename:
            MsgBox("Please input all fields.")
            ok = False
        elif not id_num.isnumeric():
            MsgBox("ID Number must be numbers.")
            ok = False
        elif self.__check_id_exists(id_num):
            MsgBox("ID Number already exists.")
            ok = False
        return ok

    def __get_sheet_index(self, sheet_name, all_sheets):
        employee_sheet_name_list = []
        for sheet in all_sheets:
            if sheet.Name != "Resigned" and sheet.Name != "Master List" \
                    and sheet.Name != "Employee Information Template" and sheet.Name != "Cache":
                employee_sheet_name_list.append(sheet.Name)
        employee_sheet_name_list.append(sheet_name)
        sorted_sheet_name_list = sorted(employee_sheet_name_list)
        return sorted_sheet_name_list.index(sheet_name)


class SaveEmployee(unohelper.Base):

    def update(self):
        ret = 1
        doc = XSCRIPTCONTEXT.getDocument()
        current_sheet = doc.getCurrentController().getActiveSheet()
        master_sheet = doc.Sheets["Master List"]
        current_sheet.unprotect("")
        # check if there are new values for id_num and name
        # update the id_num and name in the masterlist
        new_id_num = current_sheet.getCellByPosition(2, 3).getString()
        new_name = current_sheet.getCellByPosition(2, 4).getString()
        # get the old id number
        old_id_num = current_sheet.getCellByPosition(1, 3).getString()
        old_name = current_sheet.getCellByPosition(1, 4).getString()

        if new_id_num:
            # search if new id_num already exists in the masterlist
            found_flag, id_num_pos = self.__search_id_num(new_id_num)
            if not found_flag:
                # search for the old id number to be updated to the new id number
                found_flag, id_num_pos = self.__search_id_num(old_id_num)
                if found_flag:
                    master_sheet.getCellByPosition(0, id_num_pos).setString(new_id_num)
                    current_sheet.getCellByPosition(1, 3).setString(new_id_num)
                    current_sheet.setName("{} {}".format(old_name, new_id_num))
                    if new_name:
                        master_sheet.getCellByPosition(1, id_num_pos).setString(new_name)
                        current_sheet.getCellByPosition(1, 4).setString(new_name)
                        current_sheet.setName("{} {}".format(new_name, new_id_num))
                else:
                    MsgBox("Cannot find the old ID number.")
                    ret = -1
            else:
                MsgBox("Input ID Number already exists in the master list.")
                ret = -1
        else:
            if new_name:
                # search for the old id number to update the old name to the new name
                found_flag, id_num_pos = self.__search_id_num(old_id_num)
                if found_flag:
                    master_sheet.getCellByPosition(1, id_num_pos).setString(new_name)
                    current_sheet.getCellByPosition(1, 4).setString(new_name)
                    current_sheet.getCellByPosition(2, 4).setString(new_name)
                    current_sheet.setName("{} {}".format(new_name, old_id_num))
                else:
                    MsgBox("Cannot find the old ID number.")
                    ret = -1
        # update others
        for i in range(5, 16):
            new_value = current_sheet.getCellByPosition(2, i).getString()
            if new_value:
                current_sheet.getCellByPosition(1, i).setString(new_value)

        # empty the New cells again
        for i in range(3, 16):
            current_sheet.getCellByPosition(2, i).setString("")
        current_sheet.protect("")
        return ret

    def save(self):
        doc = XSCRIPTCONTEXT.getDocument()
        doc.storeToURL(doc.URL, ())
        MsgBox("Successfully saved and updated.")

    def __search_id_num(self, id_num):
        # get the master sheet
        doc = XSCRIPTCONTEXT.getDocument()
        master_sheet = doc.Sheets["Master List"]
        id_num_col = 0
        id_num_row = 4
        found = False
        while True:
            cell = master_sheet.getCellByPosition(id_num_col, id_num_row)
            if id_num == cell.getString():
                found = True
                break
            elif not cell.getString():
                break
            id_num_row += 1
        return found, id_num_row


class DeleteEmployeeDlg(unohelper.Base):
    def __init__(self, context):
        self.ctx = context
        self.dialog = None

    def create_dialog(self):
        smgr = self.ctx.ServiceManager
        self.dialog = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialog", self.ctx)
        dialog_model = smgr.createInstanceWithContext('com.sun.star.awt.UnoControlDialogModel', self.ctx)
        dialog_model.PositionX = 400
        dialog_model.PositionY = 200
        dialog_model.Width = 150
        dialog_model.Height = 45
        dialog_model.Title = "Delete Employee"

        label = dialog_model.createInstance("com.sun.star.awt.UnoControlFixedTextModel")
        label.PositionX = 25
        label.PositionY = 10
        label.Width = 100
        label.Height = 10
        label.Name = "confirmation_label"
        label.Label = "Are you sure you want to delete?"

        yes_btn = dialog_model.createInstance("com.sun.star.awt.UnoControlButtonModel")
        yes_btn.PositionX = 25
        yes_btn.PositionY = 25
        yes_btn.Width = 25
        yes_btn.Height = 15
        yes_btn.Name = "yes_btn"
        yes_btn.Label = "YES"

        no_btn = dialog_model.createInstance("com.sun.star.awt.UnoControlButtonModel")
        no_btn.PositionX = 100
        no_btn.PositionY = 25
        no_btn.Width = 25
        no_btn.Height = 15
        no_btn.Name = "no_btn"
        no_btn.Label = "NO"

        dialog_model.insertByName("confirmation_label", label)
        dialog_model.insertByName("yes_btn", yes_btn)
        dialog_model.insertByName("no_btn", no_btn)

        # set the dialog model
        self.dialog.setModel(dialog_model)
        # create a peer
        toolkit = smgr.createInstanceWithContext("com.sun.star.awt.ExtToolkit", self.ctx)
        self.dialog.createPeer(toolkit, None)


class DeleteEmployeeBtnListener(unohelper.Base, XActionListener):
    def __init__(self, dialog, controller):
        self.delete_emp_dialog = dialog
        self.delete_emp_controller = controller

    def actionPerformed(self, actionEvent):
        if actionEvent.Source.Model.Name == "yes_btn":
            self.delete_emp_controller.delete()
            self.delete_emp_dialog.dialog.endExecute()
        elif actionEvent.Source.Model.Name == "no_btn":
            self.delete_emp_dialog.dialog.endExecute()


class DeleteEmployeeController(unohelper.Base):
    def __init__(self, dialog):
        self.delete_emp_dialog = dialog

    def show(self):
        # create GUI
        self.delete_emp_dialog.create_dialog()
        self.__add_listeners()
        self.delete_emp_dialog.dialog.execute()
        self.delete_emp_dialog.dialog.dispose()

    def __add_listeners(self):
        # add yes button listener
        control = self.delete_emp_dialog.dialog.getControl('yes_btn')
        listener = DeleteEmployeeBtnListener(self.delete_emp_dialog, self)
        control.addActionListener(listener)
        # add no button listener
        control = self.delete_emp_dialog.dialog.getControl('no_btn')
        listener = DeleteEmployeeBtnListener(self.delete_emp_dialog, self)
        control.addActionListener(listener)

    def __get_last_used_row_by_col(self, sheet, start_row, col):
        # detect last used row in a specific column.
        row = start_row
        while True:
            cell = sheet.getCellByPosition(col, row)
            if not cell.getString():
                break
            row += 1
        return row

    def __search_id_num(self, id_num):
        # get the master sheet
        doc = XSCRIPTCONTEXT.getDocument()
        master_sheet = doc.Sheets["Master List"]
        id_num_col = 0
        id_num_row = 4
        found = False
        while True:
            cell = master_sheet.getCellByPosition(id_num_col, id_num_row)
            if id_num == cell.getString():
                found = True
                break
            elif not cell.getString():
                break
            id_num_row += 1
        return found, id_num_row

    def delete(self):
        # copy all the employee data
        doc = XSCRIPTCONTEXT.getDocument()
        current_sheet = doc.getCurrentController().getActiveSheet()
        # employee data
        id_num = current_sheet.getCellByPosition(1, 3).getString()
        name = current_sheet.getCellByPosition(1, 4).getString()
        address = current_sheet.getCellByPosition(1, 5).getString()
        contact = current_sheet.getCellByPosition(1, 6).getString()
        birthday = current_sheet.getCellByPosition(1, 7).getString()
        position = current_sheet.getCellByPosition(1, 8).getString()
        date_hired = current_sheet.getCellByPosition(1, 9).getString()
        department = current_sheet.getCellByPosition(1, 10).getString()
        date_of_resignation = current_sheet.getCellByPosition(1, 11).getString()
        tin = current_sheet.getCellByPosition(1, 12).getString()
        sss = current_sheet.getCellByPosition(1, 13).getString()
        philhealth = current_sheet.getCellByPosition(1, 14).getString()
        pagibig = current_sheet.getCellByPosition(1, 15).getString()

        # paste in the resigned employee table
        resigned_sheet = doc.Sheets["Resigned"]
        row_to_add = self.__get_last_used_row_by_col(resigned_sheet, 4, 0)
        resigned_sheet.getCellByPosition(0, row_to_add).setString(id_num)
        resigned_sheet.getCellByPosition(1, row_to_add).setString(name)
        resigned_sheet.getCellByPosition(2, row_to_add).setString(address)
        resigned_sheet.getCellByPosition(3, row_to_add).setString(contact)
        resigned_sheet.getCellByPosition(4, row_to_add).setString(birthday)
        resigned_sheet.getCellByPosition(5, row_to_add).setString(position)
        resigned_sheet.getCellByPosition(6, row_to_add).setString(date_hired)
        resigned_sheet.getCellByPosition(7, row_to_add).setString(department)
        resigned_sheet.getCellByPosition(8, row_to_add).setString(date_of_resignation)
        resigned_sheet.getCellByPosition(9, row_to_add).setString(tin)
        resigned_sheet.getCellByPosition(10, row_to_add).setString(sss)
        resigned_sheet.getCellByPosition(11, row_to_add).setString(philhealth)
        resigned_sheet.getCellByPosition(12, row_to_add).setString(pagibig)

        # remove from the master list
        found, id_num_row = self.__search_id_num(id_num)
        if found:
            master_sheet = doc.Sheets["Master List"]
            rows = master_sheet.getRows()
            rows.removeByIndex(id_num_row, 1)
            # delete the sheet
            current_sheet.unprotect("")
            doc.Sheets.removeByName(current_sheet.Name)
        else:
            MsgBox("Cannot find ID Number in Master List.")


class RestoreEmployeeDlg(unohelper.Base):
    def __init__(self, context):
        self.ctx = context
        self.dialog = None

    def create_dialog(self):
        smgr = self.ctx.ServiceManager
        self.dialog = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialog", self.ctx)
        dialog_model = smgr.createInstanceWithContext('com.sun.star.awt.UnoControlDialogModel', self.ctx)
        dialog_model.PositionX = 400
        dialog_model.PositionY = 200
        dialog_model.Width = 200
        dialog_model.Height = 70
        dialog_model.Title = "Restore Employee"

        label = dialog_model.createInstance("com.sun.star.awt.UnoControlFixedTextModel")
        label.PositionX = 15
        label.PositionY = 20
        label.Width = 30
        label.Height = 10
        label.Name = "idnum_label"
        label.Label = "ID Number:"

        idnum_text = dialog_model.createInstance("com.sun.star.awt.UnoControlEditModel")
        idnum_text.PositionX = label.PositionX + label.Width + 2.5
        idnum_text.PositionY = label.PositionY - 2.5
        idnum_text.Width = 125
        idnum_text.Height = 15
        idnum_text.Name = "idnum_text"

        ok_btn = dialog_model.createInstance("com.sun.star.awt.UnoControlButtonModel")
        ok_btn.PositionX = idnum_text.PositionX + (idnum_text.Width / 4)
        ok_btn.PositionY = idnum_text.PositionY + idnum_text.Height + 10
        ok_btn.Width = 50
        ok_btn.Height = 15
        ok_btn.Name = "ok_btn"
        ok_btn.Label = "OK"

        dialog_model.insertByName("idnum_label", label)
        dialog_model.insertByName("idnum_text", idnum_text)
        dialog_model.insertByName("ok_btn", ok_btn)
        # set the dialog model
        self.dialog.setModel(dialog_model)
        # create a peer
        toolkit = smgr.createInstanceWithContext("com.sun.star.awt.ExtToolkit", self.ctx)
        self.dialog.createPeer(toolkit, None)


class RestoreEmployeeBtnListener(unohelper.Base, XActionListener):
    def __init__(self, dialog, controller):
        self.restore_emp_dialog = dialog
        self.restore_emp_controller = controller

    def actionPerformed(self, event):
        idnum = self.restore_emp_dialog.dialog.getModel().getByName("idnum_text").Text
        # locate employee using id number
        found, row = self.restore_emp_controller.search_id_num(idnum)
        if found:
            self.restore_emp_controller.restore(idnum, row)
            self.restore_emp_dialog.dialog.endExecute()
        else:
            MsgBox("Cannot find ID Number.")


class RestoreEmployeeController(unohelper.Base):
    def __init__(self, dialog):
        self.restore_emp_dialog = dialog

    def show(self):
        # create GUI
        self.restore_emp_dialog.create_dialog()
        self.__add_listeners()
        self.restore_emp_dialog.dialog.execute()
        self.restore_emp_dialog.dialog.dispose()

    def __add_listeners(self):
        # add yes button listener
        control = self.restore_emp_dialog.dialog.getControl('ok_btn')
        listener = RestoreEmployeeBtnListener(self.restore_emp_dialog, self)
        control.addActionListener(listener)

    def search_id_num(self, id_num):
        # get the master sheet
        doc = XSCRIPTCONTEXT.getDocument()
        resigned_sheet = doc.Sheets["Resigned"]
        id_num_col = 0
        id_num_row = 4
        found = False
        while True:
            cell = resigned_sheet.getCellByPosition(id_num_col, id_num_row)
            if id_num == cell.getString():
                found = True
                break
            elif not cell.getString():
                break
            id_num_row += 1
        return found, id_num_row

    def restore(self, idnum, row):
        # copy data
        doc = XSCRIPTCONTEXT.getDocument()
        resigned_sheet = doc.Sheets["Resigned"]
        id_number = idnum
        name = resigned_sheet.getCellByPosition(1, row).getString()
        address = resigned_sheet.getCellByPosition(2, row).getString()
        contact = resigned_sheet.getCellByPosition(3, row).getString()
        birthday = resigned_sheet.getCellByPosition(4, row).getString()
        position = resigned_sheet.getCellByPosition(5, row).getString()
        date_hired = resigned_sheet.getCellByPosition(6, row).getString()
        department = resigned_sheet.getCellByPosition(7, row).getString()
        date_of_resignation = resigned_sheet.getCellByPosition(8, row).getString()
        tin = resigned_sheet.getCellByPosition(9, row).getString()
        sss = resigned_sheet.getCellByPosition(10, row).getString()
        philhealth = resigned_sheet.getCellByPosition(11, row).getString()
        pagibig = resigned_sheet.getCellByPosition(12, row).getString()

        add_employee_controller = AddEmployeeController(None)
        # create new employee sheet
        add_employee_controller.create_new_employee_sheet(id_number, name)
        # add data to sheet
        new_sheet_name = "{} {}".format(name, id_number)
        new_sheet = doc.Sheets[new_sheet_name]
        new_sheet.unprotect("")
        new_sheet.getCellByPosition(1, 3).setString(id_number)
        new_sheet.getCellByPosition(1, 4).setString(name)
        new_sheet.getCellByPosition(1, 5).setString(address)
        new_sheet.getCellByPosition(1, 6).setString(contact)
        new_sheet.getCellByPosition(1, 7).setString(birthday)
        new_sheet.getCellByPosition(1, 8).setString(position)
        new_sheet.getCellByPosition(1, 9).setString(date_hired)
        new_sheet.getCellByPosition(1, 10).setString(department)
        new_sheet.getCellByPosition(1, 11).setString(date_of_resignation)
        new_sheet.getCellByPosition(1, 12).setString(tin)
        new_sheet.getCellByPosition(1, 13).setString(sss)
        new_sheet.getCellByPosition(1, 14).setString(philhealth)
        new_sheet.getCellByPosition(1, 15).setString(pagibig)
        new_sheet.protect("")
        # add data to masterlist
        add_employee_controller.add_to_master(idnum, name)
        # delete entry in resigned sheet
        rows = resigned_sheet.getRows()
        rows.removeByIndex(row, 1)

# ============================= FUNCTIONS ===========================================


def add_employee(*args):
    ctx = uno.getComponentContext()
    add_emp_dlg = AddEmployeeDlg(ctx)
    add_emp_ctlr = AddEmployeeController(add_emp_dlg)
    add_emp_ctlr.show()


def save_employee(*args):
    save_emp_ctrl = SaveEmployee()
    ret = save_emp_ctrl.update()
    if ret == 1:
        save_emp_ctrl.save()


def delete_employee(*args):
    ctx = uno.getComponentContext()
    delete_emp_dlg = DeleteEmployeeDlg(ctx)
    delete_emp_ctlr = DeleteEmployeeController(delete_emp_dlg)
    delete_emp_ctlr.show()


def restore_employee(*args):
    ctx = uno.getComponentContext()
    restore_emp_dlg = RestoreEmployeeDlg(ctx)
    restore_emp_ctlr = RestoreEmployeeController(restore_emp_dlg)
    restore_emp_ctlr.show()


def filter_employee_info(event):
    column_list = ["ADDRESS",
                   "CONTACT",
                   "BIRTHDAY",
                   "POSITION",
                   "DATE HIRED",
                   "DEPARTMENT",
                   "DATE OF RESIGNATION",
                   "TIN",
                   "SSS",
                   "PHILHEALTH",
                   "PAG-IBIG",
                   "YEARS OF SERVICE"]

    doc = XSCRIPTCONTEXT.getDocument()
    master_sheet = doc.Sheets["Master List"]
    # set the empty column to the current selected info
    selected_info = event.Source.Model.CurrentValue
    master_sheet.getCellByPosition(2, 3).setString(selected_info)

    # loop through each id and name and get their respective value in their corresponding sheets.
    row = 4
    while True:
        id = master_sheet.getCellByPosition(0, row).getString()
        name = master_sheet.getCellByPosition(1, row).getString()
        if not id:
            break
        if selected_info != "":
            sheet_name = "{} {}".format(name, id)
            sheet = doc.Sheets[sheet_name]
            if selected_info == "YEARS OF SERVICE":
                # get the date hired
                date_hired = sheet.getCellByPosition(1, 9).getString()
                # convert this to datetime object
                date_hired_obj = datetime.datetime.strptime(date_hired, "%d-%b-%Y")
                # subtract to now
                diff_delta = datetime.datetime.now() - date_hired_obj
                diff_years = (diff_delta.days + diff_delta.seconds / 86400) / 365.2425
                info_value = round(diff_years, 2)
            else:
                info_row = column_list.index(selected_info) + 5  # add offset for title, id number and name.
                info_value = sheet.getCellByPosition(1, info_row).getString()
            # put it to the respective row
            master_sheet.getCellByPosition(2, row).setString(info_value)
        else:
            master_sheet.getCellByPosition(2, row).setString("")
        row += 1


def MsgBox(txt):
    mb = util.MsgBox(uno.getComponentContext())
    mb.addButton("OK")
    mb.show(txt, 0, "Message")


g_exportedScripts = (add_employee, save_employee, delete_employee, filter_employee_info,
                     restore_employee)
