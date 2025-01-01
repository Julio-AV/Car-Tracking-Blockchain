from transaction import Transaction
import json
class CarTransaction(Transaction):
    def __init__(self, transaction_type, transaction_hash, emitter, event, timestamp, signature, old_owner, new_owner, car_id):
        super().__init__(transaction_type, transaction_hash, emitter, event, timestamp, signature)
        self.old_owner = old_owner
        self.new_owner = new_owner
        self.car_id = car_id
    
    def validate(self):
        """TODO: Implement function"""
        pass


    def _as_dict(self):
        """Return the transaction as a dictionary"""
        return {
            "transaction_type": self.transaction_type,
            "transaction_hash": self.transaction_hash,
            "emitter": self.emitter,
            "event": self.event,
            "timestamp": self.timestamp,
            "signature": self.signature,
            "old_owner": self.old_owner,
            "new_owner": self.new_owner,
            "car_id": self.car_id
        }
    
    def serialize(self):
        """Return the transaction as a JSON string to send over the network"""
        return json.dumps(self._as_dict())
        
if __name__ == '__main__':
    example_transaction = CarTransaction(
        transaction_type="transfer",
        transaction_hash="abc123",
        emitter="user1",
        event="car_sale",
        timestamp="2023-10-01T12:00:00Z",
        signature="signature123",
        old_owner="user1",
        new_owner="user2",
        car_id="car123"
    )
    print(example_transaction.serialize())