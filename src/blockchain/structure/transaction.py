from abc import ABC, abstractmethod
from hashlib import sha256
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import json
from datetime import datetime
class Transaction(ABC):
    def __init__(self, emitter, new_transaction = True):
        """Signature is made from outside, since python doesn't allow function overcharging"""
        #Transaction type is handled by subclasses
        #New transaction will be true if we are creating a transaction and false if we are deserializing a transaction from the network
        self.emitter = emitter
        if new_transaction:
            self.timestamp = self.get_timestamp()
            self.transaction_hash = self.calculate_hash()
        else:
            self.timestamp = None
            self.transaction_hash = None
    

    @abstractmethod
    def _as_dict(self):
        """Return the transaction as a dictionary"""
        
    @abstractmethod
    def pretty_print(self):
        """Return a pretty print of the transaction"""

    @abstractmethod
    def _get_transaction_main_data(self):
        """Return the main data of the transaction as a dictionary, used to calculate the hash of the transaction"""
    @abstractmethod
    def validate_transaction_content(self, blockchain):
        """Validate integrity of the contents of the blockchain, e.g, transaction of a car that doesn't exist on the blockchain"""

    def validate(self, public_key, blockchain):
        """Validate the data of the transaction"""
        signature_is_valid = self.validate_signature(public_key)
        transaction_content_is_valid = self.validate_transaction_content(blockchain)
        #TODO: Complete content validation and add it to return statement
        return signature_is_valid
    
    def prepare_transaction(self, private_key):
        """Prepare the transaction to be sent to the network, currently just a wrapper for sign"""
        # Sign the transaction
        self.sign(private_key)
    
    
    def serialize(self):
        """Serialize the transaction to send to the network through the socket connections"""
        return json.dumps(self._as_dict())
    
    @staticmethod
    def deserialize(self, serialized_transaction):
        """Deserialize the transaction to receive from the network through the socket connections"""
        transaction_dict = json.loads(serialized_transaction)
        return transaction_dict
    
    def calculate_hash(self):
        """Calculate the hash of the transaction"""
        dumps = json.dumps(self._get_transaction_main_data())
        return sha256(dumps.encode()).hexdigest()

    def get_timestamp(self):
        """Get the current timestamp"""
        current_date = datetime.now()
        date_format = "%d/%m/%Y %H:%M:%S"
        formatted_date = current_date.strftime(date_format)
        return formatted_date
    
    def sign(self, private_key):
        """Sign the transaction with the private key"""
        signature = private_key.sign(self.transaction_hash.encode(),
                                      padding.PSS(
                                          mgf=padding.MGF1(hashes.SHA256()), 
                                          salt_length=padding.PSS.MAX_LENGTH), 
                                hashes.SHA256())
        self.signature = signature.hex()
    
    def validate_signature(self, public_key):
        """Validate the signature of the transaction"""
        try:
            transaction_hash = self.calculate_hash()
            signature_bytes = bytes.fromhex(self.signature)
            public_key.verify(signature_bytes, transaction_hash.encode(),
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
    def __eq__(self, value):
        return isinstance(value, Transaction) and self._as_dict() == value._as_dict()