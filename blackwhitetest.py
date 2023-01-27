from PIL import Image, ImageEnhance
import fitz
import os


def convert(file, savePath,name):
    unopend=[]
    pdf = fitz.open(file)
    doc = fitz.open()
    i=1
##    matrix = fitz.Matrix(300 / 72, 300 / 72)
    for frame in pdf.pages():
        pix = frame.get_pixmap(dpi = 300)
        pix.save(f'Page_{i}.jpg')
        unopend.append(f'Page_{i}.jpg')
        i+=1
    for uno in unopend:
        img= Image.open(uno)
        width,height = img.size
        ratio =width/700.0
        img = img.resize((int(width/ratio),int(height/ratio)),Image.ANTIALIAS)
        #img = img.convert('1')
        img = img.convert('L')
        img.save(uno, dpi = (300,300),  optimize=True, quality=50)
    for uno in unopend:
        img = fitz.open(uno)
        rect = img[0].rect
        pdfbytes = img.convert_to_pdf()  
        img.close()  
        imgPDF = fitz.open("pdf", pdfbytes)  
        page = doc.new_page(width = rect.width,  
                           height = rect.height)
        page.show_pdf_page(rect, imgPDF, 0)
    for pic in unopend:
        os.remove(pic)
    doc.save(f'{savePath}\\L_{name}.pdf', deflate = True)
    

if __name__ == '__main__':
    path = r'S:\scanns'
    file = "Besondere_Anlagebedingungen.pdf"
    convert(path + '\\' + file, path,file + 'Convert' )
##    orgPath = r'M:\Mandanten\SkyOne Property SCS\Unterlagen USt Lux 2021\Rechnungen Vorsteuer Vergütungsverfahren\Unterlagen für StB AVEGA'
##    saveOrd= r'C:\Users\davidleonschmidt\Desktop\Progs\pdf\Unterlagen für StB AVEGA'
##    
##    for root, dirs, files in os.walk(orgPath):
##        if dirs:
##            for file in files:
##                if os.path.splitext(file)[1] == '.pdf':
##                    name= os.path.splitext(file)[0]
##                    convert(f'{root}\\{file}',saveOrd,name)
##            continue
##        name = os.path.split(root)[1]
##        newOrd = f'{saveOrd}\\{name}'
##        if not os.path.isdir(newOrd):
##            os.mkdir(newOrd)
##        for file in files:
##            name= os.path.splitext(file)[0]
##            if os.path.splitext(file)[1] == '.pdf':
##                convert(f'{root}\\{file}',newOrd,name)
##
