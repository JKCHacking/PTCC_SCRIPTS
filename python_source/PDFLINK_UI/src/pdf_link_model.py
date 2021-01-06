import fitz

OK = 1
NOT_OK = -1


class PDFLinkModel:
    def __init__(self, pdf_file):
        self.doc = fitz.open(pdf_file)

    def add_link(self, keyword, pagenum_dest):
        res = NOT_OK
        found = False
        for pagenum, page in enumerate(self.doc.pages()):
            print("Working on page: {}".format(pagenum + 1))
            text_coord_list = page.searchFor(keyword)
            print("{} found on this page".format(len(text_coord_list)))
            if not found and len(text_coord_list) > 0:
                found = True
            for text_coord in text_coord_list:
                page.insertLink({"kind": fitz.LINK_GOTO, "page": pagenum_dest, "from": text_coord})
        if found:
            res = OK
        return res

    def save_document(self, filename):
        self.doc.save(filename)

    def get_total_num_page(self):
        count = 0
        for page in self.doc.pages():
            count += 1
        return count
