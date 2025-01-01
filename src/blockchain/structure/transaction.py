from abc import ABC, abstractmethod
from hashlib import sha256
import json
class Transaction(ABC):
    def __init__(self, transaction_type, transaction_hash, emitter, event, timestamp, signature):
        self.transaction_type = transaction_type
        self.transaction_hash = transaction_hash
        self.emitter = emitter
        self.event = event
        self.timestamp = timestamp
        self.signature = signature
    
    @abstractmethod
    def validate(self):
        """Validate the data of the transaction"""
    
    @abstractmethod
    def calculate_hash(self):
        """Calculate the hash of the transaction"""

    @abstractmethod
    def _as_dict(self):
        """Return the transaction as a dictionary"""
        
    def serialize(self):
        """Serialize the transaction to send to the network through the socket connections"""
        return json.dumps(self._as_dict())
    
    def calculate_hash(self):
        """Calculate the hash of the transaction"""
        return sha256(self.serialize().encode()).hexdigest()
        