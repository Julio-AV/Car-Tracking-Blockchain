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
        self.TRANSACTIONS_PER_BLOCK = 5  # Number of transactions per block

    def operate(self):
        # Override the start method to add governmental institution specific functionality
        print("Welcome aboard, governmental institution!")
        # First we generate some vehicles, so the other nodes can operate with them
        time.sleep(4)  # Give time for the connections to be established
        print("Generating initial vehicle registrations...") 
        is_first_generation = True # When we create varios governmental institution nodes, we want to generate the initial transactions even if other governmental institutions are already started
        while len(self.data_handler.transaction_list) == 0 or is_first_generation:
            is_first_generation = False
            # Wait other nodes might not be connected yet, so we wait until we receive some transactions from the network
            print("Waiting for initial vehicle registrations to be generated...")
            for _ in range(self.TRANSACTIONS_PER_BLOCK):
                transaction = self._gen_data("new_vehicle")
                if transaction is not None:
                    transaction.prepare_transaction(self.private_key)
                    serialized_transaction = transaction.serialize()
                    self.queue_to_connectionHandler.put(serialized_transaction)
                    print(f"Initial vehicle registration {transaction.pretty_print()} sent to connection handler")
                else:
                    # We should never reach this since we are generating new vehicles and no None values should be returned
                    raise ValueError("Failed to generate initial vehicle registration transaction.")
                # Sleep for a while before generating the next transaction
                time.sleep(0.2)
        # Now we generate the first block with the initial transactions
        print("Generating initial block with vehicle registrations...")
        initial_block = Block("0", 0, list(self.data_handler.transaction_list), self.name)
        initial_block.prepare_block(self.private_key)
        serialized_initial_block = initial_block.serialize()
        self.queue_to_connectionHandler.put(serialized_initial_block)
        print("Initial block sent to connection handler")
        # Clear the local transaction pool
        self._clear_transaction_list(self.TRANSACTIONS_PER_BLOCK)
        time.sleep(1)  # Give time for the initial block to be processed

        # Now we will create enough new cars to fill the blockchain
        print("Populating blockchain with new vehicle registrations")
        N = 3  # Number of blocks to create
        # Create N new blocks with 5 new vehicles each
        for _ in range(N):
            # Create 5 transactions 
            for _ in range(self.TRANSACTIONS_PER_BLOCK):
                transaction = self._gen_data("new_vehicle")
                if transaction is not None:
                    transaction.prepare_transaction(self.private_key)
                    serialized_transaction = transaction.serialize()
                    self.queue_to_connectionHandler.put(serialized_transaction)
                time.sleep(0.2)
            block = Block(self.blockchain[-1].header.block_hash, len(self.blockchain), list(self.data_handler.transaction_list), self.name)
            block.prepare_block(self.private_key)
            serialized_block = block.serialize()
            self.queue_to_connectionHandler.put(serialized_block)
            self._clear_transaction_list(self.TRANSACTIONS_PER_BLOCK)

        # Now we simulate the realistic scenario where the governmental institution generates any kind of transaction
        while True:
            # Generate data to be sent to the network
            transaction = self._gen_data()
            if transaction is not None:
                transaction.prepare_transaction(self.private_key)
                serialized_transaction = transaction.serialize()
                self.queue_to_connectionHandler.put(serialized_transaction)
                print(f"Transaction created and sent to connection handler")
            else:
                print("No transaction generated, skipping...")
            # Sleep for a while before generating the next transaction
            #Theoretically, each 10 seconds a new vehicle is transferred, but we will simulate this with a delay between 4 and 6 seconds
            time.sleep(random.uniform(4, 6))

            #Check if we have enough transactions to create a block
            with self.transaction_list_lock:
                # We use the lock to avoid clearing new transactions received on the data handler
                if len(self.data_handler.transaction_list) >= self.TRANSACTIONS_PER_BLOCK:
                    print("Enough transactions to create a block, generating block...")
                    
                    block = Block(self.blockchain[-1].header.block_hash, len(self.blockchain), list(self.data_handler.transaction_list)[:self.TRANSACTIONS_PER_BLOCK], self.name)
                    block.prepare_block(self.private_key)
                    serialized_block = block.serialize()
                    self.queue_to_connectionHandler.put(serialized_block)
                    print("Block sent to connection handler")
                    # Clear the local transaction pool
                    self._clear_transaction_list(self.TRANSACTIONS_PER_BLOCK)

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
            block_idx = random.randint(0, len(self.blockchain) - 1) if len(self.blockchain) > 0 else 0 # Defensive programming, we should always have at least the genesis block
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
                    if not isinstance(t, CarTransaction):
                        # Skip transactions that are not car transactions
                        continue
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