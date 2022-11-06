from bs4 import BeautifulSoup
import threading , time,random,os,requests,bs4,shutil,json,urllib3 
i=requests.get('https://data.cip.gov.tw/API/v1/dump/datastore/A53000000A-110078-001')
print(i.text)