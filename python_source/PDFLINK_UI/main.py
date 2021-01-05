import sys
from PyQt5.QtWidgets import QApplication
from src.pdf_link_ui import PDFLinkUI
from src.pdf_link_ctrl import PDFLinkCtrl


def main():
    pdf_linker = QApplication(sys.argv)
    view = PDFLinkUI()
    model = None
    view.show()
    PDFLinkCtrl(model, view)
    sys.exit(pdf_linker.exec_())


if __name__ == "__main__":
    main()
