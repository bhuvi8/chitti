import urllib
import re
import json
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class DescLookup:
    def __init__(self):
        pass
    def __del__(self):
        pass
    # Extract the text definition from HTML page
    def gettextdefine(self, soup):
        res = ''
        attr = {'name':'description'}
        soi = soup.find('meta', attr)
        if soi != None:
            soi = soi.get('content')
            if soi != None:
                res = re.split(":|—", soi) #changed from 'usage' to '—' as of 03/2018
                del res[0]
                del res[-1]
                res = ' : '.join(res) 

        return res
    # Extract the text data from HTML pages
    def gettextonly(self, soup):
        res = ''
        attr = {'class':'script-run-on-ready'}
        soi = soup.find('script', attr)
        if soi != None:
            soi = soi.string
            soi = re.sub("^.*?{", "{", soi)
            soi = re.sub("}.../?$", "}", soi)
            res = self.parse_json(soi)
        return res
    def parse_json(self, string):
        """parse json and get relevant data from text
           removed[data] as we directly get it from json qry 03/2018
        """
        res = ''
        res_dict = {}
        parsed_data = json.loads(string)
        abs_txt = parsed_data['AbstractText']
        if not abs_txt: return ''
        info = ''
        if isinstance(parsed_data['Infobox'], dict):
            for key in parsed_data['Infobox'].keys():
                if key != 'content': continue
                for l in parsed_data['Infobox'][key]:
                    #print(l)
                    if l['data_type'] != 'string': continue
                    info += l['label'] + ' : '
                    info += l['value'] + '\r\n<BR>'
                    res_dict[l['label']] = l['value']
        data_src_url = parsed_data['AbstractURL']
        data_src_name = parsed_data['AbstractSource']
        entity = parsed_data['Entity']
        img_url = parsed_data['Image']
        if entity:
            res += 'Category : ' + entity + '\r\n<BR><BR>'
            res_dict['Entity'] = entity
        res += '<img src="'+ img_url + '" alt="Image"> <BR>'
        if info:
            res += 'Info : \r\n<BR>'
            res += info
        res += 'Description : \r\n<BR>'
        res += abs_txt + '\r\n<BR><BR>'
        res_dict['Description'] = abs_txt
        if data_src_url :
            res += 'Data source : <a href="' + data_src_url + '">'+ data_src_name+'</a> \r\n<BR>'
            res_dict['Source_url'] = data_src_url
            res_dict['Source_name'] = data_src_name
            #res += 'Powered by : <a href="https://duckduckgo.com/">Duckduckgo search</a> \r\n<BR>'
        #res += 'To contribute vist <a href="http://duckduckhack.com/">duckduckhack.com</a> \r\n<BR>'
        logger.debug(res_dict)
        return res
    def get_data(self, string, q_class='json'): #changed from 'about' to 'json' to directly fetch json
        res = ''
        logger.info("q_class_FC"+q_class)
        if q_class == 'def':
            url = 'http://www.merriam-webster.com/dictionary/'+string
            url = re.sub(' ', '%20', url)
        else:
            url = 'https://duckduckgo.com/?q='+string+'&o='+q_class
            url = re.sub(' ', '%20', url)
        logger.info('URL: '+url)
        try:
            data = urllib.request.urlopen(url).read()
        except:
            logger.exception("Error: %s could not be opened" %url)
            return res
        if q_class == 'def':
            soup = BeautifulSoup(data,"html5lib")
            res = self.gettextdefine(soup)
        else:
            #res = self.gettextonly(soup) #not required as we directly get json
            res = self.parse_json(data.decode('utf-8'))
        return res

