from header import Header
from transaction import Transaction
from hashlib import sha256

class Block:
    def __init__(self, header: Header, transactions: list[Transaction]):
        self.header = header
        self.transactions = transactions
    
    def calculate_merkle_root(self):
        """Calculate the merkle root of the transactions of the block"""
        transaction_hashes = [transaction.calculate_hash() for transaction in self.transactions]
        transaction_hashes.sort()
        while len(transaction_hashes) > 1:
            if len(transaction_hashes) % 2 != 0:
                transaction_hashes.append(transaction_hashes[-1])
            transaction_hashes = [sha256(transaction_hashes[i] + transaction_hashes[i + 1]).hexdigest() for i in range(0, len(transaction_hashes), 2)]
        self.header.merkle_root = transaction_hashes[0]
            


            
    def calculate_hash(self):
        block_data = f"{self.previous_hash}"
        pass

    def add_transaction(self, transaction: Transaction):
        """Add a transaction to the block (pertinent checks will be done in the data handler)"""
        self.transactions.append(transaction)