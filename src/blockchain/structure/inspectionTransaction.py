from .transaction import Transaction
from .block import Block
import json
class InspectionTransaction(Transaction):
    def __init__(self, emitter, car_id, kilometers):
        self.transaction_type = "inspection"
        self.car_id = car_id
        self.kilometers = kilometers
        super().__init__(emitter)
    
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
    def _get_transaction_main_data(self):
        return {
            "transaction_type": self.transaction_type,
            "emitter": self.emitter,
            "timestamp": self.timestamp,
            "car_id": self.car_id,
            "kilometers": self.kilometers
        }
        
if __name__ == '__main__':
    #python3 -m blockchain.structure.inspectionTransaction
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import hashes
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    example_transaction = InspectionTransaction(
        emitter="user1",
        car_id="car123",
        kilometers="10000"
    )
    example_transaction.prepare_transaction(private_key)
    print(example_transaction.serialize())
    print(example_transaction.validate_signature(public_key))