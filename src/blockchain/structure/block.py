from .header import Header
from .transaction import Transaction
from hashlib import sha256
from datetime import datetime   
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
            transaction_hashes = [sha256((transaction_hashes[i] + transaction_hashes[i + 1]).encode()).hexdigest() for i in range(0, len(transaction_hashes), 2)]
        self.header.merkle_root = transaction_hashes[0] # Add merkle root to block header
        return transaction_hashes[0]
            

    def calculate_hash(self):
        """Calculate and set the hash of the block"""
        serialized_header = f"{self.header.previous_hash}{self.header.time_stamp}{self.header.block_number}{self.header.validator_sign}{self.header.merkle_root}"
        block_hash = sha256(serialized_header.encode()).hexdigest()
        self.header.block_hash = block_hash # Add hash to block
        return block_hash

    def set_timestamp(self):
        """Get the current timestamp"""
        current_date = datetime.now()
        date_format = "%d/%m/%Y %H:%M:%S"
        formatted_date = current_date.strftime(date_format)
        self.header.time_stamp = formatted_date
        return formatted_date
    
    def prepare_block(self):
        """Prepare the block for broadcasting by calculating its hash, merkle root and timestamp"""
        self.calculate_merkle_root()
        self.calculate_hash()
        self.set_timestamp()

    def add_transaction(self, transaction: Transaction):
        """Add a transaction to the block (pertinent checks will be done in the data handler)"""
        self.transactions.append(transaction)

    def validate(self):
        """Validate the block"""
        pass
    
    def serialize(self):
        """Serialize the block to send to the network through the socket connections"""
        pass

if __name__ == '__main__':
    from .inspectionTransaction import InspectionTransaction
    from .accidentTransaction import AccidentTransaction
    from .carTransaction import CarTransaction
    """Example of how to calculate the merkle root of a block"""
    inspection = InspectionTransaction(
        transaction_hash="abc123",
        emitter="user1",
        signature="signature123",
        car_id="car123",
        kilometers="10000"
    )    
    accident = AccidentTransaction(
        transaction_hash="abc123",
        emitter="user1",
        signature="signature123",
        car_id="car123",
        driver_id="driver123",
        severity="high"
    )
    car = CarTransaction(
        transaction_hash="abc123",
        emitter="user1",
        signature="signature123",
        old_owner="user1",
        new_owner="user2",
        car_id="car123"
    )
    transactions = [inspection, accident, car]
    example_header = Header(
            previous_hash="0000000000000000000769f8a8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8",
            block_number=1,
            validator_sign="validator_signature_example"
        )
    block = Block(header=example_header, transactions=transactions)
    block.prepare_block()
    print(block.header.merkle_root)
    print(block.header.block_hash)
    print(block.header.time_stamp)