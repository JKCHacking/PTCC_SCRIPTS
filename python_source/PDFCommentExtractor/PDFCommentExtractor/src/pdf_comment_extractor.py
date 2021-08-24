import os
import fitz
import openpyxl
import pdfplumber
from constants import Constants

SEARCH_MODE = "blocks"


def iter_input():
    for dir_path, dir_names, file_names in os.walk(Constants.INPUT_DIR):
        for file_name in file_names:
            if file_name.endswith(".pdf"):
                yield os.path.join(dir_path, file_name)


def main():
    for pdf_fp in iter_input():
        print("PDF File: {}".format(os.path.basename(pdf_fp)))
        comment_list = []
        doc = fitz.open(pdf_fp)
        for page_num, page in enumerate(doc.pages(), 1):
            # find for annotations
            for annot in page.annots():
                annot_text = annot.get_text()
                if annot_text:
                    comment = Comment(text=annot_text,
                                      author=annot.info["title"],
                                      color="",
                                      page_number=page_num)
                    comment_list.append(comment)
            # find for blocks with red color font
            blocks = page.get_text("dict", flags=11)["blocks"]
            for b in blocks:
                comment_text = ""
                color = ""
                for l in b["lines"]:
                    for s in l["spans"]:
                        if "#{:06x}".format(s["color"]) == "#ff0000":
                            comment_text += " {}".format(s["text"])
                            color = "red"
                if comment_text:
                    comment = Comment(text=comment_text, color=color, page_number=page_num, author="")
                    comment_list.append(comment)

        file_name = os.path.splitext(os.path.basename(pdf_fp))[0]
        workbook = openpyxl.Workbook()
        summary_ws = workbook.create_sheet("comment_summary")
        summary_ws.append(["Comment", "Author", "Color", "Page Number"])
        for row, comment in enumerate(comment_list, 2):
            summary_ws["A{}".format(row)] = comment.get_text()
            summary_ws["B{}".format(row)] = comment.get_author()
            summary_ws["C{}".format(row)] = comment.get_color()
            summary_ws["D{}".format(row)] = comment.get_page_number()
        workbook.remove(workbook["Sheet"])
        workbook.save(os.path.join(Constants.OUTPUT_DIR, file_name + ".xlsx"))


class Comment:
    def __init__(self, text=None, color=None, author=None, page_number=None):
        self.text = text
        self.color = color
        self.author = author
        self.page_number = page_number

    def get_text(self):
        return self.text

    def get_color(self):
        return self.color

    def get_author(self):
        return self.author

    def get_page_number(self):
        return self.page_number

    def set_text(self, text):
        self.text = text

    def set_color(self, color):
        self.color = color

    def set_author(self, author):
        self.author = author

    def set_page_number(self, page_number):
        self.page_number = page_number


if __name__ == "__main__":
    main()
