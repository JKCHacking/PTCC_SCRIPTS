import os
import fitz


def main():
    pdf_fp = "H:/Desktop/projects/pdf_project/2021 12 01 [WA 1000] SHOP DRAWING - TOWER REVISION.pdf"
    doc = fitz.open(pdf_fp)
    bookmarks = doc.getToC(simple=True)
    not_found = []
    for i, page in enumerate(doc.pages()):
        print("Page: {}/{}".format(i + 1, doc.pageCount), )
        for bookmark in bookmarks:
            keyword = bookmark[1]
            keyword = "{}.{}".format(keyword[0], keyword[1:])
            page_num = int(bookmark[2] - 1)
            text_coord_list = page.searchFor(keyword)
            if text_coord_list:
                if keyword in not_found:
                    not_found.remove(keyword)
                for text_coord in text_coord_list:
                    page.insertLink({"kind": fitz.LINK_GOTO, "page": page_num, "from": text_coord})
            else:
                not_found.append(keyword)
    pdf_fp_modified = os.path.splitext(pdf_fp)[0] + "_modified.pdf"
    doc.save(pdf_fp_modified)
    print("Saved to {}".format(pdf_fp_modified))
    return set(not_found)


if __name__ == "__main__":
    not_found = main()
    # print("Keywords not found:\n{}".format("\n".join(not_found)))
