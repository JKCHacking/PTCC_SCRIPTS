# -*- coding: utf-8 -*-
import uno, unohelper
from com.sun.star.awt import XActionListener


class ButtonListener(unohelper.Base, XActionListener):
    def __init__(self, dialog):
        self.dialog = dialog

    def actionPerformed(self, actionEvent):
        pass


class AddEmployeeDlg(unohelper.Base):
    def __init__(self, context):
        self.ctx = context
        self.dialog = None
        self.id_num_text = None
        self.name_text = None
        self.position_text = None
        self.add_button = None

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
        self.id_num_text = dialog_model.createInstance("com.sun.star.awt.UnoControlEditModel")
        self.id_num_text.PositionX = 46
        self.id_num_text.PositionY = 15
        self.id_num_text.Width = 125
        self.id_num_text.Height = 17
        self.id_num_text.Name = "id_num_text"

        self.name_text = dialog_model.createInstance("com.sun.star.awt.UnoControlEditModel")
        self.name_text.PositionX = 46
        self.name_text.PositionY = 42
        self.name_text.Width = 125
        self.name_text.Height = 17
        self.name_text.Name = "name_text"

        self.position_text = dialog_model.createInstance("com.sun.star.awt.UnoControlEditModel")
        self.position_text.PositionX = 46
        self.position_text.PositionY = 68
        self.position_text.Width = 125
        self.position_text.Height = 17
        self.position_text.Name = "position_text"

        # button
        self.add_button = dialog_model.createInstance("com.sun.star.awt.UnoControlButtonModel")
        self.add_button.PositionX = 63
        self.add_button.PositionY = 110
        self.add_button.Width = 53
        self.add_button.Height = 17
        self.add_button.Label = "Add"
        self.add_button.Name = "add_button"

        # insert control models into the dialog model
        dialog_model.insertByName("id_num_label", id_num_label)
        dialog_model.insertByName("name_label", name_label)
        dialog_model.insertByName("position_label", position_label)
        dialog_model.insertByName("id_num_text", self.id_num_text)
        dialog_model.insertByName("name_text", self.name_text)
        dialog_model.insertByName("position_text", self.position_text)
        dialog_model.insertByName("add_button", self.add_button)

        self.dialog.setModel(dialog_model)
        # create a peer
        toolkit = smgr.createInstanceWithContext("com.sun.star.awt.ExtToolkit", self.ctx)
        self.dialog.createPeer(toolkit, None)
        return self.dialog

    def add_listeners(self):
        control = self.dialog.getControl('add_button')
        listener = ButtonListener(self.dialog)
        control.addActionListener(listener)

    def show(self):
        # create GUI
        self.dialog = self.create_dialog()
        self.add_listeners()
        self.dialog.execute()


def add_employee(*args):
    ctx = uno.getComponentContext()
    add_emp_dlg = AddEmployeeDlg(ctx)
    add_emp_dlg.show()


g_exportedScripts = (add_employee,)

if __name__ == "__main__":
    add_employee()
