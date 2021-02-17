# -*- coding: utf-8 -*-
import uno, unohelper
# import msgbox as util
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
        position_text_model = self.add_emp_dialog.dialog.getModel().getByName("position_text")

        id_num = id_num_text_model.Text
        surname = surname_text_model.Text
        firstname = firstname_text_model.Text
        middlename = middlename_text_model.Text
        position = position_text_model.Text

        name = "{}, {} {}".format(surname, firstname, middlename)
        if id_num and name and position:
            self.add_emp_controller.add_to_master(id_num, name, position)
            self.add_emp_controller.create_new_employee_sheet()
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
        label_labelnames = ["ID Number:", "Surname:", "First Name:", "Middle Name:", "Position"]
        label_idnames = ["id_number_label", "surname_label", "firstname_label", "middlename_label", "position_label"]
        text_idnames = ["id_num_text", "surname_text", "firstname_text", "middlename_text", "position_text"]

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
        self.add_listeners()
        self.add_emp_dialog.dialog.execute()
        self.add_emp_dialog.dialog.dispose()

    def add_listeners(self):
        control = self.add_emp_dialog.dialog.getControl('add_button')
        listener = AddEmployeeButtonListener(self.add_emp_dialog, self)
        control.addActionListener(listener)

    def add_to_master(self, id_num, name, position):
        # assuming input data are valid.
        doc = XSCRIPTCONTEXT.getDocument()
        master_sheet = doc.Sheets[0]
        row = self.get_last_used_row_by_col(master_sheet, 4, 0)

        # setting cell values
        cell = master_sheet.getCellByPosition(0, row)
        cell.setString(id_num)
        cell = master_sheet.getCellByPosition(1, row)
        cell.setString(name)
        cell = master_sheet.getCellByPosition(2, row)
        cell.setString(position)

    def create_new_employee_sheet(self):
        pass

    # def MsgBox(self, txt):
    #     mb = util.MsgBox(uno.getComponentContext())
    #     mb.addButton("OK")
    #     mb.show(txt, 0, "Python")

    def get_last_used_row_by_col(self, sheet, start_row, col):
        # detect last used row
        row = start_row
        while True:
            cell = sheet.getCellByPosition(col, row)
            if not cell.getString():
                break
            row += 1
        return row


def add_employee(*args):
    ctx = uno.getComponentContext()
    add_emp_dlg = AddEmployeeDlg(ctx)
    add_emp_ctlr = AddEmployeeController(add_emp_dlg)
    add_emp_ctlr.show()


g_exportedScripts = (add_employee,)

if __name__ == "__main__":
    add_employee()
