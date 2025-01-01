import blockchain.structure.header as header
from transaction import Transaction
from transaction import CarTransaction
from transaction import InspectionTransaction
from transaction import AccidentTransaction

class Block:
    def __init__(self, header: header, transactions: list[Transaction]):
        self.header = header
        self.transactions = transactions
    
    def calculate_merkle_root(self):
        for transaction in self.transactions:

            
    def calculate_hash(self):
        block_data = f"{self.previous_hash}{ pass}"