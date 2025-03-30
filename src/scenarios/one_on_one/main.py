from comms.node import Node
from utils.key_handler import load_keys, load_node_name
import time
import os
if __name__ == "__main__":
    print(f"Data path: {os.system("ls data")}")
    node = Node()
    node.start()