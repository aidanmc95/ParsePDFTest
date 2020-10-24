import sys
import os

from pdfrw import PdfReader
import PyPDF2  
    
# creating a pdf file object  
pdfFileObj = open('test.pdf', 'rb')  
    
# creating a pdf reader object  
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  
    
# printing number of pages in pdf file  
print(pdfReader.numPages)  
    
# creating a page object  
pageObj = pdfReader.getPage(0)  
    
# extracting text from page  
print(pageObj.extractText())  
    
# closing the pdf file object  
pdfFileObj.close() 

if __name__ == "__main__":

    # # inpfn, = sys.argv[1:]
    # # outfn = 'alter.' + os.path.basename(inpfn)

    # doc = PdfReader('test.pdf')
    # for page in doc.pages:
    #     bytestream = page.Contents.stream
    #     print(utf8_decode())
    # # trailer.Info.Title = 'My New Title Goes Here'
    # # PdfWriter(outfn, trailer=trailer).write()
    print("hi")