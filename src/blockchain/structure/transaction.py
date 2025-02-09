from abc import ABC, abstractmethod
from hashlib import sha256
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import json
from datetime import datetime
import logging
class Transaction(ABC):
    def __init__(self, emitter,  signature = None):
        #Transaction type is handled by subclasses
        #If signature is None, then we are creating a new transaction -> we need to sign it
        #If signature is not None, then we are receiving a transaction -> we need to validate it
        self.emitter = emitter
        self.timestamp = self.get_timestamp()
        self.transaction_hash = self.calculate_hash()
        self.signature = signature # Signature of the transaction 
    
    @abstractmethod
    def validate(self):
        """Validate the data of the transaction"""

    @abstractmethod
    def _as_dict(self):
        """Return the transaction as a dictionary"""

    @abstractmethod
    def _get_transaction_main_data(self):
        """Return the main data of the transaction as a dictionary, used to calculate the hash of the transaction"""

    
    def prepare_transaction(self, private_key):
        """Prepare the transaction to be sent to the network, currently just a wrapper for sign"""
        # Sign the transaction
        self.sign(private_key)
        
    def serialize(self):
        """Serialize the transaction to send to the network through the socket connections"""
        return json.dumps(self._as_dict())
    
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
            signature_bytes = bytes.fromhex(self.signature)
            public_key.verify(signature_bytes, self.transaction_hash.encode(),
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
    