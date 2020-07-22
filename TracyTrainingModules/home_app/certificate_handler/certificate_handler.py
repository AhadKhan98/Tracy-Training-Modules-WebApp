from PyPDF2 import PdfFileWriter, PdfFileReader
import io, os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def generate_certificate(fullname, access_code):
    
    # file_dir = os.path.join(BASE_DIR, 'h')
    file_dir = os.path.join(os.getcwd(), 'home_app/certificate_handler')
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont('Times-Roman',45)
    offset = 10 * len(fullname)
    can.drawString(390-offset, 340, fullname)
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("{}/original.pdf".format(file_dir), "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open("{}/{}.pdf".format(file_dir, access_code), "wb")
    output.write(outputStream)
    outputStream.close()

