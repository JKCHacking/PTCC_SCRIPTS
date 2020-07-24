import fitz


class PdfScript:
    def __init__(self, filepath):
        self.doc = fitz.open(filepath)

    def search_title(self, page, title_pattern):
        title = None
        for textpage in page.getText("blocks"):
            text = textpage[4]
            if text.startswith(title_pattern):
                title = text
        return title

    def get_page_from_file(self):
        # for page in self.doc.pages:
        #     yield page
        page = self.doc[16]
        yield page

    def search_strings_from_page(self, page, text_list):
        for textpage in page.getText("blocks"):
            text = textpage[4]
            print(text)
            if any(pattern in text for pattern in text_list):
                print(True)
                yield text

    def search_annotations_from_page(self, page):
        for annot in page.annots():
            content = annot.info["content"]
            yield content
