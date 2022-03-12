import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import time


# Site descriptions

URL = 'https://www.zimmo.be/nl/panden/?status=2&type%5B0%5D=5&type%5B1%5D=1&type%5B2%5D=6&hash=14de828c2a744b723baa0ebfe4d02351&priceIncludeUnknown=1&priceChangedOnly=0&bedroomsIncludeUnknown=1&bathroomsIncludeUnknown=1&constructionIncludeUnknown=1&livingAreaIncludeUnknown=1&landAreaIncludeUnknown=1&commercialAreaIncludeUnknown=1&yearOfConstructionIncludeUnknown=1&epcIncludeUnknown=1&queryCondition=and&includeNoPhotos=1&includeNoAddress=1&onlyRecent=0&onlyRecentlyUpdated=0&isPlus=0&region=list&city=MzAYicAQAA%253D%253D&pagina='



# tag descriptions

container_root = '//*[@id="wrapper"]/div[3]/div[4]/div[2]/div[2]'
item_tag = 'property-item'
link_tag = 'property-item_title '

rent_tag = '//*[@id="main-features"]/div/div[1]/div[2]/div/span'
monthlyfee_tag = '//*[@id="tab-detail"]/div[2]/div/div[4]/div/div/div[1]/section/div/div[2]/div[2]/div[2]'
address_tag = '//*[@id="main-features"]/div/div[1]/div[1]/h2/span[1]'
type_tag = '//*[@id="main-features"]/div/div[2]/div[1]/ul/li[3]/span'
toilets_tag = ''
bedrooms_tag = ''

## Determine URL name



## Fetch URL instane data

def makeSoup(URL,driver):
    ### Fetch html file with selenium driver
    driver.get(URL)
    ### Make soup object
    soup = BeautifulSoup(driver.page_source,features="lxml")
    return soup

def setDriver(Driver):
    path = 'C:\Program Files\SeleniumDrivers'
    path = path+str(Driver)+'.exe'
    ser = Service(path)
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ser, options=op)
    return driver

def getItemLink(item):
    title = item.find_element(By.CLASS_NAME, link_tag)
    tag = title.find_element(By.TAG_NAME, "a")#find_element_by_tag_name("a")
    titleLink = tag.get_attribute('href')
    return titleLink

def findItemLinks(driver,URLb):
    page = 1
    links = []
    while(True):
        URL = str(URLb)+str(page)+'#gallery'
        #URL = 'https://www.zimmo.be/nl/panden/?status=2&type%5B0%5D=5&type%5B1%5D=1&type%5B2%5D=6&hash=14de828c2a744b723baa0ebfe4d02351&priceIncludeUnknown=1&priceChangedOnly=0&bedroomsIncludeUnknown=1&bathroomsIncludeUnknown=1&constructionIncludeUnknown=1&livingAreaIncludeUnknown=1&landAreaIncludeUnknown=1&commercialAreaIncludeUnknown=1&yearOfConstructionIncludeUnknown=1&epcIncludeUnknown=1&queryCondition=and&includeNoPhotos=1&includeNoAddress=1&onlyRecent=0&onlyRecentlyUpdated=0&isPlus=0&region=list&city=MzAYicAQAA%253D%253D&pagina='+str(page)+'#gallery'
        #URL = 'https://www.zimmo.be/nl/leuven-3000/te-huur/?pagina='+str(page)+'#gallery'
        driver.get(URL)
        try:
            root = driver.find_element(By.XPATH, container_root)
        except:
            break
        else:
            items = root.find_elements(By.CLASS_NAME, item_tag)
            for item in items:
                links.append(getItemLink(item))
            page+=1
            
    return links

def itemGetAddress(driver):
    address = driver.find_element(By.XPATH, address_tag)
    address = address.get_attribute("innerHTML")
    return address

def standardizeAddress(st):
    while(True):
        if(st[1][0].isnumeric()):
            break
        else:
            buf = [str(st[0])+" "+str(st[1])]
            st = buf+st[2:]

    if '/' in st: st.remove('/')

    for i in range(len(st)):
        if ',' in st[i]: st[i] = st[i].replace(',','')
        if '.' in st[i]: st[i] = st[i].replace('.','')

    street = 'Null'
    postal = 0
    city = 'Null'
    house_nr = 0
    bus_nr = 0


    if(len(st)==3):
        street = st[0]
        postal = int(st[1])
        city = st[2]

    if(len(st)==4):
        street = st[0]
        house_nr = st[1]
        postal = int(st[2])
        city = st[3]

    if(len(st)==5):
        while(True):
            if(st[2][0]=='0'):
                st[2]=st[2][1:]
            else:
                break
        street = st[0]
        house_nr = st[1]
        bus_nr = st[2]#int(st[2])
        postal = int(st[3])
        city = st[4]
    return street,postal,city,house_nr,bus_nr

