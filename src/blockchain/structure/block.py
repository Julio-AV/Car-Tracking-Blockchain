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
        transaction_hashes.sort() # Sort the hashes so every node has the same merkle root
        while len(transaction_hashes) > 1:
            if len(transaction_hashes) % 2 != 0:
                transaction_hashes.append(transaction_hashes[-1])
            transaction_hashes = [sha256(transaction_hashes[i].encode() + transaction_hashes[i + 1].encode()).hexdigest() for i in range(0, len(transaction_hashes), 2)]
        self.header.merkle_root = transaction_hashes[0] # Add merkle root to block header
        return transaction_hashes[0]
            


            
    def calculate_hash(self):
        block_data = f"{self.previous_hash}"
        pass

    def add_transaction(self, transaction: Transaction):
        """Add a transaction to the block (pertinent checks will be done in the data handler)"""
        self.transactions.append(transaction)

if __name__ == '__main__':
    from inspectionTransaction import InspectionTransaction
    from accidentTransaction import AccidentTransaction
    from carTransaction import CarTransaction
    """Example of how to calculate the merkle root of a block"""
    inspection = InspectionTransaction(
        transaction_type="inspection",
        transaction_hash="abc123",
        emitter="user1",
        event="car_inspection",
        timestamp="2023-10-01T12:00:00Z",
        signature="signature123",
        car_id="car123",
        kilometers="10000"
    )    
    accident = AccidentTransaction(
        transaction_type="accident",
        transaction_hash="abc123",
        emitter="user1",
        event="car_accident",
        timestamp="2023-10-01T12:00:00Z",
        signature="signature123",
        car_id="car123",
        driver_id="driver123",
        severity="high"
    )
    car = CarTransaction(
        transaction_type="transfer",
        transaction_hash="abc123",
        emitter="user1",
        event="car_sale",
        timestamp="2023-10-01T12:00:00Z",
        signature="signature123",
        old_owner="user1",
        new_owner="user2",
        car_id="car123"
    )
    transactions = [inspection, accident, car]
    example_header = Header(
            previous_hash="0000000000000000000769f8a8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8",
            time_stamp="2023-10-01 12:00:00",
            block_number=1,
            validator_sign="validator_signature_example"
        )
    block = Block(header=example_header, transactions=transactions)
    print(block.calculate_merkle_root())