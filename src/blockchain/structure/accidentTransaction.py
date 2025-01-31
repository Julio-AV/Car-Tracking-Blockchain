from .transaction import Transaction
import json
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
    example_transaction = AccidentTransaction(
        emitter="user1",
        car_id="car123",
        driver_id="driver123",
        severity="high"
    )
    print(example_transaction.serialize())