def itemGetType(driver):
    try:
        itemtype = driver.find_element(By.XPATH, type_tag)
        itemtype = itemtype.get_attribute("innerHTML")
    except:
        itemtype = 'None'
    return itemtype

def itemGetRent(driver):
    rent = driver.find_element(By.XPATH, rent_tag)
    rent = rent.get_attribute("innerHTML")
    return rent
        
def itemGetMFee(driver):
    try:
        fee = driver.find_element(By.XPATH, monthlyfee_tag)
        fee = fee.get_attribute("innerHTML")
    except:
        fee = 'Null'
    return fee

def itemGetRent(driver):
    rent = driver.find_element(By.XPATH, rent_tag)
    rent = rent.get_attribute("innerHTML")
    return rent


def itemGetBathBedOpp(driver):
    container_tag = '//*[@id="main-features"]/div/div[2]/div[1]/ul/*'
    elements = driver.find_elements(By.XPATH, container_tag)

    bath = 'Null'
    bed = 'Null'
    opp = 'Null'
    for i in range(len(elements)):
        item = elements[i]
        label = item.find_elements(By.CLASS_NAME, 'feature-label')[0].get_attribute("innerHTML")
        value = item.find_elements(By.CLASS_NAME, 'feature-value')[0].get_attribute("innerHTML")
        value = value.replace(' ','')
        value = value.replace('\n','')

        if len(value)>21:
            if value[:21]=='<aclass="op-aanvraag"':
                value = 'op aanvraag'

        if label=='Badkamers':
            bath = value
        if label=='Slaapkamers':
            bed = value
        if label=='Woonopp.':
            opp = value
    return bath,bed,opp

def getEPC(driver):
    container_tag = '//*[@id="certificates"]/div[2]/*'#'//*[@id="certificates"]/div[1]/h3/*'
    elements = driver.find_elements(By.XPATH, container_tag)

    

    EPC = 'Null'
    for i in range(len(elements)):
        item = elements[i]

        try:
        
            label = item.find_elements(By.CLASS_NAME, 'col-xsm-7.info-name')[0].get_attribute("innerHTML")
            value = item.find_element(By.CLASS_NAME, 'col-xsm-5.info-value').find_element(By.CLASS_NAME, 'energie-label').get_attribute("src")

            if len(value)>21:
                if value[:21]=='<aclass="op-aanvraag"':
                    value = 'op aanvraag'

            if label=='Energieklasse':
                if value == 'https://www.zimmo.be/public/images/energielabels/epc_e.svg':
                    EPC = 'E'
                if value == 'https://www.zimmo.be/public/images/energielabels/epc_d.svg':
                    EPC = 'D'
                if value == 'https://www.zimmo.be/public/images/energielabels/epc_c.svg':
                    EPC = 'C'
                if value == 'https://www.zimmo.be/public/images/energielabels/epc_b.svg':
                    EPC = 'B'
        except:
            errorHandler()

    return EPC

def errorHandler():
    return None


def fetchItemData(driver,link):
    driver.get(link)
    WebDriverWait(driver, 5)
    site = 'Zimmo'
    itemtype = itemGetType(driver)
    rent = itemGetRent(driver).replace('\n','')
    rent = rent.replace(' ','')
    monthly_fee = itemGetMFee(driver)
    address = str(itemGetAddress(driver)).split() #Fetched correctly
    street,postal,city,house_nr,bus_nr = standardizeAddress(address)
    #surface = itemGetOpp(driver)
    #bathrooms = itemGetToilets(driver)
    #bedrooms = itemGetBedrooms(driver)
    bathrooms,bedrooms,surface = itemGetBathBedOpp(driver)
    epc_class = getEPC(driver)
    link = link



    return [site,itemtype,rent,monthly_fee,postal,city,street,house_nr,bus_nr,bathrooms,bedrooms,surface,epc_class,link]

            


def main(URL):    
    # set the driver
    driver = setDriver('\chromedriver')

    # Find for all properties the corresponding links
    links = findItemLinks(driver,URL)
    print('links found: ',len(links))

    # Find for each item the required data
    
    columns = ['site','itemtype','rent','monthly_fee','postalcode','city','street','house_number','bus_number','bathrooms','bedrooms','surface','epc_class','link']
    dataframe = pd.DataFrame(columns=columns)

    for i in range(len(links)):
        print('=', end =" ")
    print('')
    for link in links:#[:3]:
        data = fetchItemData(driver,link)
        dataframe.loc[0 if pd.isnull(dataframe.index.max()) else dataframe.index.max() + 1] = data
        #print(data)
        #print(links.index(link))
        print('=', end =" ")
        

    driver.quit()
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    #print(dataframe)
    dataframe.to_excel("Zimmo_output.xlsx")  
    return dataframe

#start = time.time()
    
main(URL)

#end = time.time()
#print(end - start)
