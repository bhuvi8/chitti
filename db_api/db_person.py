from pymongo import MongoClient

class PersonDB(MongoClient):

    def __init__(self):
        super(PersonDB, self).__init__()
        self.dbname = 'qa_person'
        self.person_collection = 'pers_coll'
        self.db_client = MongoClient('mongodb://localhost:27017/')
        self.db = self.db_client[self.dbname]
    def insert_person(self, data):
        """ stmt_data format : {person_dict}
            """
        per_coll = self.db[self.person_collection]
        stmt_id = str_coll.insert_one(data).inserted_id
        return stmt_id
    def get_per_det(self, qry_str):
    	""" qry_str format : {col : value}
    	"""
        per_coll = self.db[self.person_collection]
        stmt_doc = per_coll.find(qry_str)
        if stmt_doc:
            del stmt_doc['_id']
            return stmt_doc


