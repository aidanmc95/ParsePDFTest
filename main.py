import sys
import os
import shutil

import PyPDF2  

# creating a pdf file object 
path = './Results'
dirs = os.listdir( path )

for file in dirs:
    file_path = 'Results/' + file
    if not os.path.isdir(file_path):
        pdfFileObj = open(file_path, 'rb')
    
        # creating a pdf reader object  
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  
    
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

        # pass return obj here
        

        # check for folder to move pdf into
        folder = 'Results/' + returnObj['Date'].split()[0].replace('/','-')
        if not os.path.exists(folder):
            os.makedirs(folder)
        shutil.move(file_path, folder + '/' + file)

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