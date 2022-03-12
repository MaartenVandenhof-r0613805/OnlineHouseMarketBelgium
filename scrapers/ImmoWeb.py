import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# Site descriptions

URL = 'https://www.immoweb.be/nl/zoeken/huis/te-huur/leuven/3000?countries=BE&page='

# tag descriptions

container_root = '//*[@id="offer"]/*'
item_tag = ''
link_tag = 'div/div[1]/a'

rent_tag = '//*[@id="main-features"]/div/div[1]/div[2]/div/span'
monthlyfee_tag = '//*[@id="tab-detail"]/div[2]/div/div[4]/div/div/div[1]/section/div/div[2]/div[2]/div[2]'
address_tag = '//*[@id="main-features"]/div/div[1]/div[1]/h2/span[1]'
type_tag = '//*[@id="main-features"]/div/div[2]/div[1]/ul/li[3]/span'
toilets_tag = ''
bedrooms_tag = ''



def setDriver(Driver):
    path = 'C:\Program Files\SeleniumDrivers'
    path = path+str(Driver)+'.exe'
    ser = Service(path)
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ser, options=op)
    return driver

    

def findItemLinks(driver,URLb):
    page = 1
    links = []
    key = ''
    WebDriverWait(driver, 5)
    while(True):
        URL = str(URLb)+str(page)+'&orderBy=relevance'
        driver.get(URL)

        # Check if there is a container list present (end of pages)
        try:
            driver.find_element(By.XPATH,'//*[@id="main-content"]')
        except: 
            break
        elements = driver.find_elements(By.XPATH,'//*[@id="main-content"]/*')
        for element in elements:
            try:
                element.find_element(By.XPATH,'article/div[1]/h2/a').get_attribute("href")
            except:
                link=''
            else:
                link = element.find_element(By.XPATH,'article/div[1]/h2/a').get_attribute("href")
                print(link)
                links.append(link)
        page+=1
       
            
    return links

def fetchItemData(driver,link):
    driver.get(link)
    WebDriverWait(driver, 5)
    items = []
    
    site = 'ImmoWeb'
    itemtype = '' #!!!!!!!!!
    rent = ''
    surface = ''
    epc_class = ''
    bathroom = ''
    monthly_fee = 'Null'
    address = ''
    postal = ''
    house_nr = ''
    bus_nr = ''
    city = ''
    street = ''

    itemtype = driver.find_element(By.XPATH,'//*[@id="classified-header"]/div/div/div[1]/div/div[2]/h1').text.replace(" ","")

    try:
        bus_nr = driver.find_element(By.XPATH,'//*[@id="classified-header"]/div/div/div[1]/div/div[3]/div[1]/div/button/span[1]/span').get_attribute("innerHTML").replace("\n","").replace(" ","").replace('Bus','')
    except:
        bus_nr = 'None'

    try:
        streetcombo = driver.find_element(By.XPATH,'//*[@id="classified-header"]/div/div/div[1]/div/div[3]/div[1]/div/button/span[1]').text.split()
        street = " ".join(streetcombo[:-1].remove('Bus'))
        house_nr = streetcombo[-1:][0]
    except:
        street = 'Op aanvraag'
        house_nr = 'None'

    try:
        postalcombo = driver.find_element(By.XPATH,'//*[@id="classified-header"]/div/div/div[1]/div/div[3]/div[1]/div/button/span[2]').text.split()
        postal = postalcombo[0]
        city = postalcombo[2]
    except:
        postal = 'Op aanvraag'
        city = 'Op aanvraag'
   
    tables = driver.find_elements(By.XPATH,'//*[@id="main-content"]/div[3]/*')[4:]
    for table in tables:
        
        items = table.find_elements(By.XPATH,'div/div/div/div/div[2]/table/tbody/*')
        for item in items: #tr
            try:
                item.find_element(By.XPATH,'th')
                try:
                    item.find_element(By.XPATH,'td')
                except:
                    None
                else:
                    subject = re.sub('<[^>]+>', '', item.find_element(By.XPATH,'th').get_attribute('innerHTML').replace(" ","").replace("\n",""))
                    value = re.sub('<[^>]+>', '', item.find_element(By.XPATH,'td').get_attribute('innerHTML').replace(" ","").replace("\n",""))
                    

                    if(subject=='Bewoonbareoppervlakte'):
                        surface = value[:-15]
                    if(subject=='Slaapkamers'):
                        bedroom = value
                    if(subject=='Badkamers'):
                        bathroom = value
                    if(subject=='Energieklasse'):
                        epc_class = value
                    if(subject=='Primairenergieverbruik'):
                        epc_value = int(value[:-35])
                        if(epc_value<=0):
                            epc_class='A+'
                        if(epc_value<100 and epc_value>=0):
                            epc_class='A'
                        if(epc_value<200 and epc_value>=100):
                            epc_class='B'
                        if(epc_value<300 and epc_value>=200):
                            epc_class='C'
                        if(epc_value<400 and epc_value>=300):
                            epc_class='D'
                        if(epc_value<500 and epc_value>=400):
                            epc_class='E'
                        if(epc_value>=500):
                            epc_class='F'
                    if(subject=='Maandelijksehuurprijs'):
                        rent = value[:(int)(-len(value)/2)]
            except:
                None

            
            

    
    return site,itemtype,rent,monthly_fee,postal,city,street,house_nr,bus_nr,bathroom,bedroom,surface,epc_class,link
    
    


def main(URL):    
    # set the driver
    driver = setDriver('\chromedriver')

    # Find for all properties the corresponding links
    links = findItemLinks(driver,URL)
    print('links found: ',len(links))

    columns = ['site','itemtype','rent','monthly_fee','postalcode','city','street','house_number','bus_number','bathrooms','bedrooms','surface','epc_class','link']
    dataframe = pd.DataFrame(columns=columns)
    
    # Find the specific values for each link
    for i in range(len(links)):
        print('=', end =" ")
    print('')
    for link in links:#[:3]:
        data = fetchItemData(driver,link)
    
        dataframe.loc[0 if pd.isnull(dataframe.index.max()) else dataframe.index.max() + 1] = data
        #print(links.index(link))
        print('=', end =" ")
    
    driver.quit()
    
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    #print(dataframe)
    dataframe.to_excel("ImmoWeb_output.xlsx")
    return dataframe
    
#main(URL)






