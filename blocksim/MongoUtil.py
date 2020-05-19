import pymongo


class MongoUtil:
    global client
    global db


    def __init__(self, host, port):
        self.client = pymongo.MongoClient(host, port)

    def initialize_db(self, db_name):
        self.db = self.client[db_name]

    def initialize_collection(self, coll_name):
        self.collection = self.db[coll_name]

    def insert(self, json_obj):
        self.collection.insert_one(json_obj)

    def upsert(self, json_obj):
        self.collection.update_one(json_obj)

    def bulk_insert(self, json_objs):
        self.collection.insert_many(json_objs)

    def find_all(self):
        j = []
        result = self.collection.find()
        for doc in result:
            j.append(doc)
        return j
