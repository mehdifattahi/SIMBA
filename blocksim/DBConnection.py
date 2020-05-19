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
        return self.mu.find_all_withoutID()

    def inserBlock_propagation(self, connection, blocks):
        self.mu.initialize_collection("block_propagation")
        self.mu.insert({'connection': connection, 'blocks': blocks})
        # print(self.mu.find_all())

    def updateBlock_propagationList(self, connection, blocks):
        self.mu.initialize_collection("block_propagation")
        self.mu.update(connection, blocks)

    def updateBlock_propagationDict(self, connection, blocks):
        self.mu.initialize_collection("block_propagation")
        self.mu.updateDict(connection, blocks)

        # {'$addToSet': {'blocks': {'$each': [{'PPYAY357ae9': 0.23460006713867188}, {'OOYAY357ae9': 0.23460006713867188}]}}})

    def getBlockPropagation(self, connection):
        self.mu.initialize_collection("block_propagation")
        return self.mu.getBlockPropagation(connection)
