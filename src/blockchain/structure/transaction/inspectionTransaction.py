from transaction import Transaction
import json
class InspectionTransaction(transaction):
    def __init__(self, transaction_type, transaction_hash, emitter, event, timestamp, signature, car_id, kilometers):
        super().__init__(transaction_type, transaction_hash, emitter, event, timestamp, signature)
        self.car_id = car_id
        self.kilometers = kilometers
    
    def validate(self):
        pass

    def _as_dict(self):
        return {
            "transaction_type": self.transaction_type,
            "transaction_hash": self.transaction_hash,
            "emitter": self.emitter,
            "event": self.event,
            "timestamp": self.timestamp,
            "signature": self.signature,
            "car_id": self.car_id,
            "kilometers": self.kilometers
        }
        
    
