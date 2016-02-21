import urllib
import re
import json
import logging

logger = logging.getLogger(__name__)

class LocationLookup:
    def __init__(self):
        pass
    #parse json and return python objects
    def parse_json(self, data):
        parsed_data = json.loads(data)
        if isinstance(parsed_data, list):
            parsed_data = parsed_data[0]
        if isinstance(parsed_data, dict):
            lat = parsed_data.get('lat')
            lon = parsed_data.get('lon')
            if lat:
                del parsed_data['lat']
            if lon:
                del parsed_data['lon']
            parsed_data['loc'] = [lat, lon]
            if parsed_data.get('query'):
                del parsed_data['query']
        return parsed_data

    def get_location_by_ip(self, ip):
        res = ''
        url = 'http://ip-api.com/json/'+ip
        logger.debug(url)
        try:
            data = urllib.request.urlopen(url).read().decode('utf-8')
            return self.parse_json(data)
        except:
            logger.exception("Error: %s could not be opened" %url)
 
    def get_location_by_str(self,string):
        res = ''
        url = 'http://nominatim.openstreetmap.org/search?q=' + string + '&format=json&addressdetails=1&limit=1'
        url = re.sub(' ','+',url)
        logger.debug(url)
        try:
            data = urllib.request.urlopen(url).read().decode('utf-8')
            return self.parse_json(data)
        except:
            logger.exception("Error: %s could not be opened" %url)
            
