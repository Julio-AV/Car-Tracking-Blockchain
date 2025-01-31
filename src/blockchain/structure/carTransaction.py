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
    example_transaction = CarTransaction(
        emitter="user1",
        old_owner="user1",
        new_owner="user2",
        car_id="car123"
    )
    print(example_transaction.serialize())