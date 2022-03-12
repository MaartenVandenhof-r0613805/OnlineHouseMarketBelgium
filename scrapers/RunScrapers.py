#import ImmoM
import ImmoProxio
import ImmoWeb
import Zimmo
import pandas as pd
import time

'''
# ImmoM
URL = 'http://immo-m.be/nl/te-huur/'
try:
    ImmoM.main(URL)
except:
    None
'''

Dataframes = []



start = time.time()
allstart = start
    





# ImmoWeb
start = time.time()

URL = 'https://www.immoweb.be/nl/zoeken/huis/te-huur/leuven/3000?countries=BE&page='
try:
    Dataframes.append(ImmoWeb.main(URL))
except:
    None

end = time.time()
print('Immoweb: ',end - start)


# ImmoProxio
start = time.time()
URL = 'https://www.immoproxio.be/nl/te-huur/leuven/appartement/'
try:
    Dataframes.append(ImmoProxio.main(URL))
except:
    None

end = time.time()
print('Immoproxio: ',end - start)

# Zimmo
start = time.time()
URL = 'https://www.zimmo.be/nl/panden/?status=2&type%5B0%5D=5&type%5B1%5D=1&type%5B2%5D=6&hash=14de828c2a744b723baa0ebfe4d02351&priceIncludeUnknown=1&priceChangedOnly=0&bedroomsIncludeUnknown=1&bathroomsIncludeUnknown=1&constructionIncludeUnknown=1&livingAreaIncludeUnknown=1&landAreaIncludeUnknown=1&commercialAreaIncludeUnknown=1&yearOfConstructionIncludeUnknown=1&epcIncludeUnknown=1&queryCondition=and&includeNoPhotos=1&includeNoAddress=1&onlyRecent=0&onlyRecentlyUpdated=0&isPlus=0&region=list&city=MzAYicAQAA%253D%253D&pagina='
try:
    Dataframes.append(Zimmo.main(URL))
except:
    None

end = time.time()
print('Zimmo: ',end - start)

print(len(Dataframes))
result = pd.concat(Dataframes)

result.to_excel("Merged_output.xlsx")

end = time.time()
print('Whole process: ',end - allstart)
