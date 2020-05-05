#!/usr/bin/env python

from PyPDF2 import PdfFileWriter, PdfFileReader
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from constants import Constants
import os


class DrawingPDFParser:
    def __init__(self):
        self.box_length = 50
        self.box_width = 50

    def get_locations(self, fp, page_names):
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pages = PDFPage.get_pages(fp)

        current_page_number = 0
        link_coor_list = []
        for page in pages:
            print(f"current page: {current_page_number}")
            interpreter.process_page(page)
            layout = device.get_result()

            for lobj in layout:
                if isinstance(lobj, LTTextBox):
                    text = lobj.get_text().replace("\n", "_")
                    for page_name in page_names:
                        if page_name in text:
                            x0, y0_orig, x1, y1_orig = lobj.bbox
                            x0 = page.mediabox[3] - x0
                            x1 = page.mediabox[3] - x1
                            rect_coord = [y0_orig, x0, y1_orig, x1]
                            link_dict = self.create_link_dict(page_name, rect_coord, current_page_number)
                            link_coor_list.append(link_dict)
                            print('At %r is text: %s' % (rect_coord, text))
            current_page_number = current_page_number + 1
        return link_coor_list

    @staticmethod
    def create_link_dict(link_name, rect_coord, curr_page):
        link_dict = {
            "link_name": link_name,
            "rect_coord": rect_coord,
            "curr_page": curr_page
        }
        return link_dict

    def add_link(self, out_writer, link_list, dest_page, page_name):
        print("add_link start....")
        for link in link_list:
            if page_name == link['link_name']:
                rect = link['rect_coord']
                out_writer.addLink(link['curr_page'], dest_page, rect=rect,
                                   border=[16, 16, 1])
        return out_writer

    def add_bookmark(self, out_writer, page_number, parent, page_name):
        out_writer.addBookmark(page_name, page_number, parent)
        return out_writer


if __name__ == "__main__":
    pdf_path = os.path.join(Constants.INPUT_DIR, 'input.pdf')
    output_path = os.path.join(Constants.OUTPUT_DIR, 'output.pdf')
    fp = open(pdf_path, 'rb')
    page_names = ["0.00", "0.01", "0.02", "0.03", "3.01",
                  "5.01", "5.02", "5.03", "5.04", "5.05",
                  "5.06", "5.07", "6.01", "6.02", "6.03",
                  "6.04", "6.05", "6.06", "6.07", "6.08",
                  "6.09", "6.10"]

    in_reader = PdfFileReader(fp, strict=False)
    out_writer = PdfFileWriter()
    page_num = in_reader.getNumPages()

    dpp = DrawingPDFParser()
    link_list = dpp.get_locations(fp, page_names)

    for i in range(page_num):
        page = in_reader.getPage(i)
        out_writer.addPage(page)

    parent = out_writer.addBookmark("Sheets and Views", 0)
    for i, page_name in zip(range(page_num), page_names):
        out_writer = dpp.add_link(out_writer, link_list, i, page_name)
        out_writer = dpp.add_bookmark(out_writer, i, parent, page_name)

    with open(output_path, 'wb') as out_file:
        out_writer.write(out_file)
