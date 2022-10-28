from pdf2image import convert_from_path

def pdf2images(file,dpi=300):

      images = convert_from_path(file,dpi=dpi)

      for i in range(len(images)):
         
            # Save pages as images in the pdf
            images[i].save('page'+ str(i) +'.jpg', 'JPEG')
