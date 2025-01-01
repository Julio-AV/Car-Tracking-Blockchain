from abc import ABC, abstractmethod
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
    def serialize(self):
        """Serialize the transaction to send to the network through the socket connections"""
        