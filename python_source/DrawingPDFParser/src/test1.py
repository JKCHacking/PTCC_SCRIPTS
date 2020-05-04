from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from constants import Constants
import os


existing_pdf = PdfFileReader(open(os.path.join(Constants.INPUT_DIR, 'test2.pdf'), "rb"), strict=False)
output = PdfFileWriter()

pageNum = existing_pdf.getNumPages()


for i in range(pageNum):
    if i == 0:
        packet = io.BytesIO()

        can = canvas.Canvas(packet, pagesize=letter)
        can.drawString(523, 45, "")
        can.save()

        packet.seek(0)
        new_pdf = PdfFileReader(packet)

        page = existing_pdf.getPage(i)
        new_pdf = PdfFileReader(packet)
        page2 = new_pdf.getPage(0)
        page.mergePage(page2)
        output.addPage(page)
    else:
        packet = io.BytesIO()

        can = canvas.Canvas(packet, pagesize=letter)
        can.drawString(523, 45, "{}".format(i+1))
        can.save()

        packet.seek(0)
        new_pdf = PdfFileReader(packet)

        page = existing_pdf.getPage(i)
        new_pdf = PdfFileReader(packet)
        page2 = new_pdf.getPage(0)
        page.mergePage(page2)
        output.addPage(page)
        output.addLink(i, 0, [500, 30, 550, 60], [10, 10, 10], "/XYZ", 0, 0, 1)


outputStream = open(os.path.join(Constants.OUTPUT_DIR, 'output_5.pdf'), "wb")
output.write(outputStream)
outputStream.close()