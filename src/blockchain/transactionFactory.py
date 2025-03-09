from .structure import Transaction, CarTransaction, AccidentTransaction, InspectionTransaction, Block, Header
import json
class TransactionFactory:
    @staticmethod
    def create_transaction(serialized_transaction : str | dict) -> Transaction:
        """Create a transaction from a serialized transaction received from the network,
         this function maps the transaction serialized json to the correct class"""
        try:
            if type(serialized_transaction) == str:
                transaction = json.loads(serialized_transaction)
            else:
                transaction = serialized_transaction
            transaction_type = transaction['transaction_type']
            if transaction_type == 'inspection':
                built_transaction = InspectionTransaction(
                    emitter=transaction['emitter'],
                    car_id=transaction['car_id'],
                    kilometers=transaction['kilometers'],
                    new_transaction=False
                )
                built_transaction.timestamp = transaction['timestamp']
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
                built_transaction.timestamp = transaction['timestamp']
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
                built_transaction.timestamp = transaction['timestamp']
                built_transaction.transaction_hash = transaction['transaction_hash'] 
                built_transaction.signature=transaction['signature'] 
                return built_transaction
            else:
                print(f"Invalid transaction type {transaction_type}")
                return None
        except KeyError:
            print(f"Invalid transaction format: {transaction}")
            return None
    @staticmethod
    def create_block(serialized_block: str | dict) -> Block:
        """Create a block from a serialized block received from the network"""
        try:
            if type(serialized_block) == str:
                deserialized_block = json.loads(serialized_block)
            else:
                deserialized_block = serialized_block
            header_dict = deserialized_block['header'] # Create header
            #Create header object
            header = Header(
                previous_hash=header_dict["previous_hash"],
                block_number=header_dict["block_number"],
            )
            header.block_hash = header_dict["block_hash"]
            header.merkle_root = header_dict["merkle_root"]
            header.time_stamp = header_dict["time_stamp"]
            header.validator_sign = header_dict["validator_sign"]
            
            #Create transactions from block
            transactions = []
            for transaction in deserialized_block['transactions']:
                print(transaction)
                transactions.append(TransactionFactory.create_transaction(transaction))
            block = Block(header.previous_hash, header.block_number, transactions, new_block=False)
            block.header = header
            return block
        except KeyError as e:
            print(f"KeyError while creating block from {serialized_block}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error while creating block from {serialized_block}: {e}")
            return None



