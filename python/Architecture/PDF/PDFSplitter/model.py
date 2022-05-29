import os
import copy
from PyPDF2 import PdfFileWriter, PdfFileReader


class Model:
    def split(self, src, dst, pad_left, pad_right, pad_top, pad_bot):
        with open(src, 'r+b') as src_f, open(dst, 'w+b') as dst_f:
            reader = PdfFileReader(src_f)
            writer = PdfFileWriter()
            for i in range(reader.getNumPages()):
                curr_page = reader.getPage(i)
                page1 = copy.copy(curr_page)
                page2 = copy.copy(curr_page)

                ll_x, ll_y = curr_page.mediaBox.lowerLeft
                ur_x, ur_y = curr_page.mediaBox.upperRight

                if ur_x > ur_y:  # landscape
                    page1.mediaBox.lowerLeft = (ll_x + pad_left, ll_y + pad_bot)
                    page1.mediaBox.upperRight = (((ur_x + ll_x) / 2) - pad_right, ur_y - pad_top)
                    page2.mediaBox.lowerLeft = (((ll_x + ur_x) / 2) + pad_left, ll_y + pad_bot)
                    page2.mediaBox.upperRight = (ur_x - pad_right, ur_y - pad_top)
                else:  # portrait
                    page1.mediaBox.lowerLeft = (ll_x + pad_left, ((ll_y + ur_y) / 2) + pad_bot)
                    page1.mediaBox.upperRight = (ur_x - pad_right, ur_y - pad_top)
                    page2.mediaBox.lowerLeft = (ll_x + pad_left, ll_y + pad_bot)
                    page2.mediaBox.upperRight = (ur_x - pad_right, ((ll_y + ur_y) / 2) - pad_top)

                writer.addPage(page1)
                writer.addPage(page2)
            writer.write(dst_f)
