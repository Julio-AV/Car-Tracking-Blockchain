import blockchain.structure.header as header
class block:
    def __init__(self, header, transactions):
        self.header = header
        self.transactions = transactions
    
    def calculate_merkle_root(self):
        for transaction in self.transactions:
            
    def calculate_hash(self):
        block_data = f"{self.previous_hash}{ pass}"