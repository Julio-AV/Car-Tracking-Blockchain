from comms.node import Node
from blockchain.structure.carTransaction import CarTransaction
from blockchain.structure.block import Block
from cryptography.hazmat.primitives.asymmetric import rsa
from utils.IP_file_handler import read_connections_from_file
import random
import string
import time
class GovernmentalInstitution(Node):
    # Inherit node class and extend it to add governmental institution specific functionality
    def __init__(self):
        super().__init__()
        print(f"Governmental Institution node will open connections with: {read_connections_from_file(self.IP)}")

    def operate(self):
        # Override the start method to add governmental institution specific functionality
        print("Welcome aboard, governmental institution!")
        # First we generate some vehicles, so the other nodes can operate with them
        print("Generating initial vehicle registrations...")
        for _ in range(5):
            transaction = self._gen_data("new_vehicle")
            if transaction is not None:
                transaction.prepare_transaction(self.private_key)
                serialized_transaction = transaction.serialize()
                self.queue_to_connectionHandler.put(serialized_transaction)
                print(f"Initial vehicle registration {transaction.car_id} sent to connection handler")
            else:
                # We should never reach this since we are generating new vehicles and no None values should be returned
                raise ValueError("Failed to generate initial vehicle registration transaction.")
            # Sleep for a while before generating the next transaction
            time.sleep(0.2)
        # Now we generate the first block with the initial transactions
        print("Generating initial block with vehicle registrations...")
        initial_block = Block("genesis_block", 0, self.data_handler.transaction_list, self.name)
        initial_block.prepare_block(self.private_key)
        serialized_initial_block = initial_block.serialize()
        self.queue_to_connectionHandler.put(serialized_initial_block)
        print("Initial block sent to connection handler")
        # Clear the local transaction pool
        self._clear_transaction_list()
        while True:
            # Generate data to be sent to the network
            transaction = self._gen_data()
            if transaction is not None:
                transaction.prepare_transaction(self.private_key)
                serialized_transaction = transaction.serialize()
                self.queue_to_connectionHandler.put(serialized_transaction)
                print(f"Transaction {transaction.car_id} sent to connection handler")
            else:
                print("No transaction generated, skipping...")
            # Sleep for a while before generating the next transaction
            time.sleep(random.uniform(1, 3))

            #Check if we have enough transactions to create a block
            if len(self.data_handler.transaction_list) >= 5:
                print("Enough transactions to create a block, generating block...")
                
                block = Block(self.blockchain[-1].header.block_hash, len(self.blockchain), self.data_handler.transaction_list, self.name)
                block.prepare_block(self.private_key)
                serialized_block = block.serialize()
                self.queue_to_connectionHandler.put(serialized_block)
                print("Block sent to connection handler")
                # Clear the local transaction pool
                self._clear_transaction_list()

    def _gen_data(self, type_of_data=None):
        """
        This function is used to generate data of the governmental institutions nature
        """
        if type_of_data is None:
            # Randomly choose the type of data to generate
            type_of_data = random.choice(["new_vehicle", "vehicle_transfer"])
        transaction = None
        if type_of_data == "new_vehicle":
            # Generate a new vehicle registration transaction
            new_vehicle_vin = self._generate_chassis_number()
            new_owner = self._generate_vehicle_owner()
            transaction = CarTransaction(
                emitter=self.name,
                old_owner="-",
                new_owner=new_owner,
                car_id=new_vehicle_vin
            )
            print(f"Generating new vehicle registration transaction for vehicle {new_vehicle_vin} with owner {new_owner}.")
        else:
            # Get random vehicle ID with owner for transfer
            # Get random block
            block_idx = random.randint(0, len(self.blockchain) - 1)
            vehicle_id = None
            old_owner = None
            for tx in self.blockchain[block_idx].transactions:
                if isinstance(tx, CarTransaction):
                    # Found a transaction with a vehicle and an owner
                    vehicle_id = tx.car_id
                    old_owner = tx.new_owner
                    break
            if vehicle_id is None or old_owner is None:
                # This time we could not find a vehicle with an owner, so we will not generate a transfer transaction
                print("No vehicle with an owner found in the blockchain, skipping vehicle transfer generation.")
                return None
            # Now check if the vehicle still is owned by the old owner
            for block in reversed(self.blockchain):
                for t in block.transactions:
                    if t.car_id == vehicle_id and t.new_owner == old_owner:
                        # Found the vehicle with the old owner
                        transaction = CarTransaction(
                            emitter=self.name,
                            old_owner=old_owner,
                            new_owner=self._generate_vehicle_owner(),
                            car_id=vehicle_id
                        )
                        print(f"Vehicle {vehicle_id} is still owned by {old_owner}, generating transfer transaction.")
                        break
                    elif t.car_id == vehicle_id and t.new_owner != old_owner:
                        # Vehicle has been transferred, so we will use it with the new owner
                        transaction = CarTransaction(
                            emitter=self.name,
                            old_owner=t.new_owner,
                            new_owner=self._generate_vehicle_owner(),
                            car_id=vehicle_id
                        )
                        print(f"Vehicle {vehicle_id} has been transferred, generating transfer transaction with new owner {t.new_owner}.")
                        break
                if transaction is not None:
                    # We found the transaction on the blockchain, we dont need to search for older instances
                    break
        return transaction
    
    def _generate_chassis_number(self):
        # Allowed characters: letters (except I, O, Q) and digits
        allowed_letters = ''.join(c for c in string.ascii_uppercase if c not in 'IOQ')
        allowed_chars = allowed_letters + string.digits

        # Generate first 8 characters
        vin_start = ''.join(random.choices(allowed_chars, k=8))

        # Placeholder check digit (normally calculated via a weighted formula)
        check_digit = random.choice(string.digits + 'X')  # X is valid as check digit

        # Generate remaining characters (positions 10-17)
        vin_end = ''.join(random.choices(allowed_chars, k=8))

        # Combine all parts
        vin = vin_start + check_digit + vin_end
        return vin
    
    def _generate_vehicle_owner(self):
        # Generate a random vehicle owner
        return f"Owner-{random.randint(100000, 999999)}"
    
if __name__ == "__main__":
    # If this file is run directly, create a GovernmentalInstitution node and start it
    node = GovernmentalInstitution()
    node.start()