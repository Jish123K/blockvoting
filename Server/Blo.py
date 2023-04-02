import hashlib

import pickle

import time

class Block:

    def __init__(self, index, transactions, previous_block_hash):

        self.index = index

        self.timestamp = time.time()

        self.transactions = transactions

        self.previous_block_hash = previous_block_hash

        self.block_hash = self.compute_block_hash()

    def compute_block_hash(self):

        """

        Compute the hash of the block using sha256

        """

        block_data = str(self.index) + str(self.timestamp) + str(self.transactions) + str(self.previous_block_hash)

        block_data_bytes = pickle.dumps(block_data)

        return hashlib.sha256(block_data_bytes).hexdigest()

    def __str__(self):

        return str(self.__dict__)

