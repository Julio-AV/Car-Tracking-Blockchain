import blockchain.structure.header as header
from blockchain.structure.transaction.transaction import Transaction
from blockchain.structure.transaction.carTransaction import CarTransaction
from blockchain.structure.transaction.inspectionTransaction import InspectionTransaction
from blockchain.structure.transaction.accidentTransaction import AccidentTransaction
class Block:
    def __init__(self, header: header, transactions: list[transaction]):
        self.header = header
        self.transactions = transactions
    
    def calculate_merkle_root(self):
        for transaction in self.transactions:

            
    def calculate_hash(self):
        block_data = f"{self.previous_hash}{ pass}"