from io import BytesIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


from datetime import date

import requests
import json
today = date.today()

year = today.strftime("%Y")
month = today.strftime("%m")
day = today.strftime("%d")
strToday = year + "-"+month+"-"+day
testURL = "http://www.fcmcclerk.com/storage/shared/daily-arraignment/FCMC Arraignment Report 4D " + strToday +" Defendant Sheets.pdf"

path = "/home/eric/Desktop/PythonDev/PythonWebScrape/FCMC Arraignment Report 4D " + strToday + " Defendant Sheets.pdf"

output_string = BytesIO()

page = requests.get(testURL)

defendant = {
  "name":"",
  "address":"",
  "DOB":"",
  "charges":"",
  "courtroom":"",
  "jurisdiction":"",
  "event":"",
  "attorney":""
}


def extract_text_by_page(pdf_path):
  with open(pdf_path, 'rb') as fh:
    for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
      resource_manager= PDFResourceManager()
      fake_file_handle = output_string
      converter = TextConverter(resource_manager, fake_file_handle)
      page_interpreter = PDFPageInterpreter(resource_manager, converter)
      page_interpreter.process_page(page)
      
      text = fake_file_handle.getvalue()
      yield text
      
    converter.close()
    fake_file_handle.close()
    
    
def extract_text(pdf_path):
  for page in extract_text_by_page(pdf_path):
    print(page)
    print()
    
    
    


def toJSON(pdfPath):
  counter = 1
  for page in extract_text_by_page(pdfPath):
    text = page
    nameStart = text.index("STATE OF OHIO vs")
    print(nameStart)
    nameStart = nameStart + 16
    nameEnd = text.index("COURTROOM")
    print(nameEnd)
    name =  text[nameStart:nameEnd]
    print(name)
    addressStart = text.find("4D")
    addressStart = addressStart + 2
    addressEnd = text.find("JURISDICTION:")
    address = text[addressStart:addressEnd]
    print(address)
    
    
    jurisdictionEnd = text.find(" ",addressEnd)
    
    jurisdiction = text[addressEnd+13:jurisdictionEnd]
    print(jurisdiction)
    
if __name__ == '__main__':
  print(extract_text(path))
  
  
