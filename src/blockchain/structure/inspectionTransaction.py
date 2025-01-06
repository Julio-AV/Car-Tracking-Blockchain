from .transaction import Transaction
from .block import Block
import json
class InspectionTransaction(Transaction):
    def __init__(self, transaction_hash, emitter, signature, car_id, kilometers):
        super().__init__(transaction_hash, emitter, signature)
        self.transaction_type = "inspection"
        self.car_id = car_id
        self.kilometers = kilometers
    
    def validate(self, blockchain: list[Block]):
        pass

    def _as_dict(self):
        return {
            "transaction_type": self.transaction_type,
            "transaction_hash": self.transaction_hash,
            "emitter": self.emitter,
            "timestamp": self.timestamp,
            "signature": self.signature,
            "car_id": self.car_id,
            "kilometers": self.kilometers
        }
        
if __name__ == '__main__':
    example_transaction = InspectionTransaction(
        transaction_hash="abc123",
        emitter="user1",
        signature="signature123",
        car_id="car123",
        kilometers="10000"
    )
    print(example_transaction.serialize())
    print(example_transaction.calculate_hash())
    
