import os
from comms.node import Node
from blockchain.structure.carTransaction import CarTransaction
from blockchain.structure.block import Block
from cryptography.hazmat.primitives.asymmetric import rsa
from utils.IP_file_handler import read_connections_from_file
import time
import json
import random
class ManagerNode(Node):
    #inherit node class and extend it to add manager specific functionality
    def __init__(self):
        super().__init__()
        print(f"Manager node will open connections with: {read_connections_from_file(self.IP)}")
        self.manipulate = False
    
    def receive(self):
        while True:
            if not self.manipulate:
                # If we are not manipulating the next transaction, we just receive it and send it to the data handler
                data_to_send = self.queue_from_connectionHandler.get()
                self.queue_to_dataHandler.put(data_to_send)

    def operate(self):
        #Override the start method to add manager specific functionality
        print("Welcome aboard, manager!")
        #Generating genesis block
        
        introduced_data = ""
        
        while True:
            #Menu to introduce data to the network
            introduced_data = input("Introduce data to the network (1: block, 2: transaction, 3: manipulate next transaction received, 4: print transaction pool,exit: exit): ")
            if introduced_data == "exit":
                print("Exiting...")
                break
            elif introduced_data == "1":
                if self.data_handler.transaction_list == []:
                    print("No transactions in the data handler, please create a transaction first.")
                    continue
                block = None
                if len(self.blockchain) == 0:
                    print("No blocks in the blockchain, creating genesis block...")
                    #Create genesis block
                    block = Block("0", 0, self.data_handler.transaction_list, self.name)
                    print("Creating genesis block...")
                else:
                    #Create block with the last block hash
                    block = Block(self.blockchain[-1].header.hash, len(self.blockchain), self.data_handler.transaction_list, self.name)
                    print(f"Creating block number {len(self.blockchain)}...")
                block.prepare_block(self.private_key)
                serialized_block = block.serialize()
                self.queue_to_connectionHandler.put(serialized_block)
                print("Block sent to connection handler")
            elif introduced_data == "2":
                #Create transaction
                random_id = str(random.randint(100000, 999999))
                transaction = CarTransaction(
                    emitter=self.name,
                    old_owner="-",
                    new_owner="First Owner",
                    car_id=random_id
                    )
                transaction.prepare_transaction(self.private_key) 
                serialized_transaction = transaction.serialize()   
                self.queue_to_connectionHandler.put(serialized_transaction)
                print("Transaction sent to connection handler")
            elif introduced_data == "3":
                #TODO: Implement transaction manipulation: when data is received from queue, manipulate it and send it back to the connection handler, implement it with a flag for the queue handler
                print("Manipulating next transaction received...")
                self.manipulate = True
                data_to_manipulate = self.queue_from_connectionHandler.get()
                try: 
                    json_data = json.loads(data_to_manipulate)
                except json.JSONDecodeError:
                    print("Data received was not in JSON format")
                    continue
                if "header" in json_data and "transactions" in json_data.keys():
                    
                    #Manipulate transaction
                    json_data["transactions"][0]["new_owner"] = "485943K"

                else:
                    json_data["new_owner"] = "485943K"

                self.queue_to_connectionHandler.put(json.dumps(json_data))
                print("Manipulated transaction sent to connection handler")
            elif introduced_data == "4":
                # print transactions in the data handler
                print(f"Transactions in the data handler: {len(self.data_handler.transaction_list)}")
                for transaction in self.data_handler.transaction_list:
                    print(transaction.serialize())
                    
                


            else:
                print("Invalid option, please try again.")

            
        
            
        

        
if __name__ == "__main__":
    print(f"Data path: {os.system("ls data")}")
    node: ManagerNode = ManagerNode()
    node.start()