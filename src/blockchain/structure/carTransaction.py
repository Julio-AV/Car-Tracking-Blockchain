from .transaction import Transaction
class CarTransaction(Transaction):
    def __init__(self, emitter, old_owner, new_owner, car_id):
        self.transaction_type = "transfer"
        self.old_owner = old_owner
        self.new_owner = new_owner
        self.car_id = car_id
        super().__init__(emitter)
    
    def validate(self):
        """TODO: Implement function"""
        pass
    
    

    def _as_dict(self):
        """Return the transaction as a dictionary"""
        return {
            "transaction_type": self.transaction_type,
            "transaction_hash": self.transaction_hash,
            "emitter": self.emitter,
            "timestamp": self.timestamp,
            "signature": self.signature,
            "old_owner": self.old_owner,
            "new_owner": self.new_owner,
            "car_id": self.car_id
        }
    
    def _get_transaction_main_data(self):
        """Return the main data of the transaction as a dictionary
            This is used to calculate the hash of the transaction"""
        return {
            "transaction_type": self.transaction_type,
            "emitter": self.emitter,
            "timestamp": self.timestamp,
            "old_owner": self.old_owner,
            "new_owner": self.new_owner,
            "car_id": self.car_id
        }
    
        
if __name__ == '__main__':
    #python3 -m blockchain.structure.carTransaction
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import hashes
    import json
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    example_transaction = CarTransaction(
        emitter="user1",
        old_owner="user1",
        new_owner="user2",
        car_id="car123"
    )
    example_transaction.prepare_transaction(private_key)
    print(example_transaction.validate_signature(public_key))

    #Test for serialization and deserialization
    serialized = example_transaction.serialize()
    serialized = json.loads(serialized)
    recovered_transaction = CarTransaction(emitter=serialized["emitter"], old_owner=serialized["old_owner"], new_owner=serialized["new_owner"], car_id=serialized["car_id"])
    recovered_transaction.signature = serialized["signature"]
    recovered_transaction.timestamp = serialized["timestamp"]
    recovered_transaction.transaction_hash = serialized["transaction_hash"]
    print(recovered_transaction.serialize())
    print(recovered_transaction.validate_signature(public_key))
