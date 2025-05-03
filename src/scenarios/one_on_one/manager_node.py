from comms.node import Node
from blockchain.structure.carTransaction import CarTransaction
from blockchain.structure.block import Block
from cryptography.hazmat.primitives.asymmetric import rsa
from utils.IP_file_handler import read_connections_from_file
import time
class ManagerNode(Node):
    #inherit node class and extend it to add manager specific functionality
    def __init__(self):
        super().__init__()
        print(f"Manager node will open connections with: {read_connections_from_file(self.IP)}")

    def generate_data(self):
        #Override the start method to add manager specific functionality
        print("Generating data...")
        example_transaction = CarTransaction(
            emitter=self.name,
            old_owner="-",
            new_owner="First Owner",
            car_id="LJCPCBLCX11000237"
            )
        example_transaction.prepare_transaction(self.private_key) 
        serialized_transaction = example_transaction.serialize()   
        self.queue_to_connectionHandler.put(serialized_transaction)
        print("Transaction sent to connection handler")

        manipulated_transaction = CarTransaction(
            emitter=self.name,
            old_owner="694034B",
            new_owner="485943K",
            car_id="BCKRCLLCX11000442"
            )
        
        fake_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        manipulated_transaction.sign(fake_key)
        serialized_manipulated_transaction = manipulated_transaction.serialize()
        self.queue_to_connectionHandler.put(serialized_manipulated_transaction)
        print("Manipulated transaction sent to connection handler")
        time.sleep(1)
        #Generate a block with the transaction
        block = Block("genesis_block", 1, [example_transaction], self.name)
        block.prepare_block(self.private_key)
        serialized_block = block.serialize()
        self.queue_to_connectionHandler.put(serialized_block)
        print("Block sent to connection handler")
        #Generate a block with the manipulated transaction
        time.sleep(1)
        block = Block("some_other_block", 2, [manipulated_transaction], self.name)
        block.prepare_block(self.private_key)
        serialized_block = block.serialize()
        self.queue_to_connectionHandler.put(serialized_block)
        print("Manipulated block sent to connection handler")
            
        

        