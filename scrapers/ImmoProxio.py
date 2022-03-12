import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import time


# Site descriptions

URL = 'https://www.immoproxio.be/nl/te-huur/leuven/appartement/'

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

def findLink(driver,root):
    link = root.find_element(By.XPATH, link_tag).get_attribute("href")
    return link
    

def findItemLinks(driver,URLb):
    page = 1
    links = []
    key = ''
    while(True):
        URL = str(URLb)+str(page)#+'/?c=1000876&h=0'
        driver.get(URL)

        # Check if first element url is the same
        if(key!='' and key==driver.find_element(By.XPATH, '//*[@id="offer"]/div[1]/div/div[1]/a').get_attribute("href")):
            break
        if(page==1):
            key = driver.find_element(By.XPATH, '//*[@id="offer"]/div[1]/div/div[1]/a').get_attribute("href")

        # Get the links for each adress
        
        
        #print(driver.find_element(By.XPATH, '//*[@id="offer"]/div[1]/div/div[1]/a').get_attribute("href"))
        items = driver.find_elements(By.XPATH, container_root)
        for item in items:
            links.append(findLink(driver,item))
        page+=1
            
    return links

def fetchItemData(driver,link):
    driver.get(link)
    WebDriverWait(driver, 5)
    items = []
    
    site = 'ImmoProxio'
    itemtype = 'Appartement' #!!!!!!!!!
    rent = ''
    surface = ''
    epc_class = ''
    bathroom = ''
    monthly_fee = ''
    address = ''
    postal = ''
    house_nr = ''
    bus_nr = ''
    city = ''
    street = ''



    textbox = driver.find_element(By.XPATH,'/html/body/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]/p[2]').get_attribute('innerHTML').split()
    #print(textbox)
    
    # Find address
    address = driver.find_element(By.XPATH,'//*[@id="detailmainsearch"]/span[2]').get_attribute("innerHTML")
    split = address.split()
    street = split[0]
    postal = '3000'
    city = 'Leuven'
    house_nr = split[1]
    if(len(split)>2):
        bus_nr = split[3]

    # Find rooms
    roomlist = driver.find_elements(By.XPATH,'html/body/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]/div/*')[1:]
    for room in roomlist:
        #print(room.get_attribute("innerHTML").replace(' ','').replace('\n','').replace(',',''))
        room_prop = room.get_attribute("innerHTML").replace(' ','').replace('\n','').replace(',','')
        if('Badkamer' in room_prop):
            if(len(room_prop)>8):
                bathroom = room_prop[8:-1]
            else:
                bathroom = '1'
        if('Slaapkamer' in room_prop):
            if(len(room_prop)>10):
                bedroom = room_prop[11:-1]
            else:
                bedroom = '1'
        
        if('Toilet' in room_prop):
            if(len(room_prop)>10):
                toilet = room_prop[11:-1]
            else:
                toilet = '1'

    
    # Find attributes
    tables = driver.find_elements(By.XPATH,'//*[@id="horizontalTab"]/div[2]/div[1]/*') # Get the div's
    for table in tables:
        items = table.find_elements(By.XPATH,'table/tbody/*')
        if (len(items)>0):
            for item in items:
                try:
                    subject = item.find_element(By.XPATH, 'td[1]/label').get_attribute("innerHTML")
                    value = item.find_element(By.XPATH, 'td[2]').get_attribute("innerHTML")
                    if(value==None):
                        value = item.find_element(By.XPATH, 'td[2]').text.replace(' ','')
                except:
                    subject = None
                    value = None


                if(subject=='Prijs'):
                    rent = value[2:-8]
                if(subject=='Bewoonbare oppervlakte'):
                    surface = value
                if(subject=='EPC waarde'):
                    try:
                        epc_value = int(value[:-7])
                    except:
                        epc_value = 'None'
                    else:
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
                        
                
                    
                    
    #print(epc_class)

    # Search all tables for the 


    
    

    return site,itemtype,rent,monthly_fee,street,postal,city,house_nr,bus_nr,bathroom,bedroom,surface,epc_class,link
    
    


def main(URL):    
    # set the driver
    driver = setDriver('\chromedriver')

    # Find for all properties the corresponding links
    links = findItemLinks(driver,URL)
    print('links found: ',len(links))

    columns = ['site','itemtype','rent','monthly_fee','postalcode','city','street','house_number','bus_number','bathrooms','bedrooms','surface','epc_class','link']
    dataframe = pd.DataFrame(columns=columns)


    for i in range(len(links)):
        print('=', end =" ")
    print('')
    # Find the specific values for each link
    for link in links:#[:3]:
        data = fetchItemData(driver,link)
        dataframe.loc[0 if pd.isnull(dataframe.index.max()) else dataframe.index.max() + 1] = data
        #print(links.index(link))
        print('=', end =" ")

    driver.quit()
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    #print(dataframe)
    dataframe.to_excel("ImmoProxio_output.xlsx")
    return dataframe
    
#main(URL)





# Find links



