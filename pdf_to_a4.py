import PyPDF2


def pdf_to_a4(file):
    pdf = PyPDF2.PdfFileReader(file)
    writer = PyPDF2.PdfFileWriter()  # create a writer to save the updated results

    for p in pdf.pages:
        x_size = float(p.mediabox[2]) # this is in user space units. there are 72 user space units per inch. 
        # A4 is 8.25 inch, we want to scale up to 72*8.25 user space units.
        scale_factor = 72*8.25/x_size
        p.scale_by(scale_factor)
        writer.add_page(p)    

    with open("Latex integration 2.pdf", "wb+") as f:
        writer.write(f)

file = "Latex integration.pdf"
pdf_to_a4(file)