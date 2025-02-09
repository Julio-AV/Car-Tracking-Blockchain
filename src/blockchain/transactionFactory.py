from .structure import Transaction, CarTransaction, AccidentTransaction, InspectionTransaction 
import json
class TransactionFactory:
    @staticmethod
    def create_transaction(serialized_transaction : str) -> Transaction:
        """Create a transaction from a serialized transaction received from the network,
         this function maps the transaction serialized json to the correct class"""
        try:
            transaction = json.loads(serialized_transaction)
            print(transaction)
            transaction_type = transaction['transaction_type']
            if transaction_type == 'inspection':
                built_transaction = InspectionTransaction(
                    emitter=transaction['emitter'],
                    car_id=transaction['car_id'],
                    kilometers=transaction['kilometers'],
                    new_transaction=False
                )
                built_transaction.transaction_hash = transaction['transaction_hash']
                built_transaction.signature = transaction['signature']
                return built_transaction
            
            elif transaction_type == 'accident':
                built_transaction = AccidentTransaction(
                    emitter=transaction['emitter'],
                    car_id=transaction['car_id'],
                    driver_id=transaction['driver_id'],
                    severity=transaction['severity'],
                    new_transaction=False
                )
                built_transaction.transaction_hash = transaction['transaction_hash']
                built_transaction.signature = transaction['signature']
                return built_transaction
            elif transaction_type == 'transfer':
                built_transaction = CarTransaction(
                    emitter=transaction['emitter'],
                    old_owner=transaction['old_owner'],
                    new_owner=transaction['new_owner'],
                    car_id=transaction['car_id'],
                    new_transaction=False
                )
                built_transaction.transaction_hash = transaction['transaction_hash'] 
                built_transaction.signature=transaction['signature'] 
                return built_transaction
            else:
                print(f"Invalid transaction type {transaction_type}")
                return None
        except KeyError:
            print(f"Invalid transaction format: {transaction}")
            return None


