import hashlib, json
from collections import OrderedDict


class MerkleTree:
    def __init__(self, listoftransaction=None):
        self.listoftransaction = listoftransaction
        self.ordered_transaction = OrderedDict()

    def create(self):
        listoftransaction = self.listoftransaction
        past_transaction = self.ordered_transaction
        temp_transaction = []

        for index in range(0, len(listoftransaction), 2):
            current = listoftransaction[index]
            if index + 1 != len(listoftransaction):
                current_right = listoftransaction[index + 1]
            else:
                current_right = ''
            current_hash = current
            if current_right != '':
                current_right_hash = current_right
            past_transaction[listoftransaction[index]] = current_hash
            if current_right != '':
                past_transaction[listoftransaction[index + 1]] = current_right_hash
            if current_right != '':
                temp_transaction.append(current_hash + current_right_hash)
            else:
                temp_transaction.append(current_hash)
        if len(listoftransaction) != 1:
            self.listoftransaction = temp_transaction
            self.ordered_transaction = past_transaction
            self.create()

    def Get_ordered_transacion(self):
        return self.ordered_transaction

    def Get_Root_node(self):
        last_key = list(self.ordered_transaction.keys())[-1]
        return self.ordered_transaction[last_key]

    def calculateMerkleRoot(self, txs):
        tx_hashes = []
        for tx in txs:
            tx_hashes.append(tx.hash)
        # transaction = ['t1', 't2', 't3', 't4']
        self.listoftransaction = tx_hashes
        self.create()

        past_transaction = self.Get_ordered_transacion()

        return self.Get_Root_node()
