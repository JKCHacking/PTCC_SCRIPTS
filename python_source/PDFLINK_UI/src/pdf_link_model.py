import fitz


class PDFLinkModel:
    def __init__(self, pdf_file, keyword, pagenum_dest):
        self.doc = fitz.open(pdf_file)
        self.keyword = keyword
        self.pagenum_dest = pagenum_dest

    def add_link(self):
        for pagenum, page in enumerate(self.doc.pages()):
            print("Working on page: {}".format(pagenum + 1))
            text_coord_list = page.searchFor(self.keyword)
            print("{} found on this page".format(len(text_coord_list)))
            for text_coord in text_coord_list:
                page.insertLink({"kind": fitz.LINK_GOTO, "page": self.pagenum_dest, "from": text_coord, "border": 1})

    def save_document(self, filename):
        self.doc.save(filename)
