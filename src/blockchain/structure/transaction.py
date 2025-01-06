from abc import ABC, abstractmethod
from hashlib import sha256
import json
from datetime import datetime
class Transaction(ABC):
    def __init__(self, transaction_hash, emitter, signature):
        self.transaction_type = None
        self.transaction_hash = transaction_hash
        self.emitter = emitter
        self.timestamp = self.get_timestamp()
        self.signature = signature
    
    @abstractmethod
    def validate(self):
        """Validate the data of the transaction"""

    @abstractmethod
    def _as_dict(self):
        """Return the transaction as a dictionary"""
        
    def serialize(self):
        """Serialize the transaction to send to the network through the socket connections"""
        return json.dumps(self._as_dict())
    
    def calculate_hash(self):
        """Calculate the hash of the transaction"""
        return sha256(self.serialize().encode()).hexdigest()

    def get_timestamp(self):
        """Get the current timestamp"""
        current_date = datetime.now()
        date_format = "%d/%m/%Y %H:%M:%S"
        formatted_date = current_date.strftime(date_format)
        return formatted_date
    