import urllib
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
import nltk
from db_api.db_search_engine import SearchIndexDB

class Index:

    def __init__(self):
        self.db_con = SearchIndexDB()
        self.ignorewords=set(['the','of','to','and','a','in','is','it'])
    # Extract text data from HTML pages
    def gettextonly(self, soup):
        text = []
        l = soup.find_all('p')
        for i in l:
            i = i.text
            i = re.sub('\[\d+\]', '', i)
            text.append(i)
        return ' '.join(text)
    
    def isindexed(self, url):
        url_id = None
        url_id = self.db_con.get_url_id(url=url)
        return url_id
    
    # Index an individual page
    def addtoindex(self, url_id, soup):
        sent_dict = {}
        text = self.gettextonly(soup)
        sents = nltk.sent_tokenize(text)
        for i in sents:
            sent_data = {}
            sent_data['url_id'] = url_id
            sent_data['sent'] = i
            sent_id = self.db_con.insert_sent(sent_data)
        
    
    def addlinkref(self,url,link_urls):
        url_dict = {}
        url_dict['url'] = url
        url_dict['links'] = link_urls
        url_id = self.db_con.insert_url(url_dict)
        return url_id
        
    def index(self,url_list):
        for i in range(2):
            links_list = set()
            for url in url_list:
                try:
                    data = urllib.request.urlopen(url)
                except:
                    print("Error: %s could not be opened" %url)
                    continue
                soup = BeautifulSoup(data.read(),"lxml")
                links = soup('a')
                link_rel = set()
                for link in links:
                    if 'href' in dict(link.attrs):
                        link_url=urljoin(url,link['href'])
                        if link_url.find("'")!= -1 : continue
                        link_url = link_url.split('#')[0]
                        if link_url[0:4] == 'http':
                            links_list.add(link_url)
                            link_rel.add(link_url)
                if self.isindexed(url): continue
                url_id = self.addlinkref(url, list(link_rel))
                print("Indexing %s " %url)
                self.addtoindex(url_id, soup)
            url_list = links_list
            
