from comms.node import Node
from blockchain.structure.accidentTransaction import AccidentTransaction
from blockchain.structure.block import Block
from cryptography.hazmat.primitives.asymmetric import rsa
from utils.IP_file_handler import read_connections_from_file
import random
import time
class InsuranceCompany(Node):
    # Inherit node class and extend it to add insurance company specific functionality
    def __init__(self):
        super().__init__()
        print(f"Insurance Company node will open connections with: {read_connections_from_file(self.IP)}")

    def operate(self):
        # Override the start method to add insurance company specific functionality
        print("Welcome aboard, insurance company!")
        time.sleep(1)  # Give time for the connection handler and data handler to start
        while len(self.blockchain) == 0:
            # Wait for the genesis block to be created by the governmental institution
            print("Waiting for the genesis block to be created...")
            time.sleep(0.5)
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
            # With data, there is an aproximate 5 seconds delay between each accident, therefore we simulate this by sleeping 5 seconds
            time.sleep(5)
            
    def _gen_data(self):
        #Get random car ID from the blockchain
        SEVERITY_LEVELS = ["low", "medium", "high", "totalLoss"]
        if len(self.blockchain) == 0:
            #Defensive programming, we always wait first for the genesis block to be created
            print("No blocks in the blockchain, cannot generate data.")
            return None
        #Every transaction has a car ID, so we can get any transaction from the blockchain
        random_block = random.choice(self.blockchain)
        random_transaction = random.choice(random_block.transactions)
        random_car_id = random_transaction.car_id
        # Create a new transaction for insurance
        transaction =   AccidentTransaction(
        emitter=self.name,
        car_id=random_car_id,
        driver_id= random.randint(100000, 999999), # Generate random driver ID
        severity= random.choice(SEVERITY_LEVELS) #Get a random severity level
        )
        return transaction
    
if __name__ == "__main__":
    # If this file is run directly, create a InsuranceCompany node and start it
    node = InsuranceCompany()
    node.start()