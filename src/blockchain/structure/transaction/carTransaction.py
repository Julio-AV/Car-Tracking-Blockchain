from blockchain.structure.transaction.transaction import transaction
class CarTransaction(transaction):
    def __init__(self, transaction_type, transaction_hash, emitter, event, timestamp, signature, old_owner, new_owner, car_id):
        super().__init__(transaction_type, transaction_hash, emitter, event, timestamp, signature)
        self.old_owner = old_owner
        self.new_owner = new_owner
        self.car_id = car_id

    def validate(self):
        """TODO: Implemente function"""