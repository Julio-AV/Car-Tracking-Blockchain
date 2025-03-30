from .header import Header
from .transaction import Transaction
from hashlib import sha256
from datetime import datetime   
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import json
class Block:
    def __init__(self, previous_hash, block_number ,transactions: list[Transaction], emmiter, new_block = True):
        """Signature is made from outside, since python is a piece of shit and doesn't allow function overcharging"""
        self.header: Header = Header(previous_hash= previous_hash, block_number= block_number, emmiter=emmiter)
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

    def validate(self, public_keys: dict, blockchain: list):
        """Validate the block"""
        # Validate the block signature
        if self.validate_signature(public_keys[self.header.emitter]) == False:
            print("Block signature is not valid")
            return False
        
        # Validate the transactions
        for transaction in self.transactions:
            try:
                public_key = public_keys[transaction.emitter]
            except KeyError:
                print(f"Transaction {transaction} was not valid, emitter {transaction.emitter} not found")
                return False
            if not transaction.validate(public_key, blockchain):
                print(f"Transaction {transaction} was not valid")
                return False
        # Validate the merkle root
        if self.header.merkle_root != self.calculate_merkle_root():
            print("Merkle root is not valid")
            return False
        # Validate the block hash
        if self.header.block_hash != self.calculate_hash():
            print("Block hash is not valid")
            return False
        return True
    
    def _as_dict(self):
        """Return the block as a dictionary"""
        return {
            "header": self.header._as_dict(),
            "transactions": [transaction._as_dict() for transaction in self.transactions]
        }
    def serialize(self):
        """Serialize the block to send to the network through the socket connections"""
        return json.dumps(self._as_dict())

    @staticmethod
    def deserialize(serialized_block):
        """Deserialize the block to receive from the network through the socket connections"""
        block_dict = json.loads(serialized_block)
        return block_dict
    
    def __eq__(self, value):
        is_equal = True
        try:
            if len(self.transactions) != len(value.transactions):
                return False
            for i in range(len(self.transactions)):
                if self.transactions[i] != value.transactions[i]:
                    is_equal = False
            return self.header == value.header and is_equal
        except AttributeError as e:
            print(e)
            return False
    def pretty_print(self):
        """Print the block in a structured, visually appealing way"""
        width = 100  # Ancho total del bloque
        padding = 20  # Espaciado para alinear bien las claves y valores

        print("+" + "-" * (width - 1) + "+")
        print("|" + " " * ((width // 2) - 3) + "BLOCK" + " " * ((width // 2) - 3) + "|")
        print("+" + "-" * (width - 1) + "+")

        print(f"| {'Block Number:':<{padding}} {self.header.block_number:<{width - padding - 4}} |")
        print(f"| {'Previous Hash:':<{padding}} {self.header.previous_hash:<{width - padding - 4}} |")
        print(f"| {'Merkle Root:':<{padding}} {self.header.merkle_root:<{width - padding - 4}} |")
        print(f"| {'Timestamp:':<{padding}} {self.header.time_stamp:<{width - padding - 4}} |")
        print(f"| {'Block Hash:':<{padding}} {self.header.block_hash:<{width - padding - 4}} |")
        print(f"| {'Validator Signature:':<{padding}} {self.header.validator_sign[:width - padding - 7]}... |")

        print("+" + "-" * (width - 1) + "+")
        print("| Transactions:" + " " * (width - 15) + "|")

        for transaction in self.transactions:
            transaction.signature = transaction.signature[:20] + "..."  # Truncate signature
            serialized_tx = transaction.serialize()
            for i in range(0, len(serialized_tx), width - 7):
                print(f"| - {serialized_tx[i:i + width - 5]:<{width - 5}} |")
            print("|" + " " * (width - 1) + "|")  # Empty line between transactions

        print("+" + "-" * (width-1) + "+")




if __name__ == '__main__':
    #python -m blockchain.structure.block
    from .inspectionTransaction import InspectionTransaction
    from .accidentTransaction import AccidentTransaction
    from .carTransaction import CarTransaction
    from ..transactionFactory import TransactionFactory
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
    block = Block("0", 1, transaction_list, "DGT")
    block.prepare_block(block_owner_key)    
    block.pretty_print()
    
    #Test serializing 
    block_serialized = block.serialize()
    print("\nBlock after serialization **********************************************\n")
    print(block_serialized)
    #Test deserializing
    print("\nBlock after deserialization **********************************************\n")
    deserialized_block = TransactionFactory.create_block(block_serialized)
    block.pretty_print()
    deserialized_block.pretty_print()
    print(deserialized_block == block)
    print(deserialized_block.validate_signature(public_key_block_owner_key))