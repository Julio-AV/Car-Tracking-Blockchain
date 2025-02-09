from .transaction import Transaction
import json
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
class AccidentTransaction(Transaction):
    def __init__(self, emitter, car_id, driver_id, severity):
        self.transaction_type = "accident"
        self.car_id = car_id
        self.driver_id = driver_id
        self.severity = severity
        super().__init__(emitter)
    
    
    def validate(self, blockchain):
        pass


    def _as_dict(self):
        """Used to serialize the transaction to broadcast"""
        return {
            "transaction_type": self.transaction_type,
            "transaction_hash": self.transaction_hash,
            "emitter": self.emitter,
            "timestamp": self.timestamp,
            "signature": self.signature,
            "car_id": self.car_id,
            "driver_id": self.driver_id,
            "severity": self.severity
        }
    def _get_transaction_main_data(self):
        """Used to calculate the hash of the transaction"""
        return {
            "transaction_type": self.transaction_type,
            "emitter": self.emitter,
            "timestamp": self.timestamp,
            "car_id": self.car_id,
            "driver_id": self.driver_id,
            "severity": self.severity
        }
if __name__ == '__main__':
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    example_transaction = AccidentTransaction(
        emitter="user1",
        car_id="car123",
        driver_id="driver123",
        severity="high"
    )
    example_transaction.prepare_transaction(private_key)
    print(example_transaction.serialize())
    #Validate signature
    print(example_transaction.validate_signature(public_key))
    bullshit_signature = "bullshit"
    example_transaction.signature = bullshit_signature
    print(example_transaction.validate_signature(public_key))