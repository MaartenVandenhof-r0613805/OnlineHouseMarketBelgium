
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import time




def setDriver(Driver):
    path = 'C:\Program Files\SeleniumDrivers'
    path = path+str(Driver)+'.exe'
    ser = Service(path)
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ser, options=op)
    return driver



driver = setDriver('\chromedriver')
driver.get('https://validate.perfdrive.com/21240cc12f281084e3ed3f9d063dd905/?ssa=074ec8bf-d887-495a-9ee6-e64354f04c2a&ssb=88182297010&ssc=https%3A%2F%2Fwww.zimmo.be%2Fnl%2Fpanden%2F%3Fstatus%3D2%26type%255B0%255D%3D5%26type%255B1%255D%3D1%26type%255B2%255D%3D6%26hash%3D14de828c2a744b723baa0ebfe4d02351%26priceIncludeUnknown%3D1%26priceChangedOnly%3D0%26bedroomsIncludeUnknown%3D1%26bathroomsIncludeUnknown%3D1%26constructionIncludeUnknown%3D1%26livingAreaIncludeUnknown%3D1%26landAreaIncludeUnknown%3D1%26commercialAreaIncludeUnknown%3D1%26yearOfConstructionIncludeUnknown%3D1%26epcIncludeUnknown%3D1%26queryCondition%3Dand%26includeNoPhotos%3D1%26includeNoAddress%3D1%26onlyRecent%3D0%26onlyRecentlyUpdated%3D0%26isPlus%3D0%26region%3Dlist%26city%3DMzAYicAQAA%25253D%25253D%26pagina%3D1&ssi=c4a00c7e-a26d-4e19-a0b9-ae0d2470e687&ssk=helpdesk@zimmo.be&ssm=69533876450803144103724397661027&ssn=ded76ecbd1cc452234596d3d7957955f58b4bbca8d75-f624-4a39-b09636&sso=3a2f0bce-2cca2842cb8bed862b6327f333d1b4bc3c0157b40a0649e1&ssp=30493980511645871723164587611186953&ssq=02104392258837834702422588370638125960011&ssr=OTQuMjI1LjEyLjc3&sst=Mozilla/5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/98.0.4758.102%20Safari/537.36&ssv=&ssw=&ssx=W10=#gallery')
https://validate.perfdrive.com/21240cc12f281084e3ed3f9d063dd905/?ssa=f8704fbb-1153-42fe-81dc-e8a225780560&ssb=30609298996&ssc=https%3A%2F%2Fwww.zimmo.be%2F&ssi=65b94f59-a26d-4abf-b7d7-94aa0aea0d19&ssk=helpdesk@zimmo.be&ssm=96767432028828453101979840760275&ssn=e7db960d2c7cd14e726bcf91b31a1eabd4c82ba1ecd5-2206-4221-a12904&sso=4fe3ece8-730e1ce698826110d061df6d8d8da141de828db43b0e0f11&ssp=61588969321645906622164596479056741&ssq=81065887686961459829476869466467600833866&ssr=OTQuMjI1LjEyLjc3&sst=Mozilla/5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/98.0.4758.102%20Safari/537.36&ssv=&ssw=&ssx=W10=
