from header import Header
from transaction import Transaction

class Block:
    def __init__(self, header: Header, transactions: list[Transaction]):
        self.header = header
        self.transactions = transactions
    
    def calculate_merkle_root(self):
        for transaction in self.transactions:
            pass

            
    def calculate_hash(self):
        block_data = f"{self.previous_hash}"
        pass