from pymongo import MongoClient


class SearchIndexDB(MongoClient):

    def __init__(self):
        self.dbname = 'search_engine_index'
        self.url_collection = 'url_collection'
        self.sent_collection = 'sent_collection'
        self.db_client = MongoClient('mongodb://localhost:27017/')
        self.db = self.db_client[self.dbname]
        #TODO : create text index on sent in sent_collection
        
    def __del__(self):
        pass
        
    def insert_url(self, url_data):
        """ url_data format : {term : 'string', url: 'url', links: [ linked-url-list] }
            """
        url_coll = self.db[self.url_collection]
        url_id = url_coll.insert_one(url_data).inserted_id
        return url_id
    
    def get_url_id(self, url=None, url_id=None, term=None):
        url_coll = self.db[self.url_collection]
        if url:
            url_id = url_coll.find_one({'url':url},{'_id':1})
        elif url_id:
            url_id = url_coll.find_one({'_id':url_id},{'_id':1})
        elif term:
            url_id = url_coll.find_one({'term':term},{'_id':1})    
        return url_id
        
    def get_url_data(self, url_id):
        url_coll = self.db[self.url_collection]
        url_data = url_coll.find_one({'_id':url_id},{'url':1})
        return url_data
        
    def insert_sent(self, sent_data):
        """word_data format : 
            { urlid : 'url_coll._id' , sent : 'sent'}
            """
        sent_coll = self.db[self.sent_collection]
        sent_id = sent_coll.insert_one(sent_data).inserted_id
        return sent_id
        
    def get_sent_dtls(self, search_term):
        sent_coll = self.db[self.sent_collection]
        result_list = []
        #requires text index enabled for sent [only on mongodb >= 2.4]
        sent_list = self.db.command("text","sent_collection",search=search_term)['results']
        
        #for sent_doc in sent_list:
            #del sent_doc['_id']
            #result_list.append(sent_doc)
        #return result_list
        return sent_list
    def get_rel_stmts(self, stmt_id, prev=False, next=True):
       sent_coll = self.db[self.sent_collection]
       sent_list = []
       #if prev:
           #sent_list.append(sent_coll.find({'_id':{ '$lt' : stmt_id}}).limit(1))
       if next:
           sent_list.append(sent_coll.find_one({'_id':{ '$gt' : stmt_id}}))
       return sent_list
