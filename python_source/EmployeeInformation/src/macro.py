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
        name_text_model = self.add_emp_dialog.dialog.getModel().getByName("name_text")
        position_text_model = self.add_emp_dialog.dialog.getModel().getByName("position_text")

        id_num = id_num_text_model.Text
        name = name_text_model.Text
        position = position_text_model.Text

        if id_num and name and position:
            self.add_emp_controller.add_to_master(id_num, name, position)
            self.add_emp_controller.create_new_employee_sheet()
            self.add_emp_dialog.dialog.endExecute()


class AddEmployeeDlg(unohelper.Base):
    def __init__(self, context):
        self.ctx = context
        self.dialog = None

    def create_dialog(self):
        smgr = self.ctx.ServiceManager
        self.dialog = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialog", self.ctx)
        dialog_model = smgr.createInstanceWithContext('com.sun.star.awt.UnoControlDialogModel', self.ctx)
        dialog_model.PositionX = 100
        dialog_model.PositionY = 100
        dialog_model.Width = 200
        dialog_model.Height = 150
        dialog_model.Title = "Add Employee"

        # labels
        id_num_label = dialog_model.createInstance("com.sun.star.awt.UnoControlFixedTextModel")
        id_num_label.PositionX = 6
        id_num_label.PositionY = 19
        id_num_label.Width = 32
        id_num_label.Height = 10
        id_num_label.Name = "id_num_label"
        id_num_label.Label = "ID Number:"

        name_label = dialog_model.createInstance("com.sun.star.awt.UnoControlFixedTextModel")
        name_label.PositionX = 20
        name_label.PositionY = 46
        name_label.Width = 17
        name_label.Height = 12
        name_label.Name = "name_label"
        name_label.Label = "Name:"

        position_label = dialog_model.createInstance("com.sun.star.awt.UnoControlFixedTextModel")
        position_label.PositionX = 14
        position_label.PositionY = 74
        position_label.Width = 27
        position_label.Height = 12
        position_label.Name = "position_label"
        position_label.Label = "Position:"

        # edit texts
        id_num_text = dialog_model.createInstance("com.sun.star.awt.UnoControlEditModel")
        id_num_text.PositionX = 46
        id_num_text.PositionY = 15
        id_num_text.Width = 125
        id_num_text.Height = 17
        id_num_text.Name = "id_num_text"

        name_text = dialog_model.createInstance("com.sun.star.awt.UnoControlEditModel")
        name_text.PositionX = 46
        name_text.PositionY = 42
        name_text.Width = 125
        name_text.Height = 17
        name_text.Name = "name_text"

        position_text = dialog_model.createInstance("com.sun.star.awt.UnoControlEditModel")
        position_text.PositionX = 46
        position_text.PositionY = 68
        position_text.Width = 125
        position_text.Height = 17
        position_text.Name = "position_text"

        # button
        add_button = dialog_model.createInstance("com.sun.star.awt.UnoControlButtonModel")
        add_button.PositionX = 63
        add_button.PositionY = 110
        add_button.Width = 53
        add_button.Height = 17
        add_button.Label = "Add"
        add_button.Name = "add_button"

        # insert control models into the dialog model
        dialog_model.insertByName("id_num_label", id_num_label)
        dialog_model.insertByName("name_label", name_label)
        dialog_model.insertByName("position_label", position_label)
        dialog_model.insertByName("id_num_text", id_num_text)
        dialog_model.insertByName("name_text", name_text)
        dialog_model.insertByName("position_text", position_text)
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
