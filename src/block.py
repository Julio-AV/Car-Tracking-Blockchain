import header
class block:
    def __init__(self, header, transactions):
        self.header = header
        self.transactions = transactions
    def calculate_hash(self, header):
        