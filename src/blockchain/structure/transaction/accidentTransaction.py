from blockchain.structure.transaction.transaction import transaction
class AccidentTransaction(transaction):
    def __init__(self, transaction_type, transaction_hash, emitter, event, timestamp, signature, car_id, driver_id, severity):
        super().__init__(transaction_type, transaction_hash, emitter, event, timestamp, signature)
        self.car_id = car_id
        self.driver_id = driver_id
        self.severity = severity

    def validate(self):

    def serialize():
        pass