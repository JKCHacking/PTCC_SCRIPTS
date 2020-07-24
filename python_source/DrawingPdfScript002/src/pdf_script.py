import fitz

SEARCH_MODE = "blocks"


class PdfScript:
    def __init__(self, filepath):
        self.doc = fitz.open(filepath)

    def search_title(self, page, title_pattern):
        title = None
        for textpage in page.getText(SEARCH_MODE):
            text = textpage[4]
            if text.startswith(title_pattern):
                title = text
        return title

    def get_page_from_file(self):
        for page in self.doc.pages:
            yield page

    def search_strings_from_page(self, page, pattern_list):
        for textpage in page.getText(SEARCH_MODE):
            text = textpage[4]
            for pattern in pattern_list:
                if pattern in text:
                    yield text, pattern

    def search_annotations_from_page(self, page):
        for annot in page.annots():
            content = annot.info["content"]
            yield content
