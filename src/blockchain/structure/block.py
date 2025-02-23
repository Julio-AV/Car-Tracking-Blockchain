from .header import Header
from .transaction import Transaction
from hashlib import sha256
from datetime import datetime   
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import json
class Block:
    def __init__(self, previous_hash, block_number ,transactions: list[Transaction], new_block = True):
        """Signature is made from outside, since python is a piece of shit and doesn't allow function overcharging"""
        self.header: Header = Header(previous_hash= previous_hash, block_number= block_number)
        self.transactions = transactions
        if new_block:
            #In case it is a received block, the factory will handle the creation of the block
            self.calculate_merkle_root()
            self.set_timestamp()
            self.calculate_hash()

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
        serialized_header = json.dumps(self.header._get_header_main_data())
        block_hash = sha256(serialized_header.encode()).hexdigest()
        self.header.block_hash = block_hash # Add hash to block header
        return block_hash
    


    def set_timestamp(self):
        """Get the current timestamp"""
        current_date = datetime.now()
        date_format = "%d/%m/%Y %H:%M:%S"
        formatted_date = current_date.strftime(date_format)
        self.header.time_stamp = formatted_date
        return formatted_date
    
    def sign_block(self, private_key):
        """Sign the block with the validator's private key"""
        signature = private_key.sign(self.header.block_hash.encode(),
                                      padding.PSS(
                                          mgf=padding.MGF1(hashes.SHA256()), 
                                          salt_length=padding.PSS.MAX_LENGTH), 
                                hashes.SHA256())
        self.header.validator_sign = signature.hex()

    def validate_signature(self, public_key):
        """Validate the signature of the transaction"""
        try:
            signature_bytes = bytes.fromhex(self.header.validator_sign)
            public_key.verify(signature_bytes, self.header.block_hash.encode(),
                                padding.PSS(
                                    mgf=padding.MGF1(hashes.SHA256()), 
                                    salt_length=padding.PSS.MAX_LENGTH), 
                                hashes.SHA256())
            return True
        except InvalidSignature:
            return False
        except ValueError as e:
            print("Transaction rejected due to value error: ", e)
            return False
    
    def prepare_block(self, private_key):
        """Prepare the block for broadcasting by calculating its hash, merkle root and timestamp"""
        self.sign_block(private_key=private_key)

    def validate(self):
        """Validate the block"""
        pass
    
    def _as_dict(self):
        """Return the block as a dictionary"""
        return {
            "header": self.header._as_dict(),
            "transactions": [transaction._as_dict() for transaction in self.transactions]
        }
    def serialize(self):
        """Serialize the block to send to the network through the socket connections"""
        return json.dumps(self._as_dict())

if __name__ == '__main__':
    from .inspectionTransaction import InspectionTransaction
    from .accidentTransaction import AccidentTransaction
    from .carTransaction import CarTransaction
    inspection_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = inspection_key.public_key()
    inspection_example = InspectionTransaction(
        emitter="user1",
        car_id="car123",
        kilometers="10000"
    )
    inspection_example.prepare_transaction(inspection_key)

    accident_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = accident_key.public_key()
    accident_example = AccidentTransaction(
        emitter="user1",
        car_id="car123",
        driver_id="driver123",
        severity="high"
    )
    accident_example.prepare_transaction(accident_key)
    car_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = car_key.public_key()
    car_transaction = CarTransaction(
        emitter="user1",
        old_owner="user1",
        new_owner="user2",
        car_id="car123"
    )
    car_transaction.prepare_transaction(car_key)

    block_owner_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key_block_owner_key = block_owner_key.public_key()
    transaction_list = [inspection_example, accident_example, car_transaction]
    block = Block("0", 1, transaction_list)
    block.prepare_block(block_owner_key)    
    print(block.header.serialize())