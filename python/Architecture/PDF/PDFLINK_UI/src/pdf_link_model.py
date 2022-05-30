import fitz


class PDFLinkModel:
    def __init__(self, pdf_file):
        self.doc = fitz.open(pdf_file)

    def add_link(self, keywords, pagenum_dests):
        not_found = set()
        for pagenum, page in enumerate(self.doc.pages()):
            print("Working on page: {}".format(pagenum + 1))
            for keyword, pagenum_dest in zip(keywords, pagenum_dests):
                text_coord_list = page.searchFor(keyword)
                if text_coord_list:
                    if keyword in not_found:
                        not_found.remove(keyword)
                    for text_coord in text_coord_list:
                        page.insertLink({"kind": fitz.LINK_GOTO, "page": pagenum_dest, "from": text_coord})
                else:
                    not_found.add(keyword)
        return not_found

    def save_document(self, filename):
        self.doc.save(filename)

    def get_total_num_page(self):
        return self.doc.pageCount
