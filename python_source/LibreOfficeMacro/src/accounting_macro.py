import datetime
import uno
import msgbox
from locale import atof, setlocale, LC_NUMERIC

TRIES = 10
setlocale(LC_NUMERIC, '')


def open_file_chooser():
    path = None
    ctx = uno.getComponentContext()
    smgr = ctx.getServiceManager()
    file_picker = smgr.createInstanceWithContext("com.sun.star.ui.dialogs.FilePicker", ctx)
    filters = "*.ods;"
    file_picker.appendFilter("Supported files", filters)
    res = file_picker.execute()
    if res == 1:
        path = file_picker.getFiles()[0]
    file_picker.dispose()
    return path


def get_transactions():
    trans_list = []
    url = open_file_chooser()
    if url:
        # find the chosen file in the list of open files.
        active_docs = get_ods_docs()
        liquid_doc = None
        for active_doc in active_docs:
            if url == active_doc.Location:
                liquid_doc = active_doc
                break

        if liquid_doc:
            input_sheet = liquid_doc.Sheets["Input Data"]
            # get all the data from constant columns
            curr_row = 5
            ewt = input_sheet.getCellByPosition(13, curr_row).getString().strip()
            if ewt != "#REF!":
                while input_sheet.getCellByPosition(1, curr_row).getString():
                    date = input_sheet.getCellByPosition(1, curr_row).getString().strip()
                    cv_no = input_sheet.getCellByPosition(2, curr_row).getString().strip()
                    si_date = input_sheet.getCellByPosition(4, curr_row).getString().strip()
                    si_no = input_sheet.getCellByPosition(5, curr_row).getString().strip()
                    supplier = input_sheet.getCellByPosition(6, curr_row).getString().strip()
                    particulars = input_sheet.getCellByPosition(7, curr_row).getString().strip()
                    is_qualified = input_sheet.getCellByPosition(8, curr_row).getString().strip()
                    atc_code = input_sheet.getCellByPosition(9, curr_row).getString().strip()
                    categories = input_sheet.getCellByPosition(11, curr_row).getString().strip()
                    cash_in_bank = input_sheet.getCellByPosition(12, curr_row).getString().strip()
                    ewt = input_sheet.getCellByPosition(13, curr_row).getString().strip()
                    in_tax = input_sheet.getCellByPosition(14, curr_row).getString().strip()

                    # get the data from the account titles
                    acc_col = 15
                    acc_dict = {}
                    while input_sheet.getCellByPosition(acc_col, 4).getString():
                        acc_name = input_sheet.getCellByPosition(acc_col, 4).getString().strip()
                        acc_val = input_sheet.getCellByPosition(acc_col, curr_row).getString().strip()
                        if acc_val:
                            acc_dict.update({acc_name: acc_val})
                        acc_col += 1
                    trans = Transaction(
                        date,
                        cv_no,
                        si_date,
                        si_no,
                        supplier,
                        particulars,
                        is_qualified,
                        atc_code,
                        categories,
                        cash_in_bank,
                        ewt,
                        in_tax,
                        acc_dict
                    )
                    trans_list.append(trans)
                    curr_row += 1
            else:
                MsgBox("There are unreferenced links.")
        else:
            MsgBox("Your file is not open.")
    return trans_list


def load_transactions(*args):
    tax_doc = XSCRIPTCONTEXT.getDocument()
    input_sheet = tax_doc.Sheets["Input Data"]
    trans_list = get_transactions()
    if trans_list:
        row_offset = 5
        for i, trans in enumerate(trans_list):
            row = row_offset + i
            # check row first
            check = input_sheet.getCellByPosition(0, row).getString().strip()
            if check:
                row += 1
            input_sheet.getCellByPosition(0, row).setString(trans.date.strftime("%Y-%b-%d"))
            input_sheet.getCellByPosition(1, row).setString(trans.cv_no)
            input_sheet.getCellByPosition(3, row).setString(trans.supplier)
            input_sheet.getCellByPosition(7, row).setString(trans.atc_code)
            input_sheet.getCellByPosition(8, row).setString(trans.categories)
            input_sheet.getCellByPosition(13, row).setString(trans.si_no)
            net_purchases = 0
            account_titles = []
            for account_title, value in trans.accounts.items():
                if "Non taxable" not in account_title:
                    net_purchases += value
                    account_titles.append(account_title)
            gross_purchases = net_purchases + trans.in_tax
            input_sheet.getCellByPosition(6, row).setString(", ".join(account_titles))
            if trans.is_qualified:
                input_sheet.getCellByPosition(9, row).setValue(gross_purchases)
                input_sheet.getCellByPosition(10, row).setValue(net_purchases)
                input_sheet.getCellByPosition(12, row).setValue(trans.in_tax)
                if trans.ewt:
                    input_sheet.getCellByPosition(0, row + 1).setString(trans.date.strftime("%Y-%b-%d"))
                    input_sheet.getCellByPosition(1, row + 1).setString(trans.cv_no)
                    input_sheet.getCellByPosition(3, row + 1).setString(trans.supplier)
                    input_sheet.getCellByPosition(6, row + 1).setString(", ".join(account_titles))
                    input_sheet.getCellByPosition(7, row + 1).setString(trans.atc_code)
                    input_sheet.getCellByPosition(8, row + 1).setString(trans.categories)
                    input_sheet.getCellByPosition(13, row + 1).setString(trans.si_no)
                    input_sheet.getCellByPosition(11, row + 1).setValue(trans.ewt)
            else:
                input_sheet.getCellByPosition(11, row).setValue(net_purchases)


def MsgBox(txt):
    mb = msgbox.MsgBox(uno.getComponentContext())
    mb.addButton("OK")
    mb.show(txt, 0, "Python")


def get_ods_docs():
    ods_doc_list = []
    components = XSCRIPTCONTEXT.getDesktop().getComponents()
    docs = components.createEnumeration()
    while docs.hasMoreElements():
        doc = docs.nextElement()
        if doc.supportsService("com.sun.star.sheet.SpreadsheetDocument"):
            ods_doc_list.append(doc)
    return ods_doc_list


class Transaction:
    __slots__ = ("date", "cv_no", "si_date", "si_no", "supplier",
                 "particulars", "is_qualified", "atc_code", "categories",
                 "cash_in_bank", "ewt", "in_tax", "accounts")

    def __init__(self, date, cv_no, si_date, si_no, supplier,
                 particulars, is_qualified, atc_code, categories, cash_in_bank,
                 ewt, in_tax, accounts):
        self.date = datetime.datetime.strptime(date, "%Y-%b-%d").date()
        self.cv_no = cv_no
        self.si_date = datetime.datetime.strptime(si_date, "%Y-%b-%d").date()
        self.si_no = si_no
        self.supplier = supplier
        self.particulars = particulars
        self.is_qualified = True if is_qualified == "Yes" else False
        self.atc_code = atc_code
        self.categories = categories
        self.cash_in_bank = atof(cash_in_bank) if cash_in_bank else 0
        self.ewt = atof(ewt) if ewt else 0
        self.in_tax = atof(in_tax) if in_tax else 0

        # convert all account values to float from string
        for k, v in accounts.items():
            accounts[k] = atof(v)
        self.accounts = accounts


g_exportedScripts = (load_transactions,)
