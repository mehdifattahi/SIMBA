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

    def update(self, connection, blocks):
        # self.collection.update_one(json_obj)
        # self.collection.update({'connection': 'usa-1_usa-2'}, {'$addToSet': {
        #     'blocks': {'$each': [{'PPYAY357ae9': 0.23460006713867188}, {'OOYAY357ae9': 0.23460006713867188}]}}})
        self.collection.update({'connection': connection}, {'$addToSet': {'blocks': {'$each': blocks}}})

    def updateDict(self, connection, blocks):
        self.collection.update({'connection': connection}, {'$set': {'blocks': blocks}})

    def bulk_insert(self, json_objs):
        self.collection.insert_many(json_objs)

    def find_all(self):
        j = []
        result = self.collection.find()
        for doc in result:
            j.append(doc)
        return j

    def find_all_withoutID(self):
        result = self.collection.aggregate([{"$project": {'_id': 0}}])
        j = []
        for doc in result:
            j.append(doc)
        return j

    def getBlockPropagation(self, connection):
        result = self.collection.aggregate(
            [{'$match': {'connection': connection}}, {"$project": {'_id': 0, 'connection': 0}}])
        return result.next()['blocks']
        # j = []
        # print(result.next()['blocks'])
        # for doc in result:
        #     j.append(doc)
        #     if doc['blocks']:
        #         print(doc['blocks'])
