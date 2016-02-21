from pymongo import MongoClient
import copy


class ChatDB(MongoClient):

    def __init__(self):
        super(ChatDB, self).__init__()
        self.dbname = 'ml_qa_db'
        self.stmt_collection = 'stmt_collection'
        self.db_client = MongoClient('mongodb://localhost:27017/')
        self.db = self.db_client[self.dbname]
        #TODO: create unique index on class and tokens
        #db.stmt_collection.createIndex({class:1,tokens:1},{unique:true})
        
    def __del__(self):
        pass
        
    def insert_stmt(self, data):
        """ stmt_data format : {tokens: [], pos_tags: [],class='' }
            """
        stmt_id = self.get_stmt_id(data)
        if not stmt_id:
        	print('inserting doc to db')
        	stmt_coll = self.db[self.stmt_collection]
        	stmt_id = stmt_coll.insert_one(data).inserted_id
        return stmt_id
        
    def get_stmt_by_class(self, stmt_class):
        stmt_coll = self.db[self.stmt_collection]
        stmt_doc = stmt_coll.find_one({'class':stmt_class})
        if stmt_doc:
            del stmt_doc['_id']
            return stmt_doc
    def get_stmt_id(self, stmt):
        stmt_coll = self.db[self.stmt_collection]
        stmt_data = copy.deepcopy(stmt)
        del stmt_data['pos_tags']
        stmt_doc = stmt_coll.find_one(stmt_data,{'_id' : 1})
        if stmt_doc:
            return stmt_doc['_id']
        
    def insert_word(self, word_data):
        """word_data format : 
            { urlid : 'url_coll._id' , word : 'word', count: 'count', index: [index_pos]}
            """
        word_coll = self.db[self.word_collection]
        word_id = word_coll.insert_one(word_data).inserted_id
        return word_id
        
    def get_word_details(self, word_list):
        word_coll = self.db[self.word_collection]
        result_list = []
        for word_doc in word_coll.find({'word':{'$in': word_list}}):
            del word_doc['_id']
            result_list.append(word_doc)
        return result_list
