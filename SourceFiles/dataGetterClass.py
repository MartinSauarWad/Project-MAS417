from urllib.request import urlopen
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import dateutil.parser
import concurrent.futures# import ThreadPoolExecutor

class dataGetter:

    def __init__(self) -> None:
       self.availableSats = {}
       self.satCoords = {}

    def getSatNamesAndIDs(self):
        url = "https://sscweb.gsfc.nasa.gov/WS/sscr/2/observatories"
        webpage = urlopen(url).read()
        tree = ET.ElementTree(ET.fromstring(webpage))
        root = tree.getroot()

        availableSats = {}

        for data in zip(root.iter('{http://sscweb.gsfc.nasa.gov/schema}Name'),
                        root.iter('{http://sscweb.gsfc.nasa.gov/schema}Id'),
                        root.iter('{http://sscweb.gsfc.nasa.gov/schema}Resolution'),
                        root.iter('{http://sscweb.gsfc.nasa.gov/schema}EndTime'),
                        root.iter('{http://sscweb.gsfc.nasa.gov/schema}StartTime')):

            name = data[0].text
            id   = data[1].text
            resolution = int(data[2].text)
            endTimeStr = data[3].text
            startTimeStr  = data[4].text

            endTime = dateutil.parser.isoparse(endTimeStr).replace(tzinfo=None)
            startTime = dateutil.parser.isoparse(startTimeStr).replace(tzinfo=None)
            currentTime = datetime.now()

            if endTime > currentTime and currentTime > startTime and resolution == 60: #Sjekk om satelitten fremdeles er operativ
                availableSats[name] = id
        
        return availableSats




    def getSatCoord(self, satIDs):
        #Get the current datetime and the datetime 2min ago to satisfy the API's requirements
        now = datetime.now()
        earlier = now - timedelta(minutes=2)
        now = now.replace(microsecond=0).isoformat()
        now = now.replace('-', '').replace(':', '') + 'Z'
        earlier = earlier.replace(microsecond=0).isoformat()
        earlier = earlier.replace('-', '').replace(':', '') + 'Z'

        satCoords = {}
        for satID in satIDs:
            url = f"https://sscweb.gsfc.nasa.gov/WS/sscr/2/locations/{satID}/{earlier},{now}/geo/"
            #url = f"https://sscweb.gsfc.nasa.gov/WS/sscr/2/locations/{satID}/20221030T200500Z,20221030T200700Z/geo/"
            webpage = urlopen(url).read()
            tree = ET.ElementTree(ET.fromstring(webpage))
            root = tree.getroot()

            for data in zip(tree.iter('{http://sscweb.gsfc.nasa.gov/schema}Id'),
                            tree.iter('{http://sscweb.gsfc.nasa.gov/schema}Longitude'),
                            tree.iter('{http://sscweb.gsfc.nasa.gov/schema}Latitude'),
                            tree.iter('{http://sscweb.gsfc.nasa.gov/schema}RadialLength')):

                id = data[0].text
                lon = float(data[1].text)
                lat = float(data[2].text)
                rad = float(data[3].text)

                #print(f"RAD: {rad}")
                            
                satCoords[id] = (lon, lat, rad)
        return satCoords
        
        