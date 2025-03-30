from comms.node import Node
from blockchain.structure.carTransaction import CarTransaction
from blockchain.structure.block import Block
class ManagerNode(Node):
    #inherit node class and extend it to add manager specific functionality
    def __init__(self):
        super().__init__()

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
            old_owner="-",
            new_owner="First Owner",
            car_id="LJCPCBLCX11000237"
            )
        fake_key = self.public_keys["autonomous_node"]
        #example_transaction.sign(fake_key)

        