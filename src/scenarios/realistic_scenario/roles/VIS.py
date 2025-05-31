from comms.node import Node
from blockchain.structure.inspectionTransaction import InspectionTransaction
from blockchain.structure.block import Block
from cryptography.hazmat.primitives.asymmetric import rsa
from utils.IP_file_handler import read_connections_from_file
import random
import time
class VIS(Node):
    # Inherit node class and extend it to add insurance company specific functionality
    def __init__(self):
        super().__init__()
        print(f"VIS node will open connections with: {read_connections_from_file(self.IP)}")

    def operate(self):
        print("Welcome aboard, VIS!")
        time.sleep(1)
        while len(self.blockchain) == 0:
            # Wait for the genesis block to be created by the governmental institution
            print("Waiting for the genesis block to be created...")
            time.sleep(0.5)
        # Once the genesis block is created, we can start operating
        print("Genesis block received, starting to operate...")
        while True:
            # Generate data to be sent to the network
            transaction = self._gen_data()
            if transaction is not None:
                transaction.prepare_transaction(self.private_key)
                serialized_transaction = transaction.serialize()
                self.queue_to_connectionHandler.put(serialized_transaction)
                print(f"Transaction {transaction.car_id} sent to connection handler")
            else:
                print("Something went wrong, no transaction generated, skipping...")
            # Sleep for a while before generating the next transaction
            time.sleep(2)

            
    def _gen_data(self):
        block_idx = random.randint(0, len(self.blockchain) - 1) if len(self.blockchain) > 0 else 0
        vehicle_id = random.choice(self.blockchain[block_idx].transactions).car_id # Get a random vehicle ID from the blockchain
        new_transaction = None
        # Search for the latest inspection transaction for the given vehicle ID
        for block in reversed(self.blockchain):
            for transaction in block.transactions:
                if isinstance(transaction, InspectionTransaction) and transaction.car_id == vehicle_id:
                    new_kilometers = int(transaction.kilometers) + random.randint(-15000, 50000)  # Random kilometers between 1000 and 200000
                    new_transaction = InspectionTransaction(
                        emitter=self.name,
                        car_id=transaction.car_id,
                        kilometers=str(new_kilometers)
                    )
                    return new_transaction
                
        #We iterated the blockchain and didn't find any inspection transaction for the given vehicle ID, therefore we need to create the first one
        new_kilometers = random.randint(1000, 50000)
        new_transaction = InspectionTransaction(
            emitter=self.name,
            car_id=vehicle_id,
            kilometers=str(new_kilometers)
        )
        return new_transaction