import hashlib, json
from collections import OrderedDict

class MerkleTreeTest:
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

            current_hash = hashlib.sha256(current.encode('utf-8'))

            if current_right != '':
                current_right_hash = hashlib.sha256(current_right.encode('utf-8'))

            past_transaction[listoftransaction[index]] = current_hash.hexdigest()

            if current_right != '':
                past_transaction[listoftransaction[index + 1]] = current_right_hash.hexdigest()

            if current_right != '':
                temp_transaction.append(current_hash.hexdigest() + current_right_hash.hexdigest())

            else:
                temp_transaction.append(current_hash.hexdigest())

        if len(listoftransaction) != 1:
            self.listoftransaction = temp_transaction
            self.ordered_transaction = past_transaction

            self.create()

    def Get_ordered_transacion(self):
        return self.ordered_transaction

    def Get_Root_node(self):
        last_key = list(self.ordered_transaction.keys())[-1]
        return self.ordered_transaction[last_key]


if __name__ == "__main__":
    tree = MerkleTreeTest()

    transaction = ['t1', 't2', 't3', 't4']

    tree.listoftransaction = transaction

    tree.create()

    past_transaction = tree.Get_ordered_transacion()

    print("Even number of transaction")
    print('Final root of the tree : ', tree.Get_Root_node())
    print((json.dumps(past_transaction, indent=4)))
    print("-" * 50)

    print("Odd number of transaction")
    tree = MerkleTreeTest()
    transaction = ['t1', 't2', 't3', 't4', 't5']
    tree.listoftransaction = transaction
    tree.create()
    past_transaction = tree.Get_ordered_transacion()
    print('Final root of the tree : ', tree.Get_Root_node())
    print((json.dumps(past_transaction, indent=4)))

