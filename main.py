import sys
import os

import PyPDF2  

# creating a pdf file object 
# pdfFileObj = open('Data/1603498716_M201023001.pdf', 'rb')
pdfFileObj = open('Data/1603498716_M201023002.pdf', 'rb')
# pdfFileObj = open('Data/1603498715_M201023003.pdf', 'rb')  
# pdfFileObj = open('Data/1603498715_M201023004.pdf', 'rb')  
# pdfFileObj = open('test.pdf', 'rb')  
    
# creating a pdf reader object  
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  
    
# printing number of pages in pdf file  
print(pdfReader.numPages)  
    
# creating a page object  
pageObj = pdfReader.getPage(0)  
    
# extracting text from page  
textObj = pageObj.extractText().splitlines()

# get important info
spot = 0
while(textObj[spot] != 'F%Mobile Xpress Clinics' and spot < len(textObj)):
    spot += 1

returnObj = {}
if(spot + 14 == len(textObj) - 1):
    returnObj['Name'] = textObj[spot + 4]
    returnObj['Birthday'] = textObj[spot + 5]
    returnObj['Gender'] = textObj[spot + 6]
    returnObj['SampleID'] = textObj[spot + 8]
    returnObj['Date'] = textObj[spot + 9]
    returnObj['Result'] = textObj[spot + 14]
print(returnObj)
    
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