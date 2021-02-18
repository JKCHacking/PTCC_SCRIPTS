# -*- coding: utf-8 -*-
import uno, unohelper
import msgbox as util
# from apso_utils import msgbox
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
            self.add_emp_controller.add_to_master(id_num, name)
            self.add_emp_controller.create_new_employee_sheet(id_num, name)
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
        dialog_model.Height = 200
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
        add_button.PositionY = 165
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

        # setting cell values
        cell = master_sheet.getCellByPosition(0, row)
        cell.setString(id_num)
        cell = master_sheet.getCellByPosition(1, row)
        cell.setString(name)

    def create_new_employee_sheet(self, id_num, name):
        # copy template sheet
        doc = XSCRIPTCONTEXT.getDocument()
        new_employee_sheet_name = "{}_{}".format(name, id_num)
        all_sheets = doc.Sheets
        sheet_count = all_sheets.Count
        # create a new sheet based on the template sheet.
        doc.Sheets.copyByName('Employee Information Template', new_employee_sheet_name, sheet_count)
        new_sheet = all_sheets[new_employee_sheet_name]
        cache_sheet = all_sheets["Cache"]

        idnum_cell = new_sheet.getCellByPosition(1, 1)
        tempidnum_cell = cache_sheet.getCellByPosition(0, 0)
        name_cell = new_sheet.getCellByPosition(1, 2)

        name_cell.setString(name)
        idnum_cell.setString(id_num)
        tempidnum_cell.setString(id_num)
        self.__add_event_macro(new_employee_sheet_name)

    def __add_event_macro(self, sheet_name):
        event_properties = list(range(2))
        event_properties[0] = uno.createUnoStruct('com.sun.star.beans.PropertyValue')
        event_properties[0].Name = "EventType"
        event_properties[0].Value = "Script"
        event_properties[1] = uno.createUnoStruct('com.sun.star.beans.PropertyValue')
        event_properties[1].Name = "Script"
        event_properties[1].Value = "vnd.sun.star.script:macro.py$add_data_to_cache?language=Python&location=user"

        doc = XSCRIPTCONTEXT.getDocument()
        all_sheets = doc.Sheets
        new_sheet = all_sheets[sheet_name]
        uno.invoke(
            new_sheet.Events,
            "replaceByName",
            ("OnFocus", uno.Any("[]com.sun.star.beans.PropertyValue", tuple(event_properties))))

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


class SaveEmployee(unohelper.Base):

    def update(self):
        doc = XSCRIPTCONTEXT.getDocument()
        current_sheet = doc.getCurrentController().getActiveSheet()
        master_sheet = doc.Sheets["Master List"]
        cache_sheet = doc.Sheets["Cache"]

        name_cell_curr = current_sheet.getCellByPosition(1, 1)
        idnum_cell_curr = current_sheet.getCellByPosition(1, 2)
        tempidnum_cell_curr = cache_sheet.getCellByPosition(0, 0)  # A1
        position_cell_curr = current_sheet.getCellByPosition(1, 3)

        new_name = name_cell_curr.getString()
        new_idnum = idnum_cell_curr.getString()
        temp_idnum = tempidnum_cell_curr.getString()
        new_position = position_cell_curr.getString()

        # check look for the current temp id in the masterlist
        found_tempid, id_num_row_temp = self.__search_id_num(temp_idnum)
        if found_tempid:
            # check if the new id number exists
            found_newid, id_num_row_new = self.__search_id_num(new_idnum)
            if not found_newid:
                idnum_cell_master = master_sheet.getCellByPosition(0, id_num_row_temp)
                name_cell_master = master_sheet.getCellByPosition(1, id_num_row_temp)
                position_cell_master = master_sheet.getCellByPosition(2, id_num_row_temp)

                idnum_cell_master.setString(new_idnum)
                tempidnum_cell_curr.setString(new_idnum)
                name_cell_master.setString(new_name)
                position_cell_master.setString(new_position)
                new_sheet_name = "{}_{}".format(new_name, new_idnum)
                current_sheet.Name = new_sheet_name
                ret = 1
            else:
                MsgBox("The new ID Number already exists in the Master List")
                # set it back to the previous value.
                idnum_cell_curr.setString(temp_idnum)
                ret = -1
        else:
            MsgBox("Employee does not exists in the Master list.")
            ret = -1
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
        pass


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
        control = self.delete_emp_dialog.dialog.getControl('yes_btn')
        listener = DeleteEmployeeBtnListener(self.delete_emp_dialog, self)
        control.addActionListener(listener)
        control = self.delete_emp_dialog.dialog.getControl('no_btn')
        listener = DeleteEmployeeBtnListener(self.delete_emp_dialog, self)
        control.addActionListener(listener)


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


def MsgBox(txt):
    mb = util.MsgBox(uno.getComponentContext())
    mb.addButton("OK")
    mb.show(txt, 0, "Message")


def add_data_to_cache(*args):
    doc = XSCRIPTCONTEXT.getDocument()
    current_sheet = doc.getCurrentController().getActiveSheet()
    cache_sheet = doc.Sheets["Cache"]
    id_number_cell = current_sheet.getCellByPosition(1, 2)
    cell_cache = cache_sheet.getCellByPosition(0, 0)
    cell_cache.setString(id_number_cell.getString())


g_exportedScripts = (add_employee, save_employee, delete_employee, add_data_to_cache)
