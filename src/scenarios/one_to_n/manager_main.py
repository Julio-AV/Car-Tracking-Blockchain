import os
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
        print("Welcome aboard, manager!")
        time.sleep(1)
        
            
        

        
if __name__ == "__main__":
    print(f"Data path: {os.system("ls data")}")
    node: ManagerNode = ManagerNode()
    node.start()