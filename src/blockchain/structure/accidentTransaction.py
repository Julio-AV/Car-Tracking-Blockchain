from .transaction import Transaction
import json
class AccidentTransaction(Transaction):
    def __init__(self, transaction_hash, emitter, signature, car_id, driver_id, severity):
        super().__init__(transaction_hash, emitter, signature)
        self.transaction_type = "accident"
        self.car_id = car_id
        self.driver_id = driver_id
        self.severity = severity
    
    
    def validate(self, blockchain):
        pass


    def _as_dict(self):
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
if __name__ == '__main__':
    example_transaction = AccidentTransaction(
        transaction_hash="abc123",
        emitter="user1",
        
        signature="signature123",
        car_id="car123",
        driver_id="driver123",
        severity="high"
    )
    print(example_transaction.serialize())