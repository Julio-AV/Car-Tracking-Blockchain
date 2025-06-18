import os
from comms.node import Node
from blockchain.structure.carTransaction import CarTransaction
from blockchain.structure.inspectionTransaction import InspectionTransaction
from blockchain.structure.accidentTransaction import AccidentTransaction
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
    
    def receive(self):
        while True:
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
            introduced_data = input("Introduce data to the network (1: block, 2: transaction, 3: Create manipulated transaction received, 4: print transaction pool, 5: print blockchain ,exit: exit): ")
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
                    block = Block(self.blockchain[-1].header.block_hash, len(self.blockchain), self.data_handler.transaction_list, self.name)
                    print(f"Creating block number {len(self.blockchain)}...")
                block.prepare_block(self.private_key)
                serialized_block = block.serialize()
                self.queue_to_connectionHandler.put(serialized_block)
                print("Block sent to connection handler")
            elif introduced_data == "2":
                #Create transaction
                transaction = self.create_transaction()
                if not transaction:
                    print("No transaction created, please try again.")
                    continue
                transaction.prepare_transaction(self.private_key) 
                serialized_transaction = transaction.serialize()   
                self.queue_to_connectionHandler.put(serialized_transaction)
                print(f"Transaction {transaction.pretty_print()} sent to connection handler")
            elif introduced_data == "3":
                transaction = self.create_transaction()
                if not transaction:
                    print("No transaction created, please try again.")
                    continue
                transaction.prepare_transaction(self.private_key)
                print(f"Transaction created before manipulation: {transaction.serialize()}")
                #Manipulate transaction
                if type(transaction) == CarTransaction:
                    manipulated_car_id = input("Enter new car ID: ")
                    manipulated_old_owner = input("Enter new old owner: ")
                    manipulated_new_owner = input("Enter new new owner: ")
                    if manipulated_new_owner:
                        transaction.new_owner = manipulated_new_owner
                    if manipulated_old_owner:
                        transaction.old_owner = manipulated_old_owner
                    if manipulated_car_id:
                        transaction.car_id = manipulated_car_id
                elif type(transaction) == InspectionTransaction:
                    manipulated_car_id = input("Enter new car ID: ")
                    manipulated_kilometers = input("Enter new kilometers: ")
                    if manipulated_kilometers:
                        transaction.kilometers = manipulated_kilometers
                    if manipulated_car_id:
                        transaction.car_id = manipulated_car_id
                elif type(transaction) == AccidentTransaction:
                    manipulated_car_id = input("Enter new car ID: ")
                    manipulated_driver_id = input("Enter new driver ID: ")
                    manipulated_severity = input("Enter new severity: ")
                    if manipulated_car_id:
                        transaction.car_id = manipulated_car_id
                    if manipulated_driver_id:
                        transaction.driver_id = manipulated_driver_id
                    if manipulated_severity:
                        transaction.severity = manipulated_severity
                print(f"Transaction after manipulation: {transaction.serialize()}")
                serialized_transaction = transaction.serialize()
                self.queue_to_connectionHandler.put(serialized_transaction)
                print("Manipulated transaction sent to connection handler")
            elif introduced_data == "4":
                # print transactions in the data handler
                print(f"Transactions in the data handler: {len(self.data_handler.transaction_list)}")
                for transaction in self.data_handler.transaction_list:
                    print(transaction.pretty_print())
                    
                
            elif introduced_data == "5":
                # print blocks in the blockchain
                print(f"Blocks in the blockchain: {len(self.blockchain)}")
                for block in self.blockchain:
                    print(block.pretty_print())

            else:
                print("Invalid option, please try again.")

            
        
            
        
    def create_transaction(self):
        type_of_transaction = input("Type of transaction (1: Vehicle transaction, 2: Inspection transaction, 3: Accident transaction ): ")
        transaction = None
        if type_of_transaction == "1":
            print("Creating vehicle transaction...")
            #Create vehicle transaction
            car_id = input("Enter car ID: ")
            old_owner = input("Enter old owner: ")
            new_owner = input("Enter new owner: ")
            transaction = CarTransaction(
                emitter=self.name,
                old_owner=old_owner,
                new_owner=new_owner,
                car_id=car_id
                )
        elif type_of_transaction == "2":
            print("Creating inspection transaction...")
            #Create inspection transaction
            car_id = input("Enter car ID: ")
            mileage = input("Enter mileage: ")
            transaction = InspectionTransaction(
                emitter=self.name,
                car_id=car_id,
                kilometers=mileage
                )
        elif type_of_transaction == "3":
            print("Creating accident transaction...")
            #Create accident transaction
            car_id = input("Enter car ID: ")
            driver_id = input("Enter driver ID: ")
            severity = input("Enter severity: ")
            transaction = AccidentTransaction(
                emitter=self.name,
                car_id=car_id,
                driver_id=driver_id,
                severity=severity
                )
        return transaction
        
if __name__ == "__main__":
    node: ManagerNode = ManagerNode()
    node.start()