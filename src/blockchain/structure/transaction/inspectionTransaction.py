from transaction import Transaction
import json
class InspectionTransaction(transaction):
    def __init__(self, transaction_type, transaction_hash, emitter, event, timestamp, signature, car_id, kilometes):
        super().__init__(transaction_type, transaction_hash, emitter, event, timestamp, signature)
        self.car_id = car_id
        self.kilometes = kilometes
    
    def validate(self):
        pass

    def serialize():
        pass
    
