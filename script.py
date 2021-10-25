from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date
from bs4 import BeautifulSoup

from pdfminer.high_level import extract_text

import requests
import io
import json
import os



#driver = webdriver.Firefox()
today = date.today()
print(today)
year = today.strftime("%Y")
month = today.strftime("%m")
day = today.strftime("%d")

strToday = year + "-"+month+"-"+day
print(strToday)

URL = "http://www.fcmcclerk.com/reports/daily-arraignment"
# driver.get(URL)

testURL = "http://www.fcmcclerk.com/storage/shared/daily-arraignment/FCMC Arraignment Report 4D " + strToday +" Defendant Sheets.pdf"
# driver.get(testURL)

page = requests.get(URL)
pagePDF = requests.get(testURL)
text = extract_text(io.BytesIO(pagePDF.content))

# print(text)
print(len(text))
count = 0
temp = 0
newDef = 0
nameflag = False
addressflag = False
addressflag2 = False
chargesflag = False
for a in text:
  count = count+1
  if (a == '\n'):
        
    maybe = text[temp:count]
    print(maybe)
    if chargesflag:
      print("charges flag true")
      defendant.charges = maybe
      chargesflag = False
    
    if maybe == "CHARGES":
      chargesflag = True
    else:
      chargesflag = False
    if nameflag:
      defendant.name = maybe
      print("nameflag true")
      nameflag = False
      addressflag = True
    if addressflag:
      print("address flag true")
      defendant.address = maybe
      addressflag = False
    if addressflag2 == True:
      print("address flag 2 true")
      defendant.address = defendant.address + maybe
      addressflag2 == False
    if len(maybe) == 0:
      newDef = newDef + 1
    else:
      newDef = 0
      
    if newDef == 3:
      newDef = 0
      nameflag = True
   
      
    temp = count
    

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

defendants = {"defendant":defendant}    



  
  
def export_as_json(pdf_path, json_path):
  page = requests.get(pdf_path)
  
