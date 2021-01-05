import sys
from PyQt5.QtWidgets import QApplication
from src.pdf_link_model import PDFLinkModel
from src.pdf_link_ui import PDFLinkUI
from src.pdf_link_ctrl import PDFLinkCtrl


class App(QApplication):
    def __init__(self, argv):
        super(App, self).__init__(argv)
        self.model = PDFLinkModel
        self.view = PDFLinkUI()
        self.controller = PDFLinkCtrl(self.model, self.view)
        self.view.show()


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec_())
