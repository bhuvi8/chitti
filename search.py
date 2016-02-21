from db_api.db_search_engine import SearchIndexDB
import re

class Query:
    def __init__(self):
        self.db_con = SearchIndexDB()
        self.ignorewords=set(['the','of','to','a','in','is','it'])
        
    def getscoredlist(self,raw_result,qr):
        totalscores=dict([(row['obj']['sent'],row['score']*0.1) for row in raw_result])
        loc_result = self.locationscore(raw_result,qr)
        for sent in totalscores:
            #print("%s m:%f l:%f" %(sent,totalscores[sent],loc_result[sent]*1.9))
            totalscores[sent]+=(loc_result[sent]*1.9)
        return totalscores
    
    def normalize(self, scores):
        vmin=0.000001 # Avoid division by zero errors
        minscore=min(scores.values())
        return dict([(u,float(minscore)/max(vmin,l)) for (u,l) \
            in scores.items( )])
    
    def locationscore(self, rows, qr):
        res = {}
        q_list = qr.split()
        for row in rows:
            location = 0.000001
            count = 0
            for wd in q_list:
                if wd in self.ignorewords: continue
                count += 1
                try:
                    #less is better
                    match = re.search(wd, row['obj']['sent'].lower())
                    location += match.start()
                except:
                    location += 100000
            res[row['obj']['sent']] = location/count
        return self.normalize(res)
        
    def search(self,q):
        q_list = q.split()
        stemmed_list = []
        for word in q_list:
            stemmed_list.append(word.lower()) #TODO: add stemmed words
        qr = ' '.join(stemmed_list)
        word_data_list=self.db_con.get_sent_dtls(q)
        if not word_data_list : 
            print("No results found")
            return None,None
        raw_result = []
        for word_data in word_data_list:
            url_name = self.db_con.get_url_data(word_data['obj']['url_id'])
            del word_data['obj']['url_id']
            word_data['obj']['url'] = url_name
            raw_result.append(word_data)
        del word_data_list
        if not raw_result: 
            print("No results found")
            return None,None
        scores=self.getscoredlist(raw_result,qr)
        rankedscores=sorted([(score,sent) for (sent,score) in scores.items( )],reverse=1)
        return rankedscores[0][1],rankedscores[0:15]
        
