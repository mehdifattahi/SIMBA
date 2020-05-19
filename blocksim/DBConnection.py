from blocksim import MongoUtil


class DBConnection:
    mu = MongoUtil.MongoUtil("127.0.0.1", 3001)
    mu.initialize_db("SIMBA")

    def inserBlock_verification(self, value):
        self.mu.initialize_collection("block_verification")
        self.mu.insert(value)
        print(self.mu.find_all())

    def getAllBlock_verification(self):
        self.mu.initialize_collection("block_verification")
        return self.mu.find_all()
