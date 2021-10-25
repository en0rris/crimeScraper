from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date
from bs4 import BeautifulSoup

from pdfminer.high_level import extract_text

import requests
import io
import json
import os



defendants = [] 
print(defendants)
  

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
# driver.get(testURL)python

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
defendantcount = 0
tempCharges =""
tempName=""
tempAddress = ""
for a in text:
  count = count+1
  if (a == '\n'):
        
    maybe1 = text[temp:count]
    maybe = maybe1.strip()
    #print(maybe)
    if chargesflag:
      #print("charges flag true")
      tempCharges = maybe
      chargesflag = False
    
    if maybe == "CHARGES":
      chargesflag = True
    else:
      chargesflag = False
      
    if nameflag and addressflag == False and addressflag2 == False:
      tempName= maybe
      #print("nameflag true")
      
      addressflag = True
    if nameflag and addressflag and addressflag2 == False:
      #print("address flag true")
      tempAddress = maybe
      addressflag = False
      addressflag2 = True
    if nameflag and addressflag and addressflag2:
      print("address flag 2 true")
      tempAddress = tempAddress +  " "+maybe
      addressflag2 == False
      addressflag = False
      print(tempAddress)
    if len(maybe) == 0:
      newDef = newDef + 1
    else:
      newDef = 0
      
    if newDef == 3:
      defendant = dict(
        name='',
        address='',
        DOB='',
        charges='',
        courtroom='',
        jurisdiction='',
        event='',
        attorney=''
      )
      newDef = 0
      nameflag = True
      chargesflag = False
      addressflag = False
      addressflag2 = False
      defendant["name"] = tempName
      defendant["address"] = tempAddress
      defendant["charges"] = tempCharges
      print(defendant)
      defendants.insert(defendantcount, defendant)
      defendantcount = defendantcount + 1
      
    temp = count
    




print(defendants)
  
def export_as_json(pdf_path, json_path):
  page = requests.get(pdf_path)
  
