from .structure import Transaction, CarTransaction, AccidentTransaction, InspectionTransaction 
class TransactionFactory:
    @staticmethod
    def create_transaction(transaction : dict):
        try:
            transaction_type = transaction['transaction_type']
            if transaction_type == 'inspection':
                return InspectionTransaction(
                    transaction_hash=transaction['transaction_hash'],
                    emitter=transaction['emitter'],
                    signature=transaction['signature'],
                    car_id=transaction['car_id'],
                    kilometers=transaction['kilometers']
                )
            elif transaction_type == 'accident':
                return AccidentTransaction(
                    transaction_hash=transaction['transaction_hash'],
                    emitter=transaction['emitter'],
                    signature=transaction['signature'],
                    car_id=transaction['car_id'],
                    driver_id=transaction['driver_id'],
                    severity=transaction['severity']
                )
            elif transaction_type == 'transfer':
                return CarTransaction(
                    transaction_hash=transaction['transaction_hash'],
                    emitter=transaction['emitter'],
                    signature=transaction['signature'],
                    old_owner=transaction['old_owner'],
                    new_owner=transaction['new_owner'],
                    car_id=transaction['car_id']
                )
            else:
                print(f"Invalid transaction type {transaction_type}")
                return None
        except KeyError:
            print(f"Invalid transaction format: {transaction}")
            return None

if __name__ == '__main__':
    inspection_transaction = {"transaction_type": "inspection", "transaction_hash": "abc123", "emitter": "user1", "timestamp": "06/01/2025 17:10:41", "signature": "signature123", "car_id": "car123", "kilometers": "10000"}
    inspection_instance = TransactionFactory.create_transaction(inspection_transaction)
    print(inspection_instance.serialize())
    accident_transaction = {"transaction_type": "accident", "transaction_hash": "abc123", "emitter": "user1", "timestamp": "06/01/2025 17:24:41", "signature": "signature123", "car_id": "car123", "driver_id": "driver123", "severity": "high"}
    accident_instance = TransactionFactory.create_transaction(accident_transaction)
    print(accident_instance.serialize())
    transfer_transaction = {"transaction_type": "transfer", "transaction_hash": "abc123", "emitter": "user1", "timestamp": "06/01/2025 17:28:30", "signature": "signature123", "old_owner": "user1", "new_owner": "user2", "car_id": "car123"}
    transfer_instance = TransactionFactory.create_transaction(transfer_transaction)
    print(transfer_instance.serialize())
    invalid_transaction = {"transaction_type": "invalid", "transaction_hash": "abc123", "emitter": "user1", "timestamp": "06/01/2025 17:28:30", "signature": "signature123", "old_owner": "user1", "new_owner": "user2", "car_id": "car123"}
    invalid_instance = TransactionFactory.create_transaction(invalid_transaction)
    print(invalid_instance)
    bullshit_transaction = {"This is absolute bullshit": 1}
    bullshit_instance = TransactionFactory.create_transaction(bullshit_transaction)
