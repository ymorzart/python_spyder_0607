# -*- coding: utf-8 -*-

"""
Created on Mon Jun 29 12:14:00 2020

@author: vincent.yu
"""

#import os
import PyPDF2
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os
os.environ["HTTP_PROXY"] = "http://70.10.15.10:8080"
os.environ["HTTPS_PROXY"] = "http://70.10.15.10:8080"
os.environ["PYTHONHTTPSVERIFY"] = "0"

def pdf_to_txt(filepath):
    fp = open(filepath, 'rb')
    #동일한 문제 나스카 문제 예상....
    total_pages = PyPDF2.PdfFileReader(fp).numPages
    print(total_pages)

    page_text = {}
    for page_no in range(total_pages):
        
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr,retstr, codec=codec, laparams=laparams)
        fp = open(filepath,'rb')
        password = None
        maxpages = 0
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        caching = True
        pagenos = [page_no]
       
        for page in PDFPage.get_pages(fp,pagenos, maxpages=maxpages, password=password,
                                  caching = caching, check_extractable=True):
            interpreter.process_page(page)
        
        page_text[page_no] = retstr.getvalue()
    
        fp.close()
        device.close()
        retstr.close()
    
    return page_text

if __name__ == "__main__":
    
#현 작업 디렉토리
    print("현재 폴더: ", os.getcwd())
# 디렉토리 변경 
    os.chdir("K:/My files/Download/wordCloud/pdftotxt")
    print("변경 폴더: ", os.getcwd())
    
    filename = "a.pdf"
    filepath = os.path.join(os.getcwd(), filename)
    pdf_text = pdf_to_txt(filepath)    
    
    text_file = os.path.join(os.getcwd(), "output", filename.split('.')[0]+".txt")
    f = open(text_file,'w',-1,"utf-8")   
    
    for k, v in pdf_text.items():
        first_row = "_________________%s 페이지의 내용입니다._________\n" % k
        f.write(first_row + v)
    f.close()
