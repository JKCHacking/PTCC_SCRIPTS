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
    def __init__(self, pdf_path):
        self.fp = open(pdf_path, 'rb')
        self.page_pair_list = [
            {"link_name": "6.04", "page": 15},
            {"link_name": "5.01", "page": 5}
        ]
        self.box_length = 50
        self.box_width = 50

    def get_locations(self):
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pages = PDFPage.get_pages(self.fp)

        current_page_number = 0
        link_coor_list = []
        for page in pages:
            print(f"current page: {current_page_number}")
            interpreter.process_page(page)
            layout = device.get_result()

            for lobj in layout:
                if isinstance(lobj, LTTextBox):
                    text = lobj.get_text().replace("\n", "_")
                    for link in self.page_pair_list:
                        link_name = link["link_name"]
                        if link_name in text:
                            x, y = lobj.bbox[0], lobj.bbox[3]
                            link_dict = self.create_link_dict(link_name, x, y, current_page_number)
                            link_coor_list.append(link_dict)
                            print('At %r is text: %s' % ((x, y), text))
            current_page_number = current_page_number + 1
        return link_coor_list

    @staticmethod
    def create_link_dict(link_name, x, y, curr_page):
        link_dict = {
            "link": {
                "link_name": link_name,
                "x_coor": x,
                "y_coor": y,
                "curr_page": curr_page
            }
        }
        return link_dict

    def add_link(self):
        print("add_link start....")
        output_path = os.path.join(Constants.OUTPUT_DIR, 'output.pdf')
        in_reader = PdfFileReader(self.fp, strict=False)
        out_writer = PdfFileWriter()
        link_list = self.get_locations()

        page_num = in_reader.getNumPages()
        for i in range(page_num):
            page = in_reader.getPage(i)
            out_writer.addPage(page)

        for link in link_list:
            for page_pair in self.page_pair_list:
                if page_pair['link_name'] == link['link']['link_name']:
                    x = link['link']['x_coor']
                    y = link['link']['y_coor']
                    rect = self.create_rect(x, y)
                    out_writer.addLink(link['link']['curr_page'], page_pair['page'], rect=rect,
                                       border="dott")

        with open(output_path, 'wb') as out_file:
            out_writer.write(out_file)

    def create_rect(self, x, y):
        # upper_left = (x - self.box_length/2, y + self.box_width/2)
        # lower_right = (x + self.box_length / 2, y - self.box_width / 2)

        lower_left = (x - self.box_length/2, y - self.box_width/2)
        upper_right = (x + self.box_length/2, y + self.box_width/2)
        # rect = RectangleObject([upper_left[0], upper_left[1], lower_right[0], lower_right[1]])
        rect = [lower_left[0], lower_left[1], upper_right[0], upper_right[1]]
        return rect


if __name__ == "__main__":
    pdf_path = os.path.join(Constants.INPUT_DIR, 'input.pdf')
    dpp = DrawingPDFParser(pdf_path)
    dpp.add_link()
