from pymongo import MongoClient

class LocCacheDB(MongoClient):

    def __init__(self):
        super(LocCacheDB, self).__init__()
        self.dbname = 'qa_loc'
        self.str_collection = 'str_loc_collection'
        self.ip_collection = 'ip_loc_collection'
        self.db_client = MongoClient('mongodb://localhost:27017/')
        self.db = self.db_client[self.dbname]
    def insert_str_loc(self, data):
        """ stmt_data format : {loc_dict}
            """
        str_coll = self.db[self.str_collection]
        stmt_id = str_coll.insert_one(data).inserted_id
        return stmt_id
    def get_str_loc(self, qry_str):
        str_coll = self.db[self.str_collection]
        stmt_doc = str_coll.find_one({'qry':qry_str})
        if stmt_doc:
            del stmt_doc['_id']
            return stmt_doc
    def insert_ip_loc(self, data):
        """ stmt_data format : {loc_dict}
            """
        ip_coll = self.db[self.ip_collection]
        stmt_id = ip_coll.insert_one(data).inserted_id
        return stmt_id
    def get_ip_loc(self, qry_str):
        ip_coll = self.db[self.ip_collection]
        stmt_doc = ip_coll.find_one({'qry':qry_str})
        if stmt_doc:
            del stmt_doc['_id']
            return stmt_doc